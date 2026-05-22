#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: dmr_cleann
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
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
from gnuradio import soapy
import dmr_cleann_epy_block_0 as epy_block_0  # embedded python block
import dmr_cleann_epy_block_1_0 as epy_block_1_0  # embedded python block
import sip



class dmr_cleann(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "dmr_cleann", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("dmr_cleann")
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

        self.settings = Qt.QSettings("GNU Radio", "dmr_cleann")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samples_per_symbol = samples_per_symbol = 5
        self.if_samp_rate = if_samp_rate = 24000.0
        self.symbol_rate = symbol_rate = if_samp_rate / samples_per_symbol
        self.sps = sps = 125.0
        self.samp_rate = samp_rate = 1e6
        self.preamble_symbols = preamble_symbols = 2
        self.num_silence_slots = num_silence_slots = 1
        self.hex_words = hex_words = [1757267730907742830085168796217001194752813194112263741422447119562445457171871]*30
        self.tx_symbols = tx_symbols = sum([[4]*preamble_symbols + [int(bin(h)[2:].zfill(264)[i:i+2], 2) for i in range(0, 264, 2)] + [4]*(156 * num_silence_slots - preamble_symbols) for h in hex_words], [])
        self.tx_rrc_taps = tx_rrc_taps = firdes.root_raised_cosine(5, if_samp_rate,symbol_rate, 0.2, (25*samples_per_symbol))
        self.postamble_symbols = postamble_symbols = 2
        self.mult_const = mult_const = 1
        self.low_pass_filter_taps_tx_resampler = low_pass_filter_taps_tx_resampler = firdes.low_pass(sps, samp_rate*3, 10000,3000, window.WIN_BLACKMAN, 6.76)
        self.hex_words_sonnette = hex_words_sonnette = [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3]
        self.freq_dev = freq_dev = 648
        self.center_freq = center_freq = 433575000

        ##################################################
        # Blocks
        ##################################################

        self._freq_dev_range = qtgui.Range(500, 200000, 1, 648, 200)
        self._freq_dev_win = qtgui.RangeWidget(self._freq_dev_range, self.set_freq_dev, "freq_dev", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._freq_dev_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._center_freq_range = qtgui.Range(425e6, 445e6, 1e3, 433575000, 200)
        self._center_freq_win = qtgui.RangeWidget(self._center_freq_range, self.set_center_freq, "center_freq", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._center_freq_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.soapy_limesdr_sink_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_limesdr_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_sink_0.set_bandwidth(0, 0.0)
        self.soapy_limesdr_sink_0.set_frequency(0, center_freq)
        self.soapy_limesdr_sink_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_sink_0.set_gain(0, min(max(50, -12.0), 64.0))
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=int(sps),
                decimation=3,
                taps=low_pass_filter_taps_tx_resampler,
                fractional_bw=0)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=samples_per_symbol,
                decimation=1,
                taps=tx_rrc_taps,
                fractional_bw=0)
        self.qtgui_time_sink_x_0_1 = qtgui.time_sink_f(
            (208*132), #size
            samp_rate, #samp_rate
            'Demod', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1.enable_control_panel(True)
        self.qtgui_time_sink_x_0_1.enable_stem_plot(False)


        labels = ['Demodulated Symbols', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [2, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [0, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_1_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            (2**15), #size
            samp_rate, #samp_rate
            'Raw Chunks', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


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
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            (2**15), #size
            samp_rate, #samp_rate
            'Tx Signal', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
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


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



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
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(1, firdes.root_raised_cosine(1.0, samp_rate, samp_rate/240, 0.2, 11*240))
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.filter_delay_fc_0 = filter.filter_delay_fc(tx_rrc_taps)
        self.filter_delay_fc_0.set_max_output_buffer(8192)
        self.epy_block_1_0 = epy_block_1_0.blk()
        self.epy_block_0 = epy_block_0.blk(num_silence_slots=num_silence_slots, preamble_symbols=preamble_symbols, postamble_symbols=postamble_symbols)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf([0.5, 1.5, -0.5, -1.5, 0], 1)
        self.blocks_vector_source_x_0 = blocks.vector_source_b(tx_symbols, True, 1, [])
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0.set_max_output_buffer(8192)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((samp_rate / (2 * math.pi * freq_dev)))
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc((2 * math.pi * freq_dev / (if_samp_rate * 0.5)))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.epy_block_1_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.epy_block_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.epy_block_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.epy_block_1_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.filter_delay_fc_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_0_1, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.filter_delay_fc_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.soapy_limesdr_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "dmr_cleann")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samples_per_symbol(self):
        return self.samples_per_symbol

    def set_samples_per_symbol(self, samples_per_symbol):
        self.samples_per_symbol = samples_per_symbol
        self.set_symbol_rate(self.if_samp_rate / self.samples_per_symbol)
        self.set_tx_rrc_taps(firdes.root_raised_cosine(5, self.if_samp_rate, self.symbol_rate, 0.2, (25*self.samples_per_symbol)))

    def get_if_samp_rate(self):
        return self.if_samp_rate

    def set_if_samp_rate(self, if_samp_rate):
        self.if_samp_rate = if_samp_rate
        self.set_symbol_rate(self.if_samp_rate / self.samples_per_symbol)
        self.set_tx_rrc_taps(firdes.root_raised_cosine(5, self.if_samp_rate, self.symbol_rate, 0.2, (25*self.samples_per_symbol)))
        self.analog_frequency_modulator_fc_0.set_sensitivity((2 * math.pi * self.freq_dev / (self.if_samp_rate * 0.5)))

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_tx_rrc_taps(firdes.root_raised_cosine(5, self.if_samp_rate, self.symbol_rate, 0.2, (25*self.samples_per_symbol)))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_low_pass_filter_taps_tx_resampler(firdes.low_pass(self.sps, self.samp_rate*3, 10000, 3000, window.WIN_BLACKMAN, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_low_pass_filter_taps_tx_resampler(firdes.low_pass(self.sps, self.samp_rate*3, 10000, 3000, window.WIN_BLACKMAN, 6.76))
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate / (2 * math.pi * self.freq_dev)))
        self.fir_filter_xxx_0.set_taps(firdes.root_raised_cosine(1.0, self.samp_rate, self.samp_rate/240, 0.2, 11*240))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_1.set_samp_rate(self.samp_rate)
        self.soapy_limesdr_sink_0.set_sample_rate(0, self.samp_rate)

    def get_preamble_symbols(self):
        return self.preamble_symbols

    def set_preamble_symbols(self, preamble_symbols):
        self.preamble_symbols = preamble_symbols
        self.set_tx_symbols(sum([[4]*self.preamble_symbols + [int(bin(h)[2:].zfill(264)[i:i+2], 2) for i in range(0, 264, 2)] + [4]*(156 * self.num_silence_slots - self.preamble_symbols) for h in self.hex_words], []))
        self.epy_block_0.preamble_symbols = self.preamble_symbols

    def get_num_silence_slots(self):
        return self.num_silence_slots

    def set_num_silence_slots(self, num_silence_slots):
        self.num_silence_slots = num_silence_slots
        self.set_tx_symbols(sum([[4]*self.preamble_symbols + [int(bin(h)[2:].zfill(264)[i:i+2], 2) for i in range(0, 264, 2)] + [4]*(156 * self.num_silence_slots - self.preamble_symbols) for h in self.hex_words], []))
        self.epy_block_0.num_silence_slots = self.num_silence_slots

    def get_hex_words(self):
        return self.hex_words

    def set_hex_words(self, hex_words):
        self.hex_words = hex_words
        self.set_tx_symbols(sum([[4]*self.preamble_symbols + [int(bin(h)[2:].zfill(264)[i:i+2], 2) for i in range(0, 264, 2)] + [4]*(156 * self.num_silence_slots - self.preamble_symbols) for h in self.hex_words], []))

    def get_tx_symbols(self):
        return self.tx_symbols

    def set_tx_symbols(self, tx_symbols):
        self.tx_symbols = tx_symbols
        self.blocks_vector_source_x_0.set_data(self.tx_symbols, [])

    def get_tx_rrc_taps(self):
        return self.tx_rrc_taps

    def set_tx_rrc_taps(self, tx_rrc_taps):
        self.tx_rrc_taps = tx_rrc_taps
        self.rational_resampler_xxx_0_0.set_taps(self.tx_rrc_taps)

    def get_postamble_symbols(self):
        return self.postamble_symbols

    def set_postamble_symbols(self, postamble_symbols):
        self.postamble_symbols = postamble_symbols
        self.epy_block_0.postamble_symbols = self.postamble_symbols

    def get_mult_const(self):
        return self.mult_const

    def set_mult_const(self, mult_const):
        self.mult_const = mult_const

    def get_low_pass_filter_taps_tx_resampler(self):
        return self.low_pass_filter_taps_tx_resampler

    def set_low_pass_filter_taps_tx_resampler(self, low_pass_filter_taps_tx_resampler):
        self.low_pass_filter_taps_tx_resampler = low_pass_filter_taps_tx_resampler
        self.rational_resampler_xxx_1.set_taps(self.low_pass_filter_taps_tx_resampler)

    def get_hex_words_sonnette(self):
        return self.hex_words_sonnette

    def set_hex_words_sonnette(self, hex_words_sonnette):
        self.hex_words_sonnette = hex_words_sonnette

    def get_freq_dev(self):
        return self.freq_dev

    def set_freq_dev(self, freq_dev):
        self.freq_dev = freq_dev
        self.analog_frequency_modulator_fc_0.set_sensitivity((2 * math.pi * self.freq_dev / (self.if_samp_rate * 0.5)))
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate / (2 * math.pi * self.freq_dev)))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.soapy_limesdr_sink_0.set_frequency(0, self.center_freq)




def main(top_block_cls=dmr_cleann, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

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
