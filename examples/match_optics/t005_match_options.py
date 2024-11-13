import xtrack as xt
import numpy as np

line = xt.Line.from_json("../../test_data/hllhc15_thick/lhc_thick_with_knobs.json")

opt = line.match(
    start='mq.30l8.b1', end='mq.23l8.b1',
    betx=1, bety=1, y=0, py=0,
    vary=[xt.VaryList(['acbv30.l8b1', 'acbv28.l8b1',],
                    step=1e-10, limits=[-1e-3, 1e-3]),
          xt.VaryList(['acbv26.l8b1', 'acbv24.l8b1'],
                    step=1e-10, limits=[-1e-3, 1e-3], tag='mytag')],
    targets = [
        xt.TargetSet(y=3e-3, py=0, at='mb.b28l8.b1'),
        xt.TargetSet(y=0, py=0, at=xt.END)
    ])

# Check autogenerated tags
assert opt.targets[0].tag == 'mb.b28l8.b1_y'
assert opt.targets[1].tag == 'mb.b28l8.b1_py'
assert opt.targets[2].tag == 'END_y'
assert opt.targets[3].tag == 'END_py'

# Check target getitem
assert opt.targets[0] == opt.targets['mb.b28l8.b1_y']
assert opt.targets[1] == opt.targets['mb.b28l8.b1_py']
assert opt.targets[2] == opt.targets['END_y']
assert opt.targets[3] == opt.targets['END_py']

assert opt.targets['END.*'][0] is opt.targets[2]
assert opt.targets['END.*'][1] is opt.targets[3]

assert np.all(
    opt.targets.status(ret=True).tag == opt.target_status(ret=True).tag)

assert opt.vary['myt.*'][0] is opt.vary[2]
assert opt.vary['myt.*'][1] is opt.vary[3]
assert np.all(opt.vary.status(ret=True).tag == np.array(['', '', 'mytag', 'mytag']))
assert np.all(opt.vary.status(ret=True).tag == opt.vary_status(ret=True).tag)
assert np.all(opt.vary.status(ret=True).name == np.array(
    ['acbv30.l8b1', 'acbv28.l8b1', 'acbv26.l8b1', 'acbv24.l8b1']))

opt1 = opt.clone(name='opt1')
assert opt1.name == 'opt1'
assert str(opt1.targets[0]) == str(opt.targets[0])
assert str(opt1.targets[1]) == str(opt.targets[1])
assert str(opt1.targets[2]) == str(opt.targets[2])
assert str(opt1.targets[3]) == str(opt.targets[3])
assert str(opt1.vary[0]) == str(opt.vary[0])
assert str(opt1.vary[1]) == str(opt.vary[1])
assert str(opt1.vary[2]) == str(opt.vary[2])
assert str(opt1.vary[3]) == str(opt.vary[3])

opt2 = opt.clone(name='opt2', remove_vary=True)
assert len(opt2.vary) == 0
assert str(opt2.targets[0]) == str(opt.targets[0])
assert str(opt2.targets[1]) == str(opt.targets[1])
assert str(opt2.targets[2]) == str(opt.targets[2])
assert str(opt2.targets[3]) == str(opt.targets[3])

opt3 = opt.clone(name='opt3', remove_targets=True,
                 add_targets=[xt.TargetSet(y=3e-3, py=0, at='mb.b28l8.b1')])
assert len(opt3.targets) == 2
assert opt.targets[0].tag == 'mb.b28l8.b1_y'
assert opt.targets[1].tag == 'mb.b28l8.b1_py'
assert str(opt3.vary[0]) == str(opt.vary[0])
assert str(opt3.vary[1]) == str(opt.vary[1])
assert str(opt3.vary[2]) == str(opt.vary[2])
assert str(opt3.vary[3]) == str(opt.vary[3])

opt4 = opt.clone(name='opt4', remove_vary=True, remove_targets=False,
                    add_vary=xt.VaryList(['acbv30.l8b1', 'acbv28.l8b1']),
                    )
assert len(opt4.vary) == 2
assert opt.vary[0].name == 'acbv30.l8b1'
assert opt.vary[1].name == 'acbv28.l8b1'