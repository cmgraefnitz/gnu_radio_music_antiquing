#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: cmgra
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import threading



class options(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "options")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.wav_len = wav_len = 51800000
        self.update = update = .05
        self.select = select = 0
        self.nyq_freq = nyq_freq = samp_rate/2
        self.noisy = noisy = 0
        self.gramophone_taps = gramophone_taps = firdes.band_pass(1.0, samp_rate, 160, 2000, 10, window.WIN_HAMMING, 6.76)
        self.gramophone_f2 = gramophone_f2 = 2000
        self.gramophone_f1 = gramophone_f1 = 160
        self.delay = delay = 2
        self.allpass_taps = allpass_taps = firdes.band_pass(1.0, samp_rate, 1, 20000, 10, window.WIN_HAMMING, 6.76)
        self.FM_taps = FM_taps = firdes.band_pass(1.0, samp_rate, 30, 15000, 10, window.WIN_HAMMING, 6.76)
        self.FM_f2 = FM_f2 = 15000
        self.FM_f1 = FM_f1 = 30
        self.AM_taps = AM_taps = firdes.band_pass(1.0, samp_rate, 200, 5000, 10, window.WIN_HAMMING, 6.76)
        self.AM_f2 = AM_f2 = 5000
        self.AM_f1 = AM_f1 = 200

        ##################################################
        # Blocks
        ##################################################

        # Create the options list
        self._select_options = [0, 1, 2, 3]
        # Create the labels list
        self._select_labels = ['Original', 'Gramophone', 'AM', 'FM']
        # Create the combo box
        self._select_tool_bar = Qt.QToolBar(self)
        self._select_tool_bar.addWidget(Qt.QLabel("Select Filter" + ": "))
        self._select_combo_box = Qt.QComboBox()
        self._select_tool_bar.addWidget(self._select_combo_box)
        for _label in self._select_labels: self._select_combo_box.addItem(_label)
        self._select_callback = lambda i: Qt.QMetaObject.invokeMethod(self._select_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._select_options.index(i)))
        self._select_callback(self.select)
        self._select_combo_box.currentIndexChanged.connect(
            lambda i: self.set_select(self._select_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._select_tool_bar)
        _noisy_check_box = Qt.QCheckBox("Noisy")
        self._noisy_choices = {True: 1, False: 0}
        self._noisy_choices_inv = dict((v,k) for k,v in self._noisy_choices.items())
        self._noisy_callback = lambda i: Qt.QMetaObject.invokeMethod(_noisy_check_box, "setChecked", Qt.Q_ARG("bool", self._noisy_choices_inv[i]))
        self._noisy_callback(self.noisy)
        _noisy_check_box.stateChanged.connect(lambda i: self.set_noisy(self._noisy_choices[bool(i)]))
        self.top_layout.addWidget(_noisy_check_box)
        self.interp_fir_filter_xxx_0_0_0_0 = filter.interp_fir_filter_fff(1, FM_taps)
        self.interp_fir_filter_xxx_0_0_0_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0_0_0 = filter.interp_fir_filter_fff(1, AM_taps)
        self.interp_fir_filter_xxx_0_0_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0_0 = filter.interp_fir_filter_fff(1, gramophone_taps)
        self.interp_fir_filter_xxx_0_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(1, allpass_taps)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\cmgra\\Desktop\\ECSE 351\\gnu_radio_music_antiquing\\351 music antiquing\\Tomorrow_Is_Today_(original).wav', True)
        self.blocks_wavfile_source_0.set_block_alias("song_source")
        self.blocks_selector_1 = blocks.selector(gr.sizeof_float*1,noisy,0)
        self.blocks_selector_1.set_enabled(True)
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_float*1,select,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(.1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_1_0 = audio.sink(samp_rate, '', True)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, .025, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_selector_1, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_selector_1, 0))
        self.connect((self.blocks_selector_1, 0), (self.audio_sink_1_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.interp_fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.interp_fir_filter_xxx_0_0_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.interp_fir_filter_xxx_0_0_0_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.interp_fir_filter_xxx_0_0, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.interp_fir_filter_xxx_0_0_0, 0), (self.blocks_selector_0_0, 2))
        self.connect((self.interp_fir_filter_xxx_0_0_0_0, 0), (self.blocks_selector_0_0, 3))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "options")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_AM_taps(firdes.band_pass(1.0, self.samp_rate, 200, 5000, 10, window.WIN_HAMMING, 6.76))
        self.set_FM_taps(firdes.band_pass(1.0, self.samp_rate, 30, 15000, 10, window.WIN_HAMMING, 6.76))
        self.set_allpass_taps(firdes.band_pass(1.0, self.samp_rate, 1, 20000, 10, window.WIN_HAMMING, 6.76))
        self.set_gramophone_taps(firdes.band_pass(1.0, self.samp_rate, 160, 2000, 10, window.WIN_HAMMING, 6.76))
        self.set_nyq_freq(self.samp_rate/2)

    def get_wav_len(self):
        return self.wav_len

    def set_wav_len(self, wav_len):
        self.wav_len = wav_len

    def get_update(self):
        return self.update

    def set_update(self, update):
        self.update = update

    def get_select(self):
        return self.select

    def set_select(self, select):
        self.select = select
        self._select_callback(self.select)
        self.blocks_selector_0_0.set_input_index(self.select)

    def get_nyq_freq(self):
        return self.nyq_freq

    def set_nyq_freq(self, nyq_freq):
        self.nyq_freq = nyq_freq

    def get_noisy(self):
        return self.noisy

    def set_noisy(self, noisy):
        self.noisy = noisy
        self._noisy_callback(self.noisy)
        self.blocks_selector_1.set_input_index(self.noisy)

    def get_gramophone_taps(self):
        return self.gramophone_taps

    def set_gramophone_taps(self, gramophone_taps):
        self.gramophone_taps = gramophone_taps
        self.interp_fir_filter_xxx_0_0.set_taps(self.gramophone_taps)

    def get_gramophone_f2(self):
        return self.gramophone_f2

    def set_gramophone_f2(self, gramophone_f2):
        self.gramophone_f2 = gramophone_f2

    def get_gramophone_f1(self):
        return self.gramophone_f1

    def set_gramophone_f1(self, gramophone_f1):
        self.gramophone_f1 = gramophone_f1

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay

    def get_allpass_taps(self):
        return self.allpass_taps

    def set_allpass_taps(self, allpass_taps):
        self.allpass_taps = allpass_taps
        self.interp_fir_filter_xxx_0.set_taps(self.allpass_taps)

    def get_FM_taps(self):
        return self.FM_taps

    def set_FM_taps(self, FM_taps):
        self.FM_taps = FM_taps
        self.interp_fir_filter_xxx_0_0_0_0.set_taps(self.FM_taps)

    def get_FM_f2(self):
        return self.FM_f2

    def set_FM_f2(self, FM_f2):
        self.FM_f2 = FM_f2

    def get_FM_f1(self):
        return self.FM_f1

    def set_FM_f1(self, FM_f1):
        self.FM_f1 = FM_f1

    def get_AM_taps(self):
        return self.AM_taps

    def set_AM_taps(self, AM_taps):
        self.AM_taps = AM_taps
        self.interp_fir_filter_xxx_0_0_0.set_taps(self.AM_taps)

    def get_AM_f2(self):
        return self.AM_f2

    def set_AM_f2(self, AM_f2):
        self.AM_f2 = AM_f2

    def get_AM_f1(self):
        return self.AM_f1

    def set_AM_f1(self, AM_f1):
        self.AM_f1 = AM_f1




def main(top_block_cls=options, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
