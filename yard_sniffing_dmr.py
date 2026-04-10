from whad.phy.connector.sniffer import Sniffer
from whad.device import WhadDevice
from whad.exceptions import WhadDeviceNotFound
from whad.phy.sniffing import SnifferConfiguration, FSKConfiguration
import re

"""
Correspondance symboles 4FSK yard <-> DMR

déjà yard :

11 : +3
10 : +1
00 : -1
01 : -3

table correspondance (yard vers DMR)

11 -> 01
10 -> 00
00 -> 10
01 -> 11
"""

symbol_mapping_y_to_dmr = {"11":"01", "10":"00", "00":"10", "01":"11"}

pattern = "".join(["{:08b}".format(t) for t in b"\xD5\xD7\xF7\x7F"])
#pattern = "".join(["{:08b}".format(t) for t in b"\xD5\xD7\xF7\x7F"])
#2832222F22F3629222222E244A2D7557F5FF7F5C2E2E28222E4D8AD82322756BE1
#D5D7F77FD757
PAT_FULL = 48
LEFT_SIDE = 108
TOTAL_BITS = 264
HEX_WIDTH = TOTAL_BITS // 4


def find_match(raw_bits, offset=0):
    start = 0
    while True:
        i = raw_bits.find(pattern, start)
        if i == -1:
            break
        packet_start = i - LEFT_SIDE
        packet_end = packet_start + TOTAL_BITS
        if packet_start >= 0 and packet_end <= len(raw_bits):
            packet_bits = raw_bits[packet_start:packet_end]  # 264 bits
            hex_packet = hex(int(packet_bits, 2))
            print("MATCH at bit", i, "->", hex_packet, " AT OFFSET : ", offset)
        start = i + 1

dev = None
try:
    # Instanciation du code
    dev = WhadDevice.create("yardstickone0")

    sniffer = Sniffer(dev)
    sniffer.configuration = SnifferConfiguration(
        qfsk=True, datarate=4800, frequency=433575000, packet_size=400, sync_word=b"", fsk_configuration=FSKConfiguration(deviation=1200)
    )
    sniffer.start()

    for packet in sniffer.sniff():
        raw_bytes = bytes(packet)
        raw_bits = "".join("{:08b}".format(t) for t in raw_bytes)
        raw_bits_offset0 = "".join([symbol_mapping_y_to_dmr[raw_bits[index:index+2]] for index in range(0,len(raw_bits)-1,2)])
        raw_bits_offset1 = "".join([symbol_mapping_y_to_dmr[raw_bits[index:index+2]] for index in range(1,len(raw_bits)-1,2)])
        print("Received packet")
        #print(raw_bits_offset0)

        find_match(raw_bits_offset0, 0)
        find_match(raw_bits_offset1, 1)

        """
        i=0
        for m in re.finditer("".join(map(str, pattern)), raw_bits_offset0):
            i+= 1
            print(m.start())
            print("FOUND SEQUENCE in offset0")
            print(raw_bits_offset0[m.start():max(m.end(),len(raw_bits_offset0))])
        
        i=0
        for m in re.finditer("".join(map(str, pattern)), raw_bits_offset1):
            i+= 1
            print(m.start())
            print("FOUND SEQUENCE in offset1")
            print(raw_bits_offset1[m.start():max(m.end(),len(raw_bits_offset1))])
        """

except KeyboardInterrupt:
    if dev is not None:
        dev.close()
    exit(2)

except WhadDeviceNotFound:
    print("Not found device")
    exit(1)