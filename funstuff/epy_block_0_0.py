#!/usr/bin/env py

# ticker thingy

import numpy as np
from gnuradio import gr

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
  def __init__(self, height=10, coldata=[0,0,0,1,1,1,1,0,0,0]):  # only default arguments here
    gr.sync_block.__init__(
      self,
      name='blink_blink',   # will show up in GRC
      in_sig=[np.complex64],
      out_sig=[np.complex64]
    )
    self.col_data = coldata
    self.height = height
    np.random.seed()
    self.clk = 0
    self.ticker = 0

  def work(self, input_items, output_items):
    if((self.clk % 50) == 0):
      self.ticker += 1
    self.clk += 1
    if self.ticker == self.height - 1:
      self.clk = 0
      self.ticker = 0
    output_items[0][:] = input_items[0] * self.col_data[self.ticker]
    return len(output_items[0])

if __name__ == "__main__":
  print " [!] this is not meant to be called directly"
