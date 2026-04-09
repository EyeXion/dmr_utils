/* -*- c++ -*- */
/*
 * Copyright 2026 gr-dmr author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DMR_IQ_SELECTOR_IMPL_H
#define INCLUDED_DMR_IQ_SELECTOR_IMPL_H

#include <gnuradio/dmr/iq_selector.h>

namespace gr {
namespace dmr {

class iq_selector_impl : public iq_selector
{
private:
    float d_noise_amp;
    bool d_is_transmitting;
    const pmt::pmt_t d_sob_key;
    const pmt::pmt_t d_eob_key;

public:
    iq_selector_impl(float noise_amp);
    ~iq_selector_impl();

    // Mandatory for gr::block
    void forecast(int noutput_items, gr_vector_int &ninput_items_required) override;

    // Mandatory for gr::block
    int general_work(int noutput_items,
                     gr_vector_int &ninput_items,
                     gr_vector_const_void_star &input_items,
                     gr_vector_void_star &output_items) override;
};

} // namespace dmr
} // namespace gr

#endif
