"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Python Message Sink',   # will show up in GRC
            in_sig=[np.byte],
            out_sig=[]
        )
	self.packets_seen = []

    def work(self, input_items, output_items):
        data = input_items[0]
	if len(data) < 10:
		return 1
	# print data
	for r in range(0,len(data) - 9):
		if data[r] == 1:
			if data[r+1] == 2 and data[r+2] == 3 and data[r+3] == 4:
				packetlen = data[r+4]
				packetid = data[r+5]
				if len(data) < r + 10 + packetlen:
					return 1    # too late to complete the packet, wait for next
				if data[r+6 + packetlen] == 5 and data[r+7 + packetlen] == 6 and data[r+8 + packetlen] == 7 and data[r+9 + packetlen] == 8:
					if packetid in self.packets_seen:
						return 1
					else:
						print " ! new packet id %d found" % packetid
						self.packets_seen.append(packetid)
						return 1
				else:
					continue
        return 1
