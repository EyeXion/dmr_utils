#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 gr-dmr author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr
import pmt
import socket
import threading
from collections import deque

class burst_source(gr.basic_block):
    def __init__(self, ip='127.0.0.1', port=52010):
        # Inherit from gr.basic_block instead of gr.sync_block
        gr.basic_block.__init__(
            self,
            name='DMR Burst Source',
            in_sig=None, # Source block, no inputs
            out_sig=[np.float32]
        )
        self.ip = ip
        self.port = port
        self.map = {0: 0.5, 1: 1.5, 2: -0.5, 3: -1.5}
        
        self.burst_queue = deque() 
        self.current_frame = []
        
        # Compteurs de zéros
        self.mandatory_silence_left = 0 # zéros non esquivables, pour le silence intertrames
        self.flushing_done_count = 0 # zéros esquivables, pour flusher les filtres et pousser les derniers symboles
        

        self.stop_thread = threading.Event()
        self.thread = threading.Thread(target=self.socket_listener, daemon=True)
        self.thread.start()

    # bon la logique du socket, rien de spécial
    def socket_listener(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.ip, self.port))
        sock.settimeout(0.5)
        
        while not self.stop_thread.is_set(): # event + stop car sinon mon flowgraph mourrait jamais mdr
            try:
                #33 data + 2 bytes d'indication de nb de silnce
                data, addr = sock.recvfrom(1024)
                if len(data) >= 35:
                    #on transorme en dibits
                    bytes_array = np.frombuffer(data[:33], dtype=np.uint8)
                    dibits = []
                    for b in bytes_array:
                        dibits.append(self.map[(b >> 6) & 0x03])
                        dibits.append(self.map[(b >> 4) & 0x03])
                        dibits.append(self.map[(b >> 2) & 0x03])
                        dibits.append(self.map[b & 0x03])
                    
                   # frame = [0.0, 0.0] + dibits + [0.0, 0.0] # les symboles de padding pour pas couper
                    frame = dibits # les symboles de padding pour pas couper
                    
                    #les deux derniers bytes sont le nb de symbole de silence
                    silence_duration = int.from_bytes(data[33:35], byteorder='big')
                    
                    # on met notre fatra dans la queue (leuleu) (kill me)
                    self.burst_queue.append((frame, silence_duration))
            except socket.timeout:
                continue
            except Exception:
                break
        sock.close()

    # Askip basic_block (donc on gère tout) ======> general_work (et pas work)
    def general_work(self, input_items, output_items):
        out = output_items[0] # magie noire des output, mais en gros output 1
        n_out = len(out) # la taille du buffer out
        produced = 0

        while produced < n_out:
            # SI on a des frames à envoyer, ON ENVOIE
            if self.current_frame:
                n_to_send = min(n_out - produced, len(self.current_frame))
                out[produced:produced + n_to_send] = self.current_frame[:n_to_send]
                
                self.current_frame = self.current_frame[n_to_send:]
                produced += n_to_send
                
                # si la rame est terminée, on reset le nb de zéro flushé
                if not self.current_frame:
                    self.flushing_done_count = 0
                continue

            # SILENCE inintérompable (ortho ?), mis en arg du PDU
            if self.mandatory_silence_left > 0:
                n_silence = min(n_out - produced, self.mandatory_silence_left)
                out[produced:produced + n_silence] = [0.0] * n_silence
                
                self.mandatory_silence_left -= n_silence
                self.flushing_done_count += n_silence
                produced += n_silence
                # on check pas si la queue car ININTEMROMPABLE, donc le continue dégueu
                continue

            # Check pour burst 
            if self.burst_queue:
                frame_data, silence_val = self.burst_queue.popleft()
                self.current_frame = frame_data # on met la prochaine frame dans le current frame
                self.mandatory_silence_left = silence_val
                
                # on met les tags là où il faut bien
                abs_index = self.nitems_written(0) + produced
                self.add_item_tag(0, abs_index, pmt.intern("tx_sob"), pmt.from_bool(True))
                self.add_item_tag(0, abs_index + 136, pmt.intern("tx_eob"), pmt.from_bool(True))
                # rpchaine itération, le current frame va être consommé
                continue
            
            # si rien à faire et qu'on a pas assez flush, bah on flush
            if self.flushing_done_count < 30:
                n_flush = min(n_out - produced, 30 - self.flushing_done_count)
                out[produced:produced + n_flush] = [0.0] * n_flush
                
                self.flushing_done_count += n_flush
                produced += n_flush
                # ici vu qu'on est en bas de la boucle, si une trame arrive en plein milieu bah on se fait hijack :)
                continue

            
            # return value. si on a envoyé des trucs, on renvoie lenb, sinon HALTING
            if produced > 0:
                return produced
            else:
                return 0 

        return produced

    def stop(self):
        self.stop_thread.set()
        self.thread.join(timeout=0.2)
        return True
