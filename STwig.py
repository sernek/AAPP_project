
# STwig class: root,children
class STwig:
    def __init__(self, root, label=None):
        self.root = root
        self.label = label if label is not None else label
    def __repr__(self):
        return "<%s,%s>" % (self.root, self.label)
