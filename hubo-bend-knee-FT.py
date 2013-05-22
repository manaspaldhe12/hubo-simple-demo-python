#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2013, Daniel M. Lofaro
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# */



import hubo_ach as ha
import ach
import sys
import time
from ctypes import *

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
s.flush()
r.flush()

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

g = 0.4
kz = 0.28


imax = 10
delta = g/imax
for i in range(1, imax):
  ref.ref[ha.RAP] = -delta*i
  ref.ref[ha.LAP] = ref.ref[ha.RAP]
  ref.ref[ha.RKN] = 2*delta*i
  ref.ref[ha.LKN] = ref.ref[ha.RKN]
  ref.ref[ha.RHP] = -delta*i
  ref.ref[ha.LHP] = ref.ref[ha.RHP]

  r.put(ref)
  time.sleep(0.1)

d = 0.0
L = 5.0
while True:

  # Get the current feed-forward (state) 
  [statuss, framesizes] = s.get(state, wait=False, last=False)
  ft = (state.ft[ha.HUBO_FT_R_FOOT].f_z + state.ft[ha.HUBO_FT_L_FOOT].f_z)/2.0/200.0
  dt = kz*ft
  d = (d*(L-1.0)+dt)/L

  if d > 0.4: 
    d = 0.4
  if d < -0.4:
    d = -0.4




  ref.ref[ha.RAP] = -(g+d)
  ref.ref[ha.LAP] = ref.ref[ha.RAP]
  ref.ref[ha.RKN] = 2*(g+d)
  ref.ref[ha.LKN] = ref.ref[ha.RKN]
  ref.ref[ha.RHP] = ref.ref[ha.RAP]
  ref.ref[ha.LHP] = ref.ref[ha.RHP]

#  ref.ref[ha.REB] = g + ky*state.ft[ha.HUBO_FT_R_HAND].m_y
  print 'New Ref: ', ref.ref[ha.RKN], ' d = ', d, ' dt = ', dt

  # Write to the feed-forward channel
  r.put(ref)

  time.sleep(0.05)  

# Close the connection to the channels
r.close()
s.close()

