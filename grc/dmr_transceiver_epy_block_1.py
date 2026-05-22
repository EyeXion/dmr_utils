import numpy as np
from gnuradio import gr
import pmt

class blk(gr.basic_block):
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='DMR Gated TX Controller',
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # Initial state is Silence
        self.state = "SILENCE"

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        n_input = len(in0)
        n_output = len(out)
        
        # We process as much as we can based on buffer availability
        n_process = min(n_input, n_output)
        
        # Get tags associated with this batch of input samples
        tags = self.get_tags_in_window(0, 0, n_process)

        for i in range(n_process):
            # Check if any tags start or end a burst at this specific sample
            for tag in tags:
                if tag.offset == self.nitems_read(0) + i:
                    tag_name = pmt.symbol_to_string(tag.key)
                    if tag_name == "tx_sob":
                        self.state = "TX"
                    elif tag_name == "tx_eob":
                        self.state = "SILENCE"

            # State Machine Output
            if self.state == "TX":
                # Pass the modulated DMR signal through
                out[i] = in0[i]
            else:
                # Output absolute zero (Radio "Off")
                out[i] = 0.0001 + 0.00001j

        # Consume and produce the samples
        self.consume(0, n_process)
        return n_process