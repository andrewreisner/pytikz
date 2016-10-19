class wrapper(object):

    def __init__(self, id):
        self.id = id
        self.rep = ''

    def compile(self):
        self.rep = ''

    def __str__(self):
        self.compile()
        return self.rep


class raw(wrapper):

    def __init__(self, id, rstr):
        self.rstr = rstr

    def compile(self):
        self.rep = self.rstr


class grid(wrapper):

    def __init__(self, id, ll, ur):
        super(grid, self).__init__(id)
        self.bbox = (ll,ur)
        self.step = None

    def compile(self):
        self.rep = ''
        attrs = []
        if self.step is not None:
            attrs.append('step=%f'%(self.step))
        self.rep += '\\draw[%s] (%f, %f) grid (%f, %f);' %tuple([''.join(attrs)] + [v for corner in self.bbox for v in corner])


class node(wrapper):

    def __init__(self, id, pos=None, label=''):
        super(node, self).__init__(id)
        self.attr = ['draw']
        self.label = label
        self.pos = pos
        self.scale = 1

    def compile(self):
        self.rep = ''
        self.rep += '\\node['
        attrs = self.attr[:]
        attrs.append('scale=%f' %(self.scale))
        self.rep += ','.join(attrs)
        pstr = ''
        if self.pos != None:
            pstr = ' at (%f, %f) ' %(self.pos[0], self.pos[1])
        self.rep += '] (%d)%s{%s};' %(self.id, pstr, self.label)


class text(node):

    def __init__(self, id, pos=None, label=''):
        super(text, self).__init__(id, pos, label)
        self.attr = []


class cnode(node):

    def __init__(self, id, pos=None, label=''):
        super(cnode, self).__init__(id, pos, label)
        self.attr.append('circle')


class circle(wrapper):

    def __init__(self, id, pos, radius):
        super(circle, self).__init__(id)
        self.pos = pos
        self.radius = radius
        self.lw = None
        self.attr = []

    def compile(self):
        self.rep = ''
        attrs = self.attr[:]
        if self.lw is not None:
            attrs.append('line width=%s' %(self.lw))
        self.rep += '\\draw[%s] (%f, %f) circle [radius=%f];' %(','.join(attrs),
                                                                self.pos[0], self.pos[1], self.radius)



class rectangle(wrapper):

    def __init__(self, id, ll, ur):
        super(rectangle, self).__init__(id)
        self.ll = ll
        self.ur = ur
        self.attr = []

    def compile(self):
        self.rep = ''
        attrs = self.attr[:]
        self.rep += '\\draw[{attr}] ({ll[0]},{ll[1]}) rectangle ({ur[0]},{ur[1]});'.format(attr=','.join(attrs),
                                                                                           ll=self.ll,
                                                                                           ur=self.ur)


class line(wrapper):

    def __init__(self, id, p0, p1):
        super(line, self).__init__(id)
        self.attr = []
        self.lw = None
        self.p0 = p0
        self.p1 = p1
        self.substr = ''

    def compile(self):
        self.rep = ''
        attrs = self.attr[:]
        if self.lw is not None:
            attrs.append('line width=%s' %(self.lw))
        if isinstance(self.p0, node):
            self.rep += '\\draw[%s] (%d) -- %s (%d);' %(','.join(attrs),
                                                        self.p0.id,
                                                        self.substr,
                                                        self.p1.id)
        else:
            self.rep += '\\draw[%s] (%f, %f) -- %s (%f, %f);' %(','.join(attrs),
                                                           self.p0[0], self.p0[1],
                                                                self.substr,
                                                           self.p1[0], self.p1[1])



class arrow(line):

    def __init__(self, id, p0, p1):
        super(arrow,self).__init__(id, p0, p1)
        self.attr.append('->')
        self.nodes = {}


    def add_node(self, dir, label):
        nd = node(-1, label=label)
        nd.attr = []
        nd.attr.append(dir)
        nd.attr.append('midway')
        self.nodes[dir] = nd

        return nd

    def compile(self):
        self.substr = ''
        for _,nd in self.nodes.iteritems():
            attrs = nd.attr[:]
            attrs.append('scale=%f' %(nd.scale))
            self.substr += ' node [%s] {%s} ' % (','.join(attrs), nd.label)
        super(arrow,self).compile()
