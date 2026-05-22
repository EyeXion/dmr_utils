import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name='Zero Idle Bursts',
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.set_history(128)  # Safe buffer for delayed tag detection
        self.zero_tag = pmt.string_to_symbol("zero_samples")
        self.sample_counter = 0
        #self.delay = 62  # (125-1)//2 for RRC taps
        self.delay = 62  # (125-1)//2 for RRC taps


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        n = len(out)
        tags = self.get_tags_in_window(0, 0, n, self.zero_tag)
        if tags:
            tags = sorted(tags, key=lambda t: t.offset)
        abs_n = self.nitems_written(0)
        for i in range(n):
            for tag in tags:
                if tag.offset == abs_n + i - self.delay:  # Negative delay postpones zeroing
                    self.sample_counter = pmt.to_uint64(tag.value)
                    break
            if self.sample_counter > 0:
                out[i] = 0 + 0j
                self.sample_counter -= 1
            else:
                out[i] = in0[i]
        return len(out)