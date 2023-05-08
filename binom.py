class BinomialTree:
    def __init__(self, val):
        # value of the root of the tree
        self.val = val
        self.children = []
        self.degree = 0
        self.parent = None
 
    # appending a subtree
    def add_child(self, t):
        self.children.append(t)
        t.parent = self
        self.degree = self.degree + 1

    # decrease the root of a tree, and bubble up if necessary
    def dec_val(self, new_val):
        self.val = new_val
        while self.parent and self.val < self.parent.val:
            self.bubble_up()      
    
    # bubble up one level, modify tree in place
    def bubble_up(self):
        if self.parent == None or self.val >= self.parent.val:
            return
        parent = self.parent
        siblings = parent.children
        siblings.remove(self)
        for s in siblings:
            s.parent = self
        parent.children = []
        for child in self.children:
            child.parent = parent
            parent.children.append(child)
        self.children = siblings
        self.children.append(parent)
        grandparent = parent.parent
        parent.parent = self
        if grandparent:
            grandparent.children.remove(parent)
            grandparent.children.append(self)
        self.parent = grandparent

class BinomialHeap:

    def __init__(self):
        self.trees = []

    # find and remove the min node in heap
    def del_min(self):
        if self.trees == []:
            return None
        smallest_node = self.trees[0]
        for tree in self.trees:
            if tree.val < smallest_node.val:
                smallest_node = tree
        for child in smallest_node.children:
            child.parent = None
        self.trees.remove(smallest_node)
        h = BinomialHeap()
        h.trees = smallest_node.children
        self.merge(h)
 
        return smallest_node

    # find the min value in heap
    def get_min(self):
        if self.trees == []:
            return None
        min_val = self.trees[0].val
        for tree in self.trees:
            if tree.val < min_val:
                min_val = tree.val
        return min_val

    # merge two binomial heaps
    def merge(self, h):
        self.trees.extend(h.trees)
        self.trees.sort(key=lambda tree: tree.degree)
        if self.trees == []:
            return
        i = 0
        while i < len(self.trees) - 1:
            current = self.trees[i]
            after = self.trees[i + 1]
            if current.degree == after.degree:
                # if the next and the next next tree have the same degree, merge them first
                if (i + 1 < len(self.trees) - 1 and self.trees[i + 2].degree == after.degree):
                    after_after = self.trees[i + 2]
                    if after.val < after_after.val:
                        after.add_child(after_after)
                        del self.trees[i + 2]
                    else:
                        after_after.add_child(after)
                        del self.trees[i + 1]
                else:
                    if current.val < after.val:
                        current.add_child(after)
                        del self.trees[i + 1]
                    else:
                        after.add_child(current)
                        del self.trees[i]
            else:
                i = i + 1

    # insert a new value into the heap
    def insert(self, key):
        g = BinomialHeap()
        t = BinomialTree(key)
        g.trees.append(t)
        self.merge(g)
        return t

    # decrease a value in the heap, this value should be at the root of a subtree
    def dec_key(self, tree, new_val):
        assert(tree != None)
        if (new_val >= tree.val):
            return
        # find the root of the subtree we're decreasing key at
        root = tree
        while root.parent:
            root = root.parent
        assert(root in self.trees)
        tree.dec_val(new_val)
        # if tree becomes the new root, update in heap
        if tree.parent == None and tree != root:
            self.trees.remove(root)
            self.trees.append(tree)