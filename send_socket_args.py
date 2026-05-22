#!/bin/python3


import socket
import time
import sys
import argparse

def process_data(lines, ip, port, repeat, delay_symbols):
    """Processes the list of lines and sends them to the socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # inter replay delay timer sortof kindof estimation-ish
    inter_rep_delay = delay_symbols / 4800.0
    
    count = 0
    try:
        while repeat == -1 or count < repeat:
            print("Repet numéro ", str(count)) 
            idx = 0
            while idx < len(lines):
                line = lines[idx].strip()
                if not line or ":SILENCE" in line:
                    idx += 1
                    continue
                
                parts = line.split()
                if len(parts) < 3:
                    idx += 1
                    continue
                
                data_hex = parts[2]
                
                if len(data_hex) == 66:
                    # silence par default
                    #silence_val = 156 - 4 # preambule == silence kindof)
                    silence_val = 156  # preambule == silence kindof)
                    
                    # on regarde la ligne en dessous pour voir si y'a du silence
                    if idx + 1 < len(lines) and ":SILENCE" in lines[idx + 1]:
                        try:
                            silence_val = int(lines[idx + 1].split(':')[0])
                            idx += 1 
                        except (ValueError, IndexError):
                            pass
                    
                    # sendiiiining packettu
                    try:
                        frame_bytes = bytes.fromhex(data_hex)
                        packet = frame_bytes + silence_val.to_bytes(2, byteorder='big')
                        print(packet)
                        sock.sendto(packet, (ip, port))
                        
                        time.sleep(0.02) 
                    except ValueError:
                        print("ouch")
                idx += 1
            
            count += 1
            if (repeat == -1 or count < repeat) and delay_symbols > 0:
                print("Sleeping between repeatition, vivement la retraite pfiou")
                time.sleep(inter_rep_delay)

    except KeyboardInterrupt:
        print("Bye bye bg")
    finally:
        sock.close()

def main():
    # merchi à l'ia pour le parsing d'arg o_o (je devrais tout faire avec en fait)
    parser = argparse.ArgumentParser(description="DMR Frame Socket Sender")
    parser.add_argument("-f", "--file", type=str, help="Input file containing DMR frames")
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1", help="Target IP (default: 127.0.0.1)")
    parser.add_argument("-p", "--port", type=int, default=52010, help="Target Port (default: 52010)")
    parser.add_argument("-r", "--repeat", type=int, default=1, help="Number of repetitions (-1 for infinite)")
    parser.add_argument("-d", "--delay", type=int, default=0, help="Delay between repetitions in symbols")
    
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, 'r') as f:
                input_text = f.read()
        except FileNotFoundError:
            return
    else:
        print("pas de fichier en input, stdin input (CTRL-D)")
        input_text = sys.stdin.read()

    lines = [l for l in input_text.split('\n') if l.strip()]
    if not lines:
        return

    process_data(lines, args.ip, args.port, args.repeat, args.delay)

if __name__ == "__main__":
    main()
