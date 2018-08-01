import tikz

def draw_children(gen, root, labels):
    nodes = []
    vdiff = 1.3
    if len(labels) == 3:
        hdiff = 1.5
        nodes.append(
            gen.cnode((root.pos[0] - hdiff, root.pos[1] - vdiff), labels[0])
            )
        nodes.append(
            gen.cnode((root.pos[0], root.pos[1] - vdiff), labels[1])
            )
        nodes.append(
            gen.cnode((root.pos[0] + hdiff, root.pos[1] - vdiff), labels[2])
        )
    elif len(labels) == 2:
        hdiff = .7
        nodes.append(
            gen.cnode((root.pos[0] - hdiff, root.pos[1] - vdiff), labels[0])
            )
        nodes.append(
            gen.cnode((root.pos[0] + hdiff, root.pos[1] - vdiff), labels[1])
        )
    else:
        nodes.append(
            gen.cnode((root.pos[0], root.pos[1] - vdiff), labels[0])
            )

    for node in nodes:
        gen.line(root, node)

    return nodes


gen = tikz.tikz_gen()
root = gen.cnode((0, 0), '8')
lvl1 = draw_children(gen, root, ('1','2','4'))
draw_children(gen, lvl1[1], ('1',))
lvl2 = draw_children(gen, lvl1[2], ('1', '2'))
draw_children(gen, lvl2[1], ('1',))

gen.show()

