import numpy as np
from gnuradio import gr

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Python Message Source',   # will show up in GRC
            in_sig=[],
            out_sig=[np.byte]
        )
        self.last_message = []

    def work(self, input_items, output_items):
	string = [1,2,3,4,4,7,65,65,66,67,5,6,7,8]
	string_mult = string * (4096 / len(string))
	output_items[0] = [string_mult[0:4096]]
        return 1
