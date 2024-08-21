import xtrack as xt
import numpy as np

line = xt.Line.from_json('../../test_data/hllhc15_thick/lhc_thick_with_knobs.json')
line.twiss_default.update({'strengths': False, 'method': '4d'})
tw0 = line.twiss()

tt = line.get_table()

obs_points = tt.rows['bpm.*'].name
corr_names = line.vars.get_table().rows['kq.*.b1'].name

response_matrix = np.zeros((len(obs_points), len(corr_names)))

dk = 0.5e-5
for ii, nn in enumerate(corr_names):
    print(f'Processing {ii}/{len(corr_names)}')
    line.vars[nn] += dk
    twp = line.twiss()
    for jj, mm in enumerate(obs_points):
        response_matrix[jj, ii] = (twp['betx', mm] - tw0['betx', mm]) / dk
    line.vars[nn] -= dk

line.vars['kq7.r5b1'] *= 1.01
tw = line.twiss()

tw['betx0'] = tw0['betx']
tw['bety0'] = tw0['bety']
tw['mux0'] = tw0['mux']
tw['muy0'] = tw0['muy']

from xtrack.trajectory_correction import _compute_correction

betx_err = tw.rows[obs_points].betx - tw0.rows[obs_points].betx

correction_svd = _compute_correction(betx_err, response_matrix, rcond=1e-3)
correction_micado = _compute_correction(betx_err, response_matrix, n_micado=1)

i_micado = np.argmax(np.abs(correction_micado))
print(f'MICADO correction: {correction_micado[i_micado]:.2e} at {corr_names[i_micado]}')

import matplotlib.pyplot as plt
plt.close('all')
plt.figure(1)
plt.plot(correction_svd, '.', label='SVD')
plt.plot(correction_micado, '.', label='MICADO')

plt.legend()
plt.show()