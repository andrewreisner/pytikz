import tikz



gen = tikz.tikz_gen()

grd = gen.grid((0, 0), (4, 2))

rad = 0.03
for j in range(2):
    for i in range(4):
        nx = 8
        ny = 1
        dx = 1./(nx+1)
        dy = 1./(ny+1)
        cy = j
        for jj in range(ny):
            cy += dy
            cx = i
            for ii in range(nx):
                cx += dx
                circ = gen.circle((cx, cy), rad)
                circ.attr.append('fill=black')

gen.show()
