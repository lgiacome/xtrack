import numpy as np
import xtrack as xt

line = xt.Line.from_json('../../test_data/hllhc15_thick/lhc_thick_with_knobs.json')
line.vars['vrf400'] = 16
line.vars['lagrf400.b1'] = 0.5

# line.vars['acbh22.l7b1'] = 10e-6
line.vars['acbv21.l7b1'] = 10e-6

ele_cut = ['ip1', 'ip2', 'ip3', 'ip4', 'ip5', 'ip6', 'ip7']

ele_cut_ext = ele_cut.copy()
if line.element_names[0] not in ele_cut_ext:
    ele_cut_ext.insert(0, line.element_names[0])
if line.element_names[-1] not in ele_cut_ext:
    ele_cut_ext.append(line.element_names[-1])

ele_cut_sorted = []
for ee in line.element_names:
    if ee in ele_cut_ext:
        ele_cut_sorted.append(ee)

elements_map_line = []
names_map_line = []
tw = line.twiss()

for ii in range(len(ele_cut_sorted)-1):
    names_map_line.append(ele_cut_sorted[ii])
    elements_map_line.append(line[ele_cut_sorted[ii]])

    smap = xt.SecondOrderTaylorMap.from_line(
                            line, ele_start=ele_cut_sorted[ii],
                            ele_stop=ele_cut_sorted[ii+1],
                            twiss_table=tw)
    names_map_line.append(f'map_{ii}')
    elements_map_line.append(smap)

names_map_line.append(ele_cut_sorted[-1])
elements_map_line.append(line[ele_cut_sorted[-1]])

line_maps = xt.Line(elements=elements_map_line, element_names=names_map_line)
line_maps.particle_ref = line.particle_ref.copy()

tw = line.twiss()
tw_map = line_maps.twiss()

assert np.isclose(np.mod(tw_map.qx, 1), np.mod(tw.qx, 1), rtol=0, atol=1e-7)
assert np.isclose(np.mod(tw_map.qy, 1), np.mod(tw.qy, 1), rtol=0, atol=1e-7)
assert np.isclose(tw_map.dqx, tw.dqx, rtol=0, atol=1e-3)
assert np.isclose(tw_map.dqy, tw.dqy, rtol=0, atol=1e-3)
assert np.isclose(tw_map.c_minus, tw.c_minus, rtol=0, atol=1e-5)

assert np.allclose(tw_map.rows[ele_cut].s, tw.rows[ele_cut].s, rtol=0, atol=1e-12)

assert np.allclose(tw_map.rows[ele_cut].x, tw.rows[ele_cut].x, rtol=0, atol=1e-12)
assert np.allclose(tw_map.rows[ele_cut].px, tw.rows[ele_cut].px, rtol=0, atol=1e-12)
assert np.allclose(tw_map.rows[ele_cut].y, tw.rows[ele_cut].y, rtol=0, atol=1e-12)
assert np.allclose(tw_map.rows[ele_cut].py, tw.rows[ele_cut].py, rtol=0, atol=1e-12)
assert np.allclose(tw_map.rows[ele_cut].zeta, tw.rows[ele_cut].zeta, rtol=0, atol=1e-10)
assert np.allclose(tw_map.rows[ele_cut].delta, tw.rows[ele_cut].delta, rtol=0, atol=1e-12)

assert np.allclose(tw_map.rows[ele_cut].betx, tw.rows[ele_cut].betx, rtol=1e-5, atol=0)
assert np.allclose(tw_map.rows[ele_cut].alfx, tw.rows[ele_cut].alfx, rtol=1e-5, atol=1e-6)
assert np.allclose(tw_map.rows[ele_cut].bety, tw.rows[ele_cut].bety, rtol=1e-5, atol=0)
assert np.allclose(tw_map.rows[ele_cut].alfy, tw.rows[ele_cut].alfy, rtol=1e-5, atol=1e-6)