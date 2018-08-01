import tikz

def draw_label(gen, box, label):
    vdiff = .2
    pos = ((box.ll[0] + box.ur[0]) * .5, box.ll[1] - vdiff)
    gen.text(pos, label)


def draw_arrow(gen, b0, b1):
    p0 = [b0.ur[0], (b0.ur[1] + b0.ll[1]) * .5]
    p1 = [b1.ll[0], (b1.ur[1] + b1.ll[1]) * .5]
    spacer = .1
    p0[0] += spacer
    p1[0] -= spacer
    if (p0[1] < p1[1]):
        p0[1] += spacer
        p1[1] -= spacer * .5
    else:
        p0[1] -= spacer
        p1[1] += spacer * .5
    arr = gen.arrow(p0, p1)
    lw = 1.2
    arr.attr.append('line width=%s' %(lw))


def divide(gen, rect, ndiv, ddir='vertical'):
    assert((ddir == 'vertical') or (ddir == 'horizontal'))
    # assume box is of size 1
    diff = 1.0 / (ndiv + 1)
    if ddir == 'vertical':
        diff = (diff, 0.0)
    else:
        diff = (0.0, diff)

    p0 = (rect.ll[0] + diff[0], rect.ll[1] + diff[1])
    p1 = (p0[0] + diff[1] * (ndiv + 1), p0[1] + diff[0] * (ndiv + 1))
    line = gen.line(p0, p1)

    for i in range(ndiv-1):
        line = gen.line((line.p0[0] + diff[0], line.p0[1] + diff[1]),
                        (line.p1[0] + diff[0], line.p1[1] + diff[1]))


gen = tikz.tikz_gen()
one = gen.rectangle((-.5, -.5), (.5, .5))

hdiff = 2
vdiff = .3
onebytwo = gen.rectangle((one.ur[0] + hdiff, one.ur[1] + vdiff),
                         (one.ur[0] + hdiff + 1, one.ur[1] + vdiff + 1))
divide(gen, onebytwo, 1, 'horizontal')
twobyone = gen.rectangle((one.ur[0] + hdiff, one.ll[1] - vdiff - 1),
                         (one.ur[0] + hdiff + 1, one.ll[1] - vdiff))
divide(gen, twobyone, 1, 'vertical')
onebyfour = gen.rectangle((onebytwo.ur[0] + hdiff,  onebytwo.ur[1] + vdiff),
                          (onebytwo.ur[0] + hdiff + 1,  onebytwo.ur[1] + vdiff + 1))
divide(gen, onebyfour, 3, 'horizontal')

fourbyone = gen.rectangle((twobyone.ur[0] + hdiff, twobyone.ll[1] - vdiff - 1),
                          (twobyone.ur[0] + hdiff + 1, twobyone.ll[1] - vdiff))
divide(gen, fourbyone, 3, 'vertical')
twobytwo = gen.rectangle((one.ll[0] + 3*hdiff, one.ll[1]),
                         (one.ll[0] + 3*hdiff + 1, one.ll[1] + 1))
divide(gen, twobytwo, 1, 'vertical')
divide(gen, twobytwo, 1, 'horizontal')

connections = [(one, twobyone),
               (one, onebytwo),
               (onebytwo, onebyfour),
               (onebytwo, twobytwo),
               (twobyone, fourbyone),
               (twobyone, twobytwo)]
for conn in connections:
    draw_arrow(gen, conn[0], conn[1])


labels = [(one, '1 x 1'),
          (onebytwo, '1 x 2'),
          (onebyfour, '1 x 4'),
          (twobyone, '2 x 1'),
          (fourbyone, '4 x 1'),
          (twobytwo, '2 x 2')]

for label in labels:
    draw_label(gen, label[0], label[1])

cheight = onebyfour.ur[1] + .5

gen.cnode(((onebyfour.ll[0] + onebyfour.ur[0]) * .5, cheight), '4')
gen.cnode((.5 * (one.ll[0] + one.ur[0]), cheight), '1')
gen.cnode((.5 * (onebytwo.ll[0] + onebytwo.ur[0]), cheight), '2')


gen.show()
