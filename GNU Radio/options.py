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
from PyQt5 import QtCore
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
import numpy as np
import sip
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
        self.choose_filter = choose_filter = [20,20000]
        self.wow_fc = wow_fc = 1.3
        self.wow_depth = wow_depth = 1/120
        self.update = update = .1
        self.noisy = noisy = 0
        self.flutter_fc = flutter_fc = 10
        self.flutter_depth = flutter_depth = .008
        self.filter_taps = filter_taps = firdes.band_pass(1.0, samp_rate, choose_filter[0], choose_filter[1], 20, window.WIN_HAMMING, 6.76)
        self.choose_effect = choose_effect = 0

        ##################################################
        # Blocks
        ##################################################

        self._wow_fc_range = qtgui.Range(0, 6, .1, 1.3, 200)
        self._wow_fc_win = qtgui.RangeWidget(self._wow_fc_range, self.set_wow_fc, "Wow Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._wow_fc_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._wow_depth_range = qtgui.Range(0, .02, .0001, 1/120, 200)
        self._wow_depth_win = qtgui.RangeWidget(self._wow_depth_range, self.set_wow_depth, "'Wow' Depth", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._wow_depth_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        _noisy_check_box = Qt.QCheckBox("Noisy")
        self._noisy_choices = {True: 1, False: 0}
        self._noisy_choices_inv = dict((v,k) for k,v in self._noisy_choices.items())
        self._noisy_callback = lambda i: Qt.QMetaObject.invokeMethod(_noisy_check_box, "setChecked", Qt.Q_ARG("bool", self._noisy_choices_inv[i]))
        self._noisy_callback(self.noisy)
        _noisy_check_box.stateChanged.connect(lambda i: self.set_noisy(self._noisy_choices[bool(i)]))
        self.top_grid_layout.addWidget(_noisy_check_box, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._flutter_fc_range = qtgui.Range(6, 100, 1, 10, 200)
        self._flutter_fc_win = qtgui.RangeWidget(self._flutter_fc_range, self.set_flutter_fc, "Flutter Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._flutter_fc_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._flutter_depth_range = qtgui.Range(0, .02, .0001, .008, 200)
        self._flutter_depth_win = qtgui.RangeWidget(self._flutter_depth_range, self.set_flutter_depth, "'Flutter' Depth", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._flutter_depth_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._choose_effect_options = [0, 1, 2]
        # Create the labels list
        self._choose_effect_labels = ['None', 'Wow', 'Flutter']
        # Create the combo box
        self._choose_effect_tool_bar = Qt.QToolBar(self)
        self._choose_effect_tool_bar.addWidget(Qt.QLabel("Effect" + ": "))
        self._choose_effect_combo_box = Qt.QComboBox()
        self._choose_effect_tool_bar.addWidget(self._choose_effect_combo_box)
        for _label in self._choose_effect_labels: self._choose_effect_combo_box.addItem(_label)
        self._choose_effect_callback = lambda i: Qt.QMetaObject.invokeMethod(self._choose_effect_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._choose_effect_options.index(i)))
        self._choose_effect_callback(self.choose_effect)
        self._choose_effect_combo_box.currentIndexChanged.connect(
            lambda i: self.set_choose_effect(self._choose_effect_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._choose_effect_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            256, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(update)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(False)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        self.qtgui_time_sink_x_0.disable_legend()

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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 3, 2, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(update)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(True)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 3, 0, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.mmse_resampler_xx_0_0 = filter.mmse_resampler_ff(0, 1)
        self.mmse_resampler_xx_0 = filter.mmse_resampler_ff(0, 1)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(1, filter_taps)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(4, [1,0,0,0])
        self.fir_filter_xxx_0.declare_sample_delay(0)
        # Create the options list
        self._choose_filter_options = [[20, 20000], [160, 2000], [200, 5000], [30, 15000], [30, 3000]]
        # Create the labels list
        self._choose_filter_labels = ['Original', 'Gramophone', 'AM', 'FM', 'Telephone']
        # Create the combo box
        self._choose_filter_tool_bar = Qt.QToolBar(self)
        self._choose_filter_tool_bar.addWidget(Qt.QLabel("Filter" + ": "))
        self._choose_filter_combo_box = Qt.QComboBox()
        self._choose_filter_tool_bar.addWidget(self._choose_filter_combo_box)
        for _label in self._choose_filter_labels: self._choose_filter_combo_box.addItem(_label)
        self._choose_filter_callback = lambda i: Qt.QMetaObject.invokeMethod(self._choose_filter_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._choose_filter_options.index(i)))
        self._choose_filter_callback(self.choose_filter)
        self._choose_filter_combo_box.currentIndexChanged.connect(
            lambda i: self.set_choose_filter(self._choose_filter_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._choose_filter_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\cmgra\\Desktop\\ECSE 351\\gnu_radio_music_antiquing\\GNU Radio\\Tomorrow_Is_Today_Billy_Joel.wav', False)
        self.blocks_wavfile_source_0.set_block_alias("song_source")
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,choose_effect,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(noisy)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(.1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_1_0 = audio.sink(samp_rate, '', True)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, flutter_fc, flutter_depth, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, wow_fc, wow_depth, 1, 0)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, .025, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.mmse_resampler_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.mmse_resampler_xx_0_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_selector_0, 0), (self.audio_sink_1_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.mmse_resampler_xx_0_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.mmse_resampler_xx_0_0, 0), (self.blocks_selector_0, 2))


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
        self.set_filter_taps(firdes.band_pass(1.0, self.samp_rate, self.choose_filter[0], self.choose_filter[1], 20, window.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_choose_filter(self):
        return self.choose_filter

    def set_choose_filter(self, choose_filter):
        self.choose_filter = choose_filter
        self._choose_filter_callback(self.choose_filter)
        self.set_filter_taps(firdes.band_pass(1.0, self.samp_rate, self.choose_filter[0], self.choose_filter[1], 20, window.WIN_HAMMING, 6.76))

    def get_wow_fc(self):
        return self.wow_fc

    def set_wow_fc(self, wow_fc):
        self.wow_fc = wow_fc
        self.analog_sig_source_x_0.set_frequency(self.wow_fc)

    def get_wow_depth(self):
        return self.wow_depth

    def set_wow_depth(self, wow_depth):
        self.wow_depth = wow_depth
        self.analog_sig_source_x_0.set_amplitude(self.wow_depth)

    def get_update(self):
        return self.update

    def set_update(self, update):
        self.update = update
        self.qtgui_freq_sink_x_0.set_update_time(self.update)
        self.qtgui_time_sink_x_0.set_update_time(self.update)

    def get_noisy(self):
        return self.noisy

    def set_noisy(self, noisy):
        self.noisy = noisy
        self._noisy_callback(self.noisy)
        self.blocks_multiply_const_vxx_0_0.set_k(self.noisy)

    def get_flutter_fc(self):
        return self.flutter_fc

    def set_flutter_fc(self, flutter_fc):
        self.flutter_fc = flutter_fc
        self.analog_sig_source_x_0_0.set_frequency(self.flutter_fc)

    def get_flutter_depth(self):
        return self.flutter_depth

    def set_flutter_depth(self, flutter_depth):
        self.flutter_depth = flutter_depth
        self.analog_sig_source_x_0_0.set_amplitude(self.flutter_depth)

    def get_filter_taps(self):
        return self.filter_taps

    def set_filter_taps(self, filter_taps):
        self.filter_taps = filter_taps
        self.interp_fir_filter_xxx_0.set_taps(self.filter_taps)

    def get_choose_effect(self):
        return self.choose_effect

    def set_choose_effect(self, choose_effect):
        self.choose_effect = choose_effect
        self._choose_effect_callback(self.choose_effect)
        self.blocks_selector_0.set_input_index(self.choose_effect)




def main(top_block_cls=options, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        gr.logger("realtime").warn("Error: failed to enable real-time scheduling.")

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
