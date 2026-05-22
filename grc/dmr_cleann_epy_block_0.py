import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):
    def __init__(self, num_silence_slots=1, preamble_symbols=5, postamble_symbols=3):
        gr.sync_block.__init__(self,
            name='Add Zero Tag',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.zero_tag = pmt.string_to_symbol("zero_samples")
        self.data_symbols = 132
        self.idle_symbols_per_slot = 156
        self.num_silence_slots = int(num_silence_slots)
        self.preamble_symbols = int(preamble_symbols)
        self.postamble_symbols = int(postamble_symbols)
        self.idle_symbols = self.idle_symbols_per_slot * self.num_silence_slots
        self.burst_symbols = self.data_symbols + self.idle_symbols
        self.samples_per_symbol = 5
        self.tag_pos = self.preamble_symbols + self.data_symbols + self.postamble_symbols
        self.zero_samples = (self.idle_symbols - self.preamble_symbols - self.postamble_symbols) * self.samples_per_symbol

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        out[:] = in0
        n = len(out)
        start = self.nitems_written(0)
        for i in range(n):
            pos = (start + i) % self.burst_symbols
            if pos == self.tag_pos:
                val = pmt.from_uint64(self.zero_samples)
                self.add_item_tag(0, start + i, self.zero_tag, val)
        return len(out)