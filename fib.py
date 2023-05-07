class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.child = None
        self.left = None
        self.right = None
        self.degree = 0
        self.mark = False
        
class FibonacciHeap:
    def __init__(self):
        self.root_list =  None
        self.min = None
        self.total_num_nodes = 0

    # Returns the total number of nodes in the heap
    def get_total_number_nodes(self):
        return self.total_num_nodes
    
    # Returns number of trees in the heap
    def get_total_number_trees(self):
        if self.root_list == None:
            return 0
        return len([x for x in self.iterate(self.root_list)])

    # Iterates through the circular-doubly linked list
    def iterate(self, head):
        if not head:
            head = self.root_list
        current = head
        while True:
            yield current
            if not current:
                break
            current = current.right
            if current == head:
                break

    # Returns minimum node of heap
    def get_minimum(self):
        return self.min
    
    # Returns minimum key of heap
    def get_minimum_key(self):
        return self.min.key

    # Inserts node with given key to heap
    def insert(self, key):
        node = Node(key)
        node.left = node.right = node
        self.insert_into_root_list(node)
        if self.min:
            if node.key < self.min.key:
                self.min = node
        else:
            self.min = node
        self.total_num_nodes += 1
        return node

    # Extracts the minimum node of the heap
    def extract_minimum(self):
        z = self.min
        if z:
            if z.child:
                children = [x for x in self.iterate(z.child)]
                for x in children:
                    self.insert_into_root_list(x)
                    x.parent = None
            self.remove_from_root_list(z)    
            if z == z.right:
                self.min = None
                self.root_list = None
            else:
                self.consolidate()
                min = self.root_list
                for node in self.iterate(self.root_list):
                    if node.key < min.key:
                        min = node
                self.min = min
            self.total_num_nodes -= 1
        return z

    # (DONE) Decreases node's key to key 
    def decrease_key(self, node, key):
        if key > node.key:
            #raise ValueError("New key greater than current key.")
            return
        node.key = key
        p = node.parent
        if p and node.key < p.key:
            self.cut(node, p)
            self.cascading_cut(p)
        if node.key < self.min.key:
            self.min = node
        return

    # Removes a node from the heap
    def delete(self, node):
        self.decrease_key(node, -float('inf'))
        self.extract_minimum()
        
    # Cuts node from its parent 
    def cut(self, node, parent):
        self.remove_from_child_list(parent, node)
        parent.degree -= 1
        self.insert_into_root_list(node)
        node.parent = None
        node.mark = False
    def cascading_cut(self, node):
        p = node.parent
        if p:
            if not p.mark:
                p.mark = True
            else:
                self.cut(node, p)
                self.cascading_cut(p)

    # Inserts a node into the end of root list 
    def insert_into_root_list(self, node):
        if not self.root_list:
            self.root_list = node
        else:
            node.right = self.root_list
            node.left = self.root_list.left
            self.root_list.left.right = node
            self.root_list.left = node

    # Removes a root node from the doubly linked root list.
    def remove_from_root_list(self, node):
        if not self.root_list:
            raise ValueError('Heap is empty!')    
        if self.root_list == node:
            if self.root_list == self.root_list.right:
                self.root_list = None
                return
            else:
                self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left
        return

    # Removes a node from the doubly linked list at the child level
    def remove_from_child_list(self, parent, node):
        # if single child
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left
    
    # Consolidates trees until all trees have distinct degrees
    def consolidate(self):
        if not self.root_list:
            return
        A = [None] * self.get_total_number_nodes()
        roots = [root for root in self.iterate(self.root_list)]
        for w in roots:
            x = w
            d = w.degree
            while A[d] != None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self.link(x, y)
                A[d] = None
                d += 1
            A[d] = x
        return

    # Links two root trees together, making the smaller node the parent
    def link(self, parent, node):
        self.remove_from_root_list(node)
        node.left = node.right = node
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node
        parent.degree += 1
        node.parent = parent
        node.mark = False
        return
                
    # Prints the whole heap
    def print_heap(self, head = None):
        if self.root_list:
            roots = [tree for tree in self.iterate(self.root_list)]
            for root in roots:
                print('-----')
                self.print_tree(root)
                print()
            print('-----')
                
    # Prints a tree rooted at node
    def print_tree(self, node):
        if not node:
            return
        print(node.key, end=' ')
        if node.child:
            print()
            children = [child for child in self.iterate(node.child)]
            for child in children:
                self.print_tree(child)