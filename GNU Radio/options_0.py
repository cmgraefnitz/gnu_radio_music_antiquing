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
import options_0_epy_block_0 as epy_block_0  # embedded python block
import options_0_epy_block_1 as epy_block_1  # embedded python block
import sip
import threading



class options_0(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "options_0")

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
        self.variable_qtgui_toggle_switch_0 = variable_qtgui_toggle_switch_0 = 0
        self.update = update = .05
        self.select = select = 0
        self.nyq_freq = nyq_freq = samp_rate/2
        self.noisy = noisy = 0
        self.gramophone_f2 = gramophone_f2 = 2000
        self.gramophone_f1 = gramophone_f1 = 160
        self.delay = delay = 2
        self.FM_f2 = FM_f2 = 15000
        self.FM_f1 = FM_f1 = 30
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
        self._variable_qtgui_toggle_switch_0_choices = {'Pressed': 1, 'Released': 0}

        _variable_qtgui_toggle_switch_0_toggle_switch = qtgui.GrToggleSwitch(self.set_variable_qtgui_toggle_switch_0, '', self._variable_qtgui_toggle_switch_0_choices, False, "green", "gray", 4, 50, 1, 1, self, 'value')
        self.variable_qtgui_toggle_switch_0 = _variable_qtgui_toggle_switch_0_toggle_switch

        self.top_layout.addWidget(_variable_qtgui_toggle_switch_0_toggle_switch)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(update)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.epy_block_0 = epy_block_0.blk(snr=10, noise_offset=-40)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\cmgra\\Desktop\\ECSE 351\\gnu_radio_music_antiquing\\351 music antiquing\\Tomorrow_Is_Today_(original).wav', True)
        self.blocks_wavfile_source_0.set_block_alias("song_source1")
        self.blocks_selector_1 = blocks.selector(gr.sizeof_float*1,noisy,0)
        self.blocks_selector_1.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,select,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_noisy)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, delay)
        self.band_pass_filter_0_0_0 = filter.interp_fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                FM_f1,
                FM_f2,
                1,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0_0 = filter.interp_fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                AM_f1,
                AM_f2,
                1,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0 = filter.interp_fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                gramophone_f1,
                gramophone_f2,
                1,
                window.WIN_HAMMING,
                6.76))
        self.audio_sink_1_0 = audio.sink(samp_rate, '', True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.variable_qtgui_toggle_switch_0, 'state'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_selector_0, 2))
        self.connect((self.band_pass_filter_0_0_0, 0), (self.blocks_selector_0, 3))
        self.connect((self.blocks_delay_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.audio_sink_1_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.band_pass_filter_0_0_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.epy_block_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_selector_1, 1))
        self.connect((self.epy_block_1, 0), (self.blocks_selector_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "options_0")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_nyq_freq(self.samp_rate/2)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, self.gramophone_f1, self.gramophone_f2, 1, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.samp_rate, self.AM_f1, self.AM_f2, 1, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.samp_rate, self.FM_f1, self.FM_f2, 1, window.WIN_HAMMING, 6.76))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_wav_len(self):
        return self.wav_len

    def set_wav_len(self, wav_len):
        self.wav_len = wav_len

    def get_variable_qtgui_toggle_switch_0(self):
        return self.variable_qtgui_toggle_switch_0

    def set_variable_qtgui_toggle_switch_0(self, variable_qtgui_toggle_switch_0):
        self.variable_qtgui_toggle_switch_0 = variable_qtgui_toggle_switch_0

    def get_update(self):
        return self.update

    def set_update(self, update):
        self.update = update
        self.qtgui_time_sink_x_0.set_update_time(self.update)

    def get_select(self):
        return self.select

    def set_select(self, select):
        self.select = select
        self._select_callback(self.select)
        self.blocks_selector_0.set_input_index(self.select)

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

    def get_gramophone_f2(self):
        return self.gramophone_f2

    def set_gramophone_f2(self, gramophone_f2):
        self.gramophone_f2 = gramophone_f2
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, self.gramophone_f1, self.gramophone_f2, 1, window.WIN_HAMMING, 6.76))

    def get_gramophone_f1(self):
        return self.gramophone_f1

    def set_gramophone_f1(self, gramophone_f1):
        self.gramophone_f1 = gramophone_f1
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, self.gramophone_f1, self.gramophone_f2, 1, window.WIN_HAMMING, 6.76))

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_delay_0.set_dly(int(self.delay))

    def get_FM_f2(self):
        return self.FM_f2

    def set_FM_f2(self, FM_f2):
        self.FM_f2 = FM_f2
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.samp_rate, self.FM_f1, self.FM_f2, 1, window.WIN_HAMMING, 6.76))

    def get_FM_f1(self):
        return self.FM_f1

    def set_FM_f1(self, FM_f1):
        self.FM_f1 = FM_f1
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.samp_rate, self.FM_f1, self.FM_f2, 1, window.WIN_HAMMING, 6.76))

    def get_AM_f2(self):
        return self.AM_f2

    def set_AM_f2(self, AM_f2):
        self.AM_f2 = AM_f2
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.samp_rate, self.AM_f1, self.AM_f2, 1, window.WIN_HAMMING, 6.76))

    def get_AM_f1(self):
        return self.AM_f1

    def set_AM_f1(self, AM_f1):
        self.AM_f1 = AM_f1
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.samp_rate, self.AM_f1, self.AM_f2, 1, window.WIN_HAMMING, 6.76))




def main(top_block_cls=options_0, options=None):

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
