/* -*- c++ -*- */
/*
 * Copyright 2026 gr-dmr author.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DMR_IQ_SELECTOR_H
#define INCLUDED_DMR_IQ_SELECTOR_H

#include <gnuradio/dmr/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace dmr {

    /*!
     * \brief <+description of block+>
     * \ingroup dmr
     *
     */
    class DMR_API iq_selector : virtual public gr::block
    {
     public:
      typedef std::shared_ptr<iq_selector> sptr;

      static sptr make(float noise_amp);
    };

  } // namespace dmr
} // namespace gr

#endif /* INCLUDED_DMR_IQ_SELECTOR_H */
