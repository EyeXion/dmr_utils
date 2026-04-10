from whad.phy.connector.sniffer import Sniffer
from whad.device import WhadDevice
from whad.exceptions import WhadDeviceNotFound
from whad.phy.sniffing import SnifferConfiguration
import re


expected_sequence1 = [1,0,0,0,0,1,0,0,1,0,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,0,0,1,0,0,1,1,0]
c = [[1, 1, 1, 0] if s == 1 else [1, 0, 0, 0] for s in expected_sequence1]
expected_sequence1 = [item for sublist in c for item in sublist]

dev = None
try:
    # Instanciation du code
    dev = WhadDevice.create("yardstickone0")

    sniffer = Sniffer(dev)
    sniffer.configuration = SnifferConfiguration(
        ask=True, datarate=1923, frequency=433885000, packet_size=17, sync_word=b"\xe8"
    )
    sniffer.start()
    expected_sequence = "".join(map(str, expected_sequence1))
    print("Expected Sequence ", expected_sequence)
    for packet in sniffer.sniff():
        # packet.show()
        raw_bytes = bytes(packet).hex()
        raw_bits = bin(int(raw_bytes, 16))[2:]
        i = 0
        for m in re.finditer("".join(map(str, expected_sequence1)), raw_bits):
            i+= 1
            print("FOUND SEQUENCE", m.start(), m.end())
        print("Number of sequences found ", i)
        if i == 0:
            print(raw_bits)

except KeyboardInterrupt:
    if dev is not None:
        dev.close()
    exit(2)

except WhadDeviceNotFound:
    print("Not found device")
    exit(1)