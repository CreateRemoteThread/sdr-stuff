#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# lighting up the (rf) skies demo (v1)
# lin_s

if __name__ == '__main__':
  import ctypes
  import sys
  if sys.platform.startswith('linux'):
    try:
      x11 = ctypes.cdll.LoadLibrary('libX11.so')
      x11.XInitThreads()
    except:
      print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
import osmosdr
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import epy_block_0_0
import sip
import sys
import time
from gnuradio import qtgui
from PIL import Image
import copy

usrp_enable = False

class noise(gr.top_block, Qt.QWidget):
  def __init__(self, imagefile):
    f = Image.open(imagefile)
    width,height = f.size
    f_rgb = f.convert("RGB") 
    gr.top_block.__init__(self, "hi")
    Qt.QWidget.__init__(self)
    self.setWindowTitle("hi")
    qtgui.util.check_set_qss()
    try:
      self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
    except:
      pass
    self.top_scroll_layout = Qt.QVBoxLayout()
    self.setLayout(self.top_scroll_layout)
    self.top_scroll = Qt.QScrollArea()
    self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
    self.top_scroll_layout.addWidget(self.top_scroll)
    self.top_scroll.setWidgetResizable(True)
    self.top_widget = Qt.QWidget()
    self.top_scroll.setWidget(self.top_widget)
    self.top_layout = Qt.QVBoxLayout(self.top_widget)
    self.top_grid_layout = Qt.QGridLayout()
    self.top_layout.addLayout(self.top_grid_layout)

    self.settings = Qt.QSettings("GNU Radio", "noise")
    self.restoreGeometry(self.settings.value("geometry").toByteArray())

    ##################################################
    # Blocks
    ##################################################
    if usrp_enable:
      self.uhd_usrp_sink_0 = uhd.usrp_sink(
       	",".join(("", "")),
        uhd.stream_args(
      		cpu_format="fc32",
      		channels=range(1),
      	),
      )
      self.uhd_usrp_sink_0.set_samp_rate(400)
      self.uhd_usrp_sink_0.set_center_freq(2460000000, 0)
      self.uhd_usrp_sink_0.set_gain(50, 0)
      self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
      self.uhd_usrp_sink_0.set_bandwidth(width * 5, 0)
    else:
      self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + '' )
      self.osmosdr_sink_0.set_time_source('gpsdo', 0)
      self.osmosdr_sink_0.set_sample_rate(80000)
      self.osmosdr_sink_0.set_center_freq(2400000000, 0)
      self.osmosdr_sink_0.set_freq_corr(0, 0)
      self.osmosdr_sink_0.set_gain(10, 0)
      self.osmosdr_sink_0.set_if_gain(20, 0)
      self.osmosdr_sink_0.set_bb_gain(20, 0)
      self.osmosdr_sink_0.set_antenna('0', 0)
      self.osmosdr_sink_0.set_bandwidth(20, 0)
    self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
      5000, #size
      firdes.WIN_BLACKMAN_hARRIS, #wintype
      2460000000, #fc
      400, #bw
      "", #name
      1 #number of inputs
    )
    self.qtgui_freq_sink_x_0.set_update_time(0.10)
    self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
    self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
    self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
    self.qtgui_freq_sink_x_0.enable_autoscale(True)
    self.qtgui_freq_sink_x_0.enable_grid(True)
    self.qtgui_freq_sink_x_0.set_fft_average(1.0)
    self.qtgui_freq_sink_x_0.enable_axis_labels(True)
    self.qtgui_freq_sink_x_0.enable_control_panel(False)

    if not True:
     self.qtgui_freq_sink_x_0.disable_legend()

    if "complex" == "float" or "complex" == "msg_float":
     self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

    labels = ['', '', '', '', '',
         '', '', '', '', '']
    widths = [1, 1, 1, 1, 1,
         1, 1, 1, 1, 1]
    colors = ["blue", "red", "green", "black", "cyan",
         "magenta", "yellow", "dark red", "dark green", "dark blue"]
    alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
         1.0, 1.0, 1.0, 1.0, 1.0]
    for i in xrange(1):
      if len(labels[i]) == 0:
        self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
      else:
        self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
      self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
      self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
      self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

    self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
    self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
   
    print " [!] attempting to write filling column data"
 
    self.columns = []
    # drop a zero column for alignment purposes
    self.columns.append(analog.sig_source_c(100,analog.GR_SIN_WAVE,5,1,0))

    # create "zero" column for alignment purposes
    for x in range(1,width):
      temp_coldata = []
      # grab column data pixel by pixel
      for y in range(height-1,-1,-1): 
        (r,g,b) = f_rgb.getpixel((x,y))
        if r + g + b > 375:
          temp_coldata.append(0.0)
        else:
          temp_coldata.append(1.0)
      temp_signal = analog.sig_source_c(100,analog.GR_SIN_WAVE,5+(x * 3),1,0)
      temp_filter = epy_block_0_0.blk(height,temp_coldata)
      temp_add = blocks.add_vcc(1)    
      self.connect((temp_signal,0), (temp_filter,0))
      self.connect((temp_filter,0), (temp_add,0))
      self.connect((self.columns[-1],0),(temp_add,1))
      print " [+] adding column %d data..." % (x)
      self.columns.append(temp_add)

    print " [!] writing final brace column"  

    self.connect((self.columns[-1],0),(self.qtgui_freq_sink_x_0,0))
    if usrp_enable:
      print " [+] ok, connecting USRP sink. going live..."
      self.connect((self.columns[-1],0),(self.uhd_usrp_sink_0,0))
    else:
      print " [+] ok, connecting osmocom sink, going live..."
      self.connect((self.columns[-1],0),(self.osmosdr_sink_0,0))
      

  def closeEvent(self, event):
    self.settings = Qt.QSettings("GNU Radio", "noise")
    self.settings.setValue("geometry", self.saveGeometry())
    event.accept()

def main(top_block_cls=noise, options=None):
  from distutils.version import StrictVersion
  if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
    style = gr.prefs().get_string('qtgui', 'style', 'raster')
    Qt.QApplication.setGraphicsSystem(style)
  qapp = Qt.QApplication(sys.argv)
  if(len(sys.argv) < 2):
    print "usage: %s [imagefile]" % (sys.argv[0])
    sys.exit(0)
  tb = top_block_cls(sys.argv[1])
  tb.start()
  tb.show()

  def quitting():
    tb.stop()
    tb.wait()
  qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
  qapp.exec_()

if __name__ == '__main__':
  main()
