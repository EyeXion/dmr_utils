import os

# The named pipe path
fifo_path = '/tmp/fifo'

# Expected sequence for comparison
expected_sequence1 = [1,0,1,1,0,0,1,0,0,0,0,1,1,0,1,1,1,0,0,0,0,1,0,1,1,1,0,1,0,0,1,1,0]
expected_sequence2 = [1,0,0,0,0,1,0,0,1,0,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,0,0,1,0,0,1,1,0]

with open(fifo_path, 'rb') as fifo:
    buffer = []
    while True:
        byte = fifo.read(1)
        if byte:
            bit = int.from_bytes(byte, byteorder='big')
            buffer.append(bit)


            preamble_length = 10
            preamble1 = expected_sequence1[:preamble_length] 
            preamble2 = expected_sequence2[:preamble_length] 


            preamble1 = preamble2
            expected_sequence1 =  expected_sequence2
            sequence_length = 33  # Total length of the sequence to check

            for i in range(len(buffer) - preamble_length + 1):
                if buffer[i:i+preamble_length] == preamble1 or buffer[i:i+preamble_length] == preamble2:
                    if len(buffer) >= i + sequence_length:
                        sequence = buffer[i:i+sequence_length]
                        sequence_str = ''.join(map(str, sequence))
                        expected_sequence_str1 = ''.join(map(str, expected_sequence1))
                        expected_sequence_str2 = ''.join(map(str, expected_sequence2))
                        if sequence_str == expected_sequence_str1 or sequence_str == expected_sequence_str2:
                            print(sequence_str + " OK")
                            print("".join(map(str,buffer)))
                            buffer = buffer[i+sequence_length:]
                        else:
                            print(sequence_str + " KO")

                        buffer = buffer[i+preamble_length:]
                    else:
                        pass
                else:
                    if len(buffer) >= 128:
                        buffer_str = ''.join(map(str, buffer))
                        print(buffer_str)
                        buffer = []
        else:
            break

