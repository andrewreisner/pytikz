import tikz


def geth(grd):
    return (grd.bbox[1][0]-grd.bbox[0][0],
            grd.bbox[1][1]-grd.bbox[0][1])

def draw_gnodes(gen, corner):
    igs = corner[0] + .5
    jgs = corner[1] + .5 + 3

    cnt = 0
    for j in range(4):
        for i in range(4):
            gen.cnode((igs + i, jgs - j), str(hex(cnt))[2:])
            cnt += 1

def draw_snodes(gen, corner, labels):
    igs = corner[0] + .25
    jgs = corner[1] - .25

    cnt = 0
    for jj in range(2):
        for ii in range(2):
            cnt = 0
            for j in range(2):
                for i in range(2):
                    gen.cnode((ii+i*.5 + igs, jgs - j*.5 - jj), str(labels[cnt])).scale = .5
                    cnt += 1

gen = tikz.tikz_gen()

diff = 8
lw = '.16cm'
grd0 = gen.grid((0, diff), (4, 4+diff))
draw_gnodes(gen, grd0.bbox[0])

grd1 = gen.grid((diff, diff), (4+diff, 4+diff))
draw_gnodes(gen, grd1.bbox[0])

def draw_divide(gen, grd):
    mdy = .5*(grd.bbox[1][1] + grd.bbox[0][1])
    mdx = .5*(grd.bbox[1][0] + grd.bbox[0][0])
    gen.line((grd.bbox[0][0], mdy), (grd.bbox[1][0], mdy)).lw = lw
    gen.line((mdx, grd.bbox[0][1]), (mdx, grd.bbox[1][1])).lw = lw
    return (mdx, mdy)

(mdx, mdy) = draw_divide(gen, grd1)

agg_arr = gen.arrow((grd0.bbox[1][0], mdy), (grd1.bbox[0][0], mdy))
agg_arr.attr.append('ultra thick')
agg_arr.add_node('above', 'Agglomerate')

hx, hy = geth(grd1)
hx /= 4.
hy /= 4.
clw = '.08cm'
gen.circle((mdx - hx, mdy-hy), hx).lw = clw
gen.circle((mdx + hx, mdy + hy), hx).lw = clw
gen.circle((mdx + hx, mdy - hy), hx).lw = clw
gen.circle((mdx - hx, mdy + hy), hx).lw = clw

grd2 = gen.grid((0,0), (4,4))
gather_arr = gen.arrow((grd1.bbox[0][0], grd1.bbox[0][1]),
                       (grd2.bbox[1][0], grd2.bbox[1][1]))
gather_arr.attr.append('ultra thick')
gather_arr.add_node('above', 'Allgather').attr.append('sloped')

(mdx, mdy) = draw_divide(gen, grd2)

hx, hy = geth(grd2)
hx /= 8.
hy /= 8.

gen.circle((mdx-3*hx, mdy-hy), hx).lw = clw
gen.circle((mdx-3*hx, mdy+3*hy), hx).lw = clw
gen.circle((mdx+hx, mdy+3*hy), hx).lw = clw
gen.circle((mdx+hx, mdy-hy), hx).lw = clw

draw_snodes(gen, (grd2.bbox[0][0], grd2.bbox[1][1]), [0,1,4,5])
draw_snodes(gen, (mdx, grd2.bbox[1][1]), [2,3,6,7])
draw_snodes(gen, (grd2.bbox[0][0], mdy), [8,9,'c','d'])
draw_snodes(gen, (mdx, mdy), ['a','b','e','f'])

grd3 = gen.grid((diff,0), (4+diff, 4))
grd3.step = 2.0

draw_gnodes(gen, grd3.bbox[0])

mdy = .5*(grd3.bbox[1][1] + grd3.bbox[0][1])
cycle_arr = gen.arrow((grd2.bbox[1][0], mdy), (grd3.bbox[0][0], mdy))
cycle_arr.attr.append('ultra thick')
cycle_arr.add_node('above', 'Redundant Cycle')
cycle_arr.add_node('below', r'$\times 4$')

#gen.save('figs/agglom.tikz')
#gen.save('figs/agglom-anim.tikz')
gen.show()
