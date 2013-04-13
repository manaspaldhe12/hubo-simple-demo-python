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

from optparse import OptionParser
import select
from datetime import date


if __name__=='__main__':

  # Open Hubo-Ach feed-forward and feed-back (reference and state) channels
  s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
  r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
  fs = ach.Channel(ha.HUBO_CHAN_VIRTUAL_FROM_SIM_NAME)
  s.flush()
  r.flush()
  fs.flush()
  RT = False


  # feed-forward will now be refered to as "state"
  state = ha.HUBO_STATE()

  # feed-back will now be refered to as "ref"
  ref = ha.HUBO_REF()
  sim = ha.HUBO_VIRTUAL()

  # Get file name
  exten = ".traj"

  parser = OptionParser()
  (options, args) = parser.parse_args()
  try:
    filename = args[0]
  except:
    thetime = time.time()
    dt = date.fromtimestamp(thetime).isocalendar()
    filename = "recordOutput-" + str(dt[0]) + "-" + str(dt[1]) + "-" + str(dt[2]) + "-" + str(int(thetime))

  filename = filename + exten
  print "File Name set to ", filename 
  f = open(filename, 'w')
  print "file: ",f
  print "*** Recording ***"
  timei = 0;
  [statusr, framesizer] = r.get(ref, wait=False, last=True)
  r.put(ref)
  thold = 0.0
  firstTime = True
  stepTime = 1.0
  stepEnd = 5.0
  dontBreak = True
  while(dontBreak):
    # Wait for simtime
    if(RT==False):
      [statusfs, framesizefs] = fs.get(sim,wait=True, last=False)
    # Get the current feed-forward (state) 
    [statuss, framesizes] = s.get(state, wait=False, last=True)
    [statusr, framesizer] = r.get(ref, wait=False, last=True)

    if(firstTime == True):
      thold = state.time 
      firstTime = False 
    if((state.time - thold) >= stepTime):
      ref.ref[ha.RSP] = 0.4
      ref.mode[ha.RSP] = 1
      r.put(ref)


    # Print out the actual position of the LEB
  #  print "Time = ",state.time, " : WST = ", state.joint[ha.WST].pos
    data = [ (state.time - thold), ref.ref[ha.RSP], state.joint[ha.RSP].ref, state.joint[ha.RSP].pos]
    if(timei > 100):
      print data
      timei = 0
    else:
      timei = timei+1

    f.write(str(data)[1:-1]+'\n')
    if((state.time-thold) > stepEnd):
      dontBreak = False
      break

    # Write to the feed-forward channel
  #  r.put(ref)

  # Close the connection to the channels
  fs.close()
  r.close()
  s.close()

