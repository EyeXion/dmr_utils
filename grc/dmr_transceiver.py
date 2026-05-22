#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: dmr_transceiver
# Author: Elies, après des larmes de sang
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import dmr
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
from gnuradio import network
from gnuradio import soapy
import dmr_transceiver_epy_block_1 as epy_block_1  # embedded python block
import pmt
import sip


def snipfcn_snippet_0(self):
    import threading
    import time
    from subprocess import Popen


    def callback_dsd():
      Popen("nc -lu 52052 | dsd-fme   -Z -i - -Q ../../../../../../../tmp/out", shell=True)

    def callback_nc():
      Popen("alacritty -e \"bash -c 'nc -lu 52020'\"", shell=True)


    dsd_thread = threading.Thread(target=callback_dsd, daemon=True)
    dsd_thread.start()

    #nc_thread = threading.Thread(target=callback_nc, daemon=True)
    #nc_thread.start()


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)

class dmr_transceiver(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "dmr_transceiver", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("dmr_transceiver")
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

        self.settings = Qt.QSettings("GNU Radio", "dmr_transceiver")

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
        self.xlating_transition_bw = xlating_transition_bw = 3e3
        self.xlating_bw = xlating_bw = 16e3
        self.target_samp_rate = target_samp_rate = 48e3
        self.symbol_rate = symbol_rate = if_samp_rate / samples_per_symbol
        self.sps = sps = 125.0
        self.samp_rate = samp_rate = 1e6
        self.decim_xlating = decim_xlating = 1
        self.xlating_low_pass_taps = xlating_low_pass_taps = firdes.low_pass(1.0, samp_rate, xlating_bw/2,xlating_transition_bw, window.WIN_HAMMING, 6.76)
        self.tx_rrc_taps = tx_rrc_taps = firdes.root_raised_cosine(5, if_samp_rate,symbol_rate, 0.2, (25*samples_per_symbol))
        self.samp_per_symb = samp_per_symb = 10
        self.rx_port = rx_port = 52052
        self.offset = offset = 100e3
        self.low_pass_filter_taps_tx_resampler = low_pass_filter_taps_tx_resampler = firdes.low_pass(sps, samp_rate*3, 10000,3000, window.WIN_BLACKMAN, 6.76)
        self.interp_rate = interp_rate = int(int(target_samp_rate)/math.gcd(int(samp_rate/decim_xlating),int(target_samp_rate)))
        self.gain = gain = 40
        self.freq_dev = freq_dev = 648
        self.decim_rate = decim_rate = int(int(samp_rate/decim_xlating)/math.gcd(int(samp_rate/decim_xlating),int(target_samp_rate)))
        self.center_freq_tx = center_freq_tx = 433575000
        self.center_freq_rx = center_freq_rx = 433.57446e6

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
        self._center_freq_tx_range = qtgui.Range(425e6, 445e6, 1e3, 433575000, 200)
        self._center_freq_tx_win = qtgui.RangeWidget(self._center_freq_tx_range, self.set_center_freq_tx, "center_freq_tx", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._center_freq_tx_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._center_freq_rx_range = qtgui.Range(420.0e6, 450.0e6, 1, 433.57446e6, 200)
        self._center_freq_rx_win = qtgui.RangeWidget(self._center_freq_rx_range, self.set_center_freq_rx, "center_freq_rx", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._center_freq_rx_win, 2, 2, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.soapy_limesdr_source_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_limesdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_source_0.set_bandwidth(0, samp_rate)
        self.soapy_limesdr_source_0.set_frequency(0, (center_freq_rx + offset))
        self.soapy_limesdr_source_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_source_0.set_gain(0, min(max(50.0, -12.0), 61.0))
        self.soapy_limesdr_sink_0_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_limesdr_sink_0_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_sink_0_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_sink_0_0.set_bandwidth(0, 0.0)
        self.soapy_limesdr_sink_0_0.set_frequency(0, center_freq_tx)
        self.soapy_limesdr_sink_0_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_sink_0_0.set_gain(0, min(max(50, -12.0), 64.0))
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
        self.rational_resampler_xxx_0_0.set_max_output_buffer(1024)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=interp_rate,
                decimation=decim_rate,
                taps=[],
                fractional_bw=0)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            1024, #size
            48e3, #samp_rate
            "aaaaa", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


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
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0_0_2 = qtgui.time_sink_f(
            (2**10), #size
            samp_rate, #samp_rate
            'Raw Chunks', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_2.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_2.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_2.enable_tags(True)
        self.qtgui_time_sink_x_0_0_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_2.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_2.enable_grid(False)
        self.qtgui_time_sink_x_0_0_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_2.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0_2.enable_stem_plot(False)


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
                self.qtgui_time_sink_x_0_0_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_2_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_2_win)
        self.qtgui_time_sink_x_0_0_1 = qtgui.time_sink_c(
            (2**10), #size
            samp_rate, #samp_rate
            'After Selector', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_1.set_y_axis(-1, 5)

        self.qtgui_time_sink_x_0_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0_1.enable_stem_plot(False)


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
                    self.qtgui_time_sink_x_0_0_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_1_win)
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_c(
            (2**10), #size
            samp_rate, #samp_rate
            'Frequency Modulated', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(-1, 5)

        self.qtgui_time_sink_x_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0_0_0.enable_stem_plot(False)


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
                    self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_0_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            (2**10), #size
            samp_rate, #samp_rate
            'Frequency Modulated filtered', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 5)

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


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
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
            1024, #size
            target_samp_rate, #samp_rate
            "", #name
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
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            target_samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)



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
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_win)
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
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_short, 1, '127.0.0.1', rx_port, 0, 1024, True)
        self._gain_range = qtgui.Range((-12), 64, 1, 40, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "gain", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decim_xlating, xlating_low_pass_taps, (-offset), samp_rate)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(1, (1/samp_per_symb,)*samp_per_symb)
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.filter_delay_fc_0 = filter.filter_delay_fc(tx_rrc_taps)
        self.filter_delay_fc_0.set_max_output_buffer(8192)
        self.epy_block_1 = epy_block_1.blk()
        self.epy_block_1.set_max_output_buffer(8192)
        self.dmr_burst_source_0 = dmr.burst_source('127.0.0.1', 52010)
        self.dmr_burst_source_0.set_max_output_buffer(1024)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 32767)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0.set_max_output_buffer(8192)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(1.6)
        self.analog_frequency_modulator_fc_0_0 = analog.frequency_modulator_fc((2 * math.pi * freq_dev / (if_samp_rate * 0.5)))
        self.analog_frequency_modulator_fc_0_0.set_max_output_buffer(8192)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_frequency_modulator_fc_0_0, 0), (self.epy_block_1, 0))
        self.connect((self.analog_frequency_modulator_fc_0_0, 0), (self.qtgui_time_sink_x_0_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.analog_frequency_modulator_fc_0_0, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.network_udp_sink_0, 0))
        self.connect((self.dmr_burst_source_0, 0), (self.qtgui_time_sink_x_0_0_2, 0))
        self.connect((self.dmr_burst_source_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.epy_block_1, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.epy_block_1, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.filter_delay_fc_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.filter_delay_fc_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.qtgui_time_sink_x_0_0_1, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.soapy_limesdr_sink_0_0, 0))
        self.connect((self.soapy_limesdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "dmr_transceiver")
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
        self.analog_frequency_modulator_fc_0_0.set_sensitivity((2 * math.pi * self.freq_dev / (self.if_samp_rate * 0.5)))

    def get_xlating_transition_bw(self):
        return self.xlating_transition_bw

    def set_xlating_transition_bw(self, xlating_transition_bw):
        self.xlating_transition_bw = xlating_transition_bw
        self.set_xlating_low_pass_taps(firdes.low_pass(1.0, self.samp_rate, self.xlating_bw/2, self.xlating_transition_bw, window.WIN_HAMMING, 6.76))

    def get_xlating_bw(self):
        return self.xlating_bw

    def set_xlating_bw(self, xlating_bw):
        self.xlating_bw = xlating_bw
        self.set_xlating_low_pass_taps(firdes.low_pass(1.0, self.samp_rate, self.xlating_bw/2, self.xlating_transition_bw, window.WIN_HAMMING, 6.76))

    def get_target_samp_rate(self):
        return self.target_samp_rate

    def set_target_samp_rate(self, target_samp_rate):
        self.target_samp_rate = target_samp_rate
        self.set_decim_rate(int(int(self.samp_rate/self.decim_xlating)/math.gcd(int(self.samp_rate/self.decim_xlating),int(self.target_samp_rate))))
        self.set_interp_rate(int(int(self.target_samp_rate)/math.gcd(int(self.samp_rate/self.decim_xlating),int(self.target_samp_rate))))
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.target_samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.target_samp_rate)

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
        self.set_decim_rate(int(int(self.samp_rate/self.decim_xlating)/math.gcd(int(self.samp_rate/self.decim_xlating),int(self.target_samp_rate))))
        self.set_interp_rate(int(int(self.target_samp_rate)/math.gcd(int(self.samp_rate/self.decim_xlating),int(self.target_samp_rate))))
        self.set_low_pass_filter_taps_tx_resampler(firdes.low_pass(self.sps, self.samp_rate*3, 10000, 3000, window.WIN_BLACKMAN, 6.76))
        self.set_xlating_low_pass_taps(firdes.low_pass(1.0, self.samp_rate, self.xlating_bw/2, self.xlating_transition_bw, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_2.set_samp_rate(self.samp_rate)
        self.soapy_limesdr_sink_0_0.set_sample_rate(0, self.samp_rate)
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)
        self.soapy_limesdr_source_0.set_bandwidth(0, self.samp_rate)

    def get_decim_xlating(self):
        return self.decim_xlating

    def set_decim_xlating(self, decim_xlating):
        self.decim_xlating = decim_xlating
        self.set_decim_rate(int(int(self.samp_rate/self.decim_xlating)/math.gcd(int(self.samp_rate/self.decim_xlating),int(self.target_samp_rate))))
        self.set_interp_rate(int(int(self.target_samp_rate)/math.gcd(int(self.samp_rate/self.decim_xlating),int(self.target_samp_rate))))

    def get_xlating_low_pass_taps(self):
        return self.xlating_low_pass_taps

    def set_xlating_low_pass_taps(self, xlating_low_pass_taps):
        self.xlating_low_pass_taps = xlating_low_pass_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.xlating_low_pass_taps)

    def get_tx_rrc_taps(self):
        return self.tx_rrc_taps

    def set_tx_rrc_taps(self, tx_rrc_taps):
        self.tx_rrc_taps = tx_rrc_taps
        self.rational_resampler_xxx_0_0.set_taps(self.tx_rrc_taps)

    def get_samp_per_symb(self):
        return self.samp_per_symb

    def set_samp_per_symb(self, samp_per_symb):
        self.samp_per_symb = samp_per_symb
        self.fir_filter_xxx_0.set_taps((1/self.samp_per_symb,)*self.samp_per_symb)

    def get_rx_port(self):
        return self.rx_port

    def set_rx_port(self, rx_port):
        self.rx_port = rx_port

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((-self.offset))
        self.soapy_limesdr_source_0.set_frequency(0, (self.center_freq_rx + self.offset))

    def get_low_pass_filter_taps_tx_resampler(self):
        return self.low_pass_filter_taps_tx_resampler

    def set_low_pass_filter_taps_tx_resampler(self, low_pass_filter_taps_tx_resampler):
        self.low_pass_filter_taps_tx_resampler = low_pass_filter_taps_tx_resampler
        self.rational_resampler_xxx_1.set_taps(self.low_pass_filter_taps_tx_resampler)

    def get_interp_rate(self):
        return self.interp_rate

    def set_interp_rate(self, interp_rate):
        self.interp_rate = interp_rate

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_freq_dev(self):
        return self.freq_dev

    def set_freq_dev(self, freq_dev):
        self.freq_dev = freq_dev
        self.analog_frequency_modulator_fc_0_0.set_sensitivity((2 * math.pi * self.freq_dev / (self.if_samp_rate * 0.5)))

    def get_decim_rate(self):
        return self.decim_rate

    def set_decim_rate(self, decim_rate):
        self.decim_rate = decim_rate

    def get_center_freq_tx(self):
        return self.center_freq_tx

    def set_center_freq_tx(self, center_freq_tx):
        self.center_freq_tx = center_freq_tx
        self.soapy_limesdr_sink_0_0.set_frequency(0, self.center_freq_tx)

    def get_center_freq_rx(self):
        return self.center_freq_rx

    def set_center_freq_rx(self, center_freq_rx):
        self.center_freq_rx = center_freq_rx
        self.soapy_limesdr_source_0.set_frequency(0, (self.center_freq_rx + self.offset))




def main(top_block_cls=dmr_transceiver, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    snippets_main_after_init(tb)
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
