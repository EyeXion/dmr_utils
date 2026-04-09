/* -*- c++ -*- */
/*
 * Copyright 2026 gr-dmr author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "iq_selector_impl.h"
#include <gnuradio/io_signature.h>
#include <cstring>
#include <algorithm> 
#include <iostream>

namespace gr {
namespace dmr {

iq_selector::sptr
iq_selector::make(float noise_amp)
{
    return gnuradio::make_block_sptr<iq_selector_impl>(noise_amp);
}

iq_selector_impl::iq_selector_impl(float noise_amp)
    : gr::block("iq_selector",
                gr::io_signature::make(2, 2, sizeof(gr_complex)),
                gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_noise_amp(noise_amp),
      d_is_transmitting(false),
      d_sob_key(pmt::mp("tx_sob")),
      d_eob_key(pmt::mp("tx_eob"))
{}

iq_selector_impl::~iq_selector_impl() {}

void iq_selector_impl::forecast(int noutput_items, gr_vector_int &ninput_items_required)
{
    ninput_items_required[0] = 0; 
    ninput_items_required[1] = 1; 
}

int iq_selector_impl::general_work(int noutput_items,
                                   gr_vector_int &ninput_items,
                                   gr_vector_const_void_star &input_items,
                                   gr_vector_void_star &output_items)
{
    const gr_complex *in_data = (const gr_complex *)input_items[0];
    const gr_complex *in_noise = (const gr_complex *)input_items[1];
    gr_complex *out = (gr_complex *)output_items[0];

    int n_data_available = ninput_items[0];
    int n_noise_available = ninput_items[1];

    std::vector<tag_t> tags;
    get_tags_in_window(tags, 0, 0, n_data_available);

    int n_to_produce = std::min({noutput_items, n_noise_available, 512});
    if (n_to_produce <= 0) return 0;

    if (!d_is_transmitting) {
        bool sob_found = false;
        uint64_t sob_rel_offset = 0;

        for (auto &tag : tags) {
            if (pmt::eq(tag.key, d_sob_key)) {
                sob_found = true;
                sob_rel_offset = tag.offset - nitems_read(0);
                break; 
            }
        }

        if (sob_found) {
            if (sob_rel_offset > 0) {
                consume(0, sob_rel_offset);
            }
            
            d_is_transmitting = true;
            
            return 0; 
        } else {
            for (int i = 0; i < n_to_produce; i++) out[i] = in_noise[i] * d_noise_amp;
            
            int n_to_consume_data = std::min(n_to_produce, n_data_available);
            consume(0, n_to_consume_data);
            
            consume(1, n_to_produce);
            return n_to_produce;
        }

    } else {
        bool eob_found = false;
        uint64_t eob_rel_offset = 0;

        for (auto &tag : tags) {
            if (pmt::eq(tag.key, d_eob_key)) {
                eob_found = true;
                eob_rel_offset = tag.offset - nitems_read(0);
                break;
            }
        }

        int n_to_copy = std::min(n_to_produce, n_data_available);
        if (n_to_copy <= 0) return 0; // Wait for data to catch up

        if (eob_found && eob_rel_offset < (uint64_t)n_to_copy) {
            int burst_size = (int)eob_rel_offset + 1;
            std::memcpy(out, in_data, burst_size * sizeof(gr_complex));
            consume(0, burst_size);
            consume(1, burst_size);
            d_is_transmitting = false;
            return burst_size;
        } 

        std::memcpy(out, in_data, n_to_copy * sizeof(gr_complex));
        consume(0, n_to_copy);
        consume(1, n_to_copy);
        return n_to_copy;
    }
}


} // namespace dmr
} // namespace gr
