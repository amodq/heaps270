class BinomialTree:
    def __init__(self, val, value):
        # value of the root of the tree
        self.key = val # this is key
        self.value = value
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
        self.key = new_val
        if self.parent and self.key < self.parent.key:
            self.bubble_up()
    
    # bubble up a node in the tree, modify tree in place
    def bubble_up(self):
#         if self.parent == None or self.val > self.parent.val:
#             return
#         siblings = self.parent.children[:]
#         siblings.remove(self)
#         self.parent.children = []
#         for child in self.children:
#             child.parent = self.parent
#             self.parent.children.append(child)
#         self.children = siblings
#         self.children.append(self.parent)
#         if self.parent.parent:
#             self.parent.parent.children.remove(self.parent)
#             self.parent.parent.children.append(self)
#         temp = self.parent
#         self.parent = self.parent.parent
#         temp.parent = self
        if self.parent == None or self.key > self.parent.key:
            return
        self.key, self.value, self.parent.key, self.parent.value = \
            self.parent.key, self.parent.value, self.key, self.value
        self.parent.bubble_up()

class BinomialHeap:

    def __init__(self):
        self.trees = []
        self.nodes = {}

    # find and remove the min value in heap
    def del_min(self):
        if self.trees == []:
            return None
        smallest_node = self.trees[0]
        for tree in self.trees:
            if tree.key < smallest_node.key:
                smallest_node = tree
        self.trees.remove(smallest_node)
        h = BinomialHeap()
        h.trees = smallest_node.children
        self.merge(h)
 
        return smallest_node.key

    # find the min value in heap
    def get_min(self):
        if self.trees == []:
            return None
        min_val = self.trees[0].key
        for tree in self.trees:
            if tree.key < min_val:
                min_val = tree.key
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
                    if after.key < after_after.key:
                        after.add_child(after_after)
                        del self.trees[i + 2]
                    else:
                        after_after.add_child(after)
                        del self.trees[i + 1]
                else:
                    if current.key < after.key:
                        current.add_child(after)
                        del self.trees[i + 1]
                    else:
                        after.add_child(current)
                        del self.trees[i]
            i = i + 1

    # insert a new value into the heap
    def insert(self, key, value):
        if value in self.nodes:
            print("value in nodes already, returning")
            return
        g = BinomialHeap()
        t = BinomialTree(key, value)
        g.trees.append(t)
        self.merge(g)
        self.nodes[value] = t
        return t
        
    # decrease a value in the heap, this value should be at the root of a subtree
    def dec_key(self, tree, new_val):
        if tree.key < new_val:
            return
        tree.dec_val(new_val)
#         if tree.parent == None:
#             for i in range(len(self.trees)):
#                 if self.trees[i] in tree.children:
#                     del self.trees[i]
#                     break
#             self.trees.append(tree)