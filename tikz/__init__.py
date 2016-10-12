from wrappers import *

class tikz_gen(object):

    def __init__(self):
        self.tobj = []
        self.cid = 0
        self.rep = ''

    def __getattr__(self, attr):
        import wrappers
        dict = wrappers.__dict__
        # return lambda *args, **kwargs: dict[attr](self.cid, *args, **kwargs)
        return lambda *args, **kwargs: self.register(dict[attr], *args, **kwargs)

    def register(self, const, *args, **kwargs):
        v = const(self.cid, *args, **kwargs)
        self.tobj.append(v)
        self.cid += 1
        return v

    def compile(self):
        self.rep = ''
        self.rep += '\\begin{tikzpicture}\n'
        for obj in self.tobj:
            self.rep += str(obj) + '\n'
        self.rep += '\\end{tikzpicture}\n'

    def save(self, fname):
        self.compile()
        with open(fname, mode='w') as fh:
            fh.write(self.rep)

    def show(self):
        self.save('/tmp/fig.tex')
        import subprocess
        subprocess.call(['tikz2pdf', '/tmp/fig.tex', '-o', '/tmp/fig.pdf'])
        subprocess.call(['okular', '/tmp/fig.pdf'])
