import numpy as np

import xtrack as xt
import xpart as xp
import xdeps as xd

import matplotlib.pyplot as plt

line = xt.Line.from_json('psb_00_from_mad.json')
line.build_tracker()
line.twiss_default['method'] = '4d'

tw0 = line.twiss()

# inspect a bit...
tw0.qx, tw0.qy

# A few checks on the imported model
line.vars['k0bi1bsw1l11']._info() # Check that the knob controls k0 and the edges

line.element_refs['bi1.bsw1l1.1'].h._info() # Check no reference system curvature
line.element_refs['bi1.bsw1l1.1_den'].r21._info() # Check no horizontal edge focusing

# Build chicane knob (k0)
line.vars['bsw_k0l_ref'] = 6.6e-2
line.vars['on_chicane'] = 0

line.vars['k0bi1bsw1l11'] = (line.vars['on_chicane'] * line.vars['bsw_k0l_ref']
                             / line['bi1.bsw1l1.1'].length)
line.vars['k0bi1bsw1l12'] = (-line.vars['on_chicane'] * line.vars['bsw_k0l_ref']
                                / line['bi1.bsw1l1.2'].length)
line.vars['k0bi1bsw1l13'] = (-line.vars['on_chicane'] * line.vars['bsw_k0l_ref']
                                / line['bi1.bsw1l1.3'].length)
line.vars['k0bi1bsw1l14'] = (line.vars['on_chicane'] * line.vars['bsw_k0l_ref']
                                / line['bi1.bsw1l1.4'].length)
# Inspect:
line.vars['k0bi1bsw1l11']._info()

# Match tunes (with chicane off)
line.match(
    targets=[
        xt.Target('qx',  4.4, tol=1e-6),
        xt.Target('qy',  4.45, tol=1e-6)],
    vary=[
        xt.Vary('kbrqf', step=1e-5),
        xt.Vary('kbrqd', step=1e-5)],
)

# Inspect bump and induced beta beating for different bump amplitudes
plt.close('all')

chicane_values = np.linspace(0, 1, 5)
fig1 = plt.figure(1)
sp1 = plt.subplot(3,1,1)
sp2 = plt.subplot(3,1,2, sharex=sp1)
sp3 = plt.subplot(3,1,3, sharex=sp1)

colors = plt.cm.rainbow(np.linspace(0,1,len(chicane_values)))

for ii, vv in enumerate(chicane_values[::-1]):
    line.vars['on_chicane'] = vv
    tw = line.twiss()

    sp1.plot(tw.s, tw.x, color=colors[ii])
    sp2.plot(tw.s, tw.betx, color=colors[ii])
    sp3.plot(tw.s, tw.bety, color=colors[ii])

sp1.set_ylabel('x [m]')
sp2.set_ylabel('betx [m]')
sp3.set_ylabel('bety [m]')
sp3.set_xlabel('s [m]')

line.vars['on_chicane'] = 1

# Match beta beating correction knob

# Add a marker to the line
line.discard_tracker()
line.insert_element(element=xt.Marker(), name='marker_for_match', at_s=80.)
line.build_tracker()
line.vars['on_chicane'] = 0
tw_nochicane = line.twiss()

line.vars['on_chicane'] =  1
line.match_knob('on_chicane_betabeat_corr',
    knob_value_start=0,
    knob_value_end=1,
    vary=[
        xt.Vary('kbrqd3corr', step=1e-5),
        xt.Vary('kbrqd14corr', step=1e-5),
    ],
    targets = [
        xt.Target('bety', at='marker_for_match',
                    value=tw_nochicane['bety', 'marker_for_match'], tol=1e-4, scale=1),
        xt.Target('alfy', at='marker_for_match',
                    value=tw_nochicane['alfy', 'marker_for_match'], tol=1e-4, scale=1)
    ])

plt.show()

