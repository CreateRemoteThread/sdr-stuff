#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Source To File
# Generated: Sun Apr 16 22:38:20 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import numpy
import osmosdr
import time
import wx
from threading import Thread

class source_to_file(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Source To File")

        ##################################################
        # Variables
        ##################################################
        self.target_freq = target_freq = 2467000000
        self.start_var = start_var = (1,2,3,4,4,10,61,61,62,62,5,6,7,8)
        self.samp_rate = samp_rate = 500000
        self.cocks = 5

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_fftsink2_1 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=target_freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot - TX',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_1.win)
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + 'bladerf' )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(target_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(50, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)

        self.digital_gmsk_mod_1 = digital.gmsk_mod(
        	samples_per_symbol=2,
        	bt=0.35,
        	verbose=False,
        	log=False,
        )
        self.blocks_vector_source_x_0 = blocks.vector_source_b(start_var, True, 1, [])
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((1.0, ))
        self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=2,
        		bits_per_symbol=1,
        		preamble='',
        		access_code='',
        		pad_for_usrp=False,
        	),
        	payload_length=0,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_packet_encoder_0, 0), (self.digital_gmsk_mod_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blks2_packet_encoder_0, 0))
        self.connect((self.digital_gmsk_mod_1, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.digital_gmsk_mod_1, 0), (self.wxgui_fftsink2_1, 0))
        self.packetQueue = Thread(target=source_to_file.changeValueThread, args=(self,))
        self.packetQueue.start()

    def changeValueThread(self):
        while True:
            print " + moving packet id forward"
            self.cocks += 1
            start_var = (1,2,3,4,4,self.cocks,61,61,62,62,5,6,7,8)
            self.blocks_vector_source_x_0.set_data(start_var)
            time.sleep(5)

    def get_target_freq(self):
        return self.target_freq

    def set_target_freq(self, target_freq):
        self.target_freq = target_freq
        self.wxgui_fftsink2_1.set_baseband_freq(self.target_freq)
        self.osmosdr_sink_0.set_center_freq(self.target_freq, 0)

    def get_start_var(self):
        return self.start_var

    def set_start_var(self, start_var):
        self.start_var = start_var
        self.blocks_vector_source_x_0.set_data(self.start_var, [])

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_1.set_sample_rate(self.samp_rate)
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)


def main(top_block_cls=source_to_file, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
