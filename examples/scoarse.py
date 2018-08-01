import tikz
import numpy as np

class topo:

    def alloc(self):
        self.beg = np.zeros((4,2), dtype='int')
        self.nlocal = np.zeros((4,2), dtype='int')

    def __init__(self, nglobal=None):
        self.alloc()
        if not nglobal is None:
            self.nglobal = nglobal

            for i in range(4):
                for dim in range(2):
                    self.beg[i,dim] = self.low(i) + 1
                    self.nlocal[i,dim] = self.size(i)

    def low(self, ind):
        return ind*self.nglobal/4

    def high(self, ind):
        return self.low(ind+1) - 1

    def size(self, ind):
        return self.high(ind) - self.low(ind) + 1



def refine(fgrid):
    cgrid = topo()
    for i in range(4):
        for ind in range(2):
            if (fgrid.beg[i,ind] % 2 == 1):
                cgrid.beg[i,ind] = (fgrid.beg[i,ind] + 1) / 2
                cgrid.nlocal[i,ind] = (fgrid.nlocal[i,ind] + 1) / 2
            else:
                cgrid.beg[i,ind] = fgrid.beg[i,ind] / 2 + 1
                if fgrid.nlocal[i,ind] % 2 == 1:
                    cgrid.nlocal[i,ind] = (fgrid.nlocal[i,ind] - 1) / 2
                else:
                    cgrid.nlocal[i,ind] = (fgrid.nlocal[i,ind] + 1) / 2

    return cgrid


def get_corners(gen, grd):
    ret = []
    ret.append(gen.node(grd.bbox[0]))
    ret.append(gen.node(grd.bbox[1]))
    ret.append(gen.node((grd.bbox[0][0], grd.bbox[1][1])))
    ret.append(gen.node((grd.bbox[1][0], grd.bbox[0][1])))

    for crn in ret:
        crn.attr.append('draw=none')

    return ret


class scope:

    def __init__(self, gen, shift, slant):
        self.gen = gen
        self.shift = shift
        self.slant = slant

    def __enter__(self):
        gen = self.gen
        shift = self.shift
        slant = self.slant
        gen.raw('\\begin{{scope}}[xshift={0},yshift={1},every node/.append style={{yslant={3},xslant={2}}},yslant={3},xslant={2}]'.format(*(shift+slant)))

    def __exit__(self, *args):
        self.gen.raw('\\end{scope}')
        return True


def draw_grid(gen, grd):
    pgrid = gen.grid((0,0), (4,4))
    rad = .05
    for j in range(4):
        for i in range(4):
            nx = grd.nlocal[i,0]
            ny = grd.nlocal[j,0]
            dx = 1./(nx+1)
            dy = 1./(ny+1)
            cy = j
            for jj in range(ny):
                cy += dy
                cx = i
                for ii in range(nx):
                    cx += dx
                    circ = gen.circle((cx,cy), rad)
                    circ.attr.append('fill=black')
    return pgrid


def draw_seq(gen, shift, slant):
    cgrid = topo(13)
    for i in range(2):
        with scope(gen, shift, slant):
            draw_grid(gen, cgrid)
        shift[1] -= 130
        cgrid = refine(cgrid)


def draw_gather(gen, shift, slant):
    grd = topo(4)
    corners0 = None
    with scope(gen, shift, slant):
        pgrid = draw_grid(gen, grd)
        corners0 = get_corners(gen, pgrid)
    shift[1] -= 130

    grd = topo()
    grd.nlocal[0,0] = 4
    grd.nlocal[0,1] = 4
    corners1 = None
    with scope(gen, shift, slant):
        pgrid = draw_grid(gen, grd)
        corners1 = get_corners(gen, pgrid)

    arr_scale = 1.5
    gather_arrow = gen.arrow(corners0[2], corners1[2])
    gather_arrow.lw = 2
    gather_arrow.add_node('left', 'gather')
    gather_arrow.nodes['left'].scale = arr_scale
    scatter_arrow = gen.arrow(corners1[3], corners0[3])
    scatter_arrow.lw = 2
    scatter_arrow.add_node('right', 'scatter')
    scatter_arrow.nodes['right'].scale = arr_scale


gen = tikz.tikz_gen()

slant = [-1, 0.5]
shift = [0, 0]
draw_seq(gen, shift, slant)

draw_gather(gen, shift, slant)

gen.show()
