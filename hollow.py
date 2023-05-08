# https://arxiv.org/pdf/1510.06535.pdf

class HollowNode():
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.child = None
        self.next = None
        self.ep = None
        self.rank = 0
        

    
class HollowHeap():
    def __init__(self):
        self.vals = {} # store val, node
        
        
    def insert(self, k, v, h):
        return self.meld(self.makeNode(k, v), h)
    
    def meld(self, g, h):
        if g == None:
            return h
        if h == None:
            return g
        return self.link(g, h)
        
    def findMin(self, h):
        if h == None:
            return None
        return h.item
    
    def decKey(self, k, v, h):
        
        if v not in self.vals:
            return h
        
        if (k >= self.vals[v].key):
            return h
        
        # if root
        u = self.vals[v]
        if u is h:
            u.key = k
            return h
        # otherwise
        v = self.makeNode(k, v)
        u.value = None
        if u.rank > 2:
            v.rank = u.rank - 2
        v.child = u
        u.ep = v
        
        return self.link(v, h)
        
    def deleteMin(self, h):
        return self.delete(h.value, h)
    
    def delete(self, v, h):
        self.vals[v].value = None
        self.vals[v] = None
        self.vals.pop(v, None)
        # not root del
        if h.value != None:
            print("not root del")
            return h
        maxRank = 0
        A = {}
        h.next = None
        
        # otherwise
        while h != None:
            w = h.child
            v = h
            h = h.next
            while w != None:
                u = w
                w = w.next
                if u.value == None:
                    if u.ep == None:
                        u.next = h
                        h = u
                    else:
                        if u.ep is v:
                            w = None
                        else:
                            u.next = None
                        u.ep = None
                else:
                    # do ranked links
                    while u.rank in A:
                        u = self.link(u, A[u.rank])
                        del A[u.rank]
                        u.rank += 1
                    A[u.rank] = u
                    if u.rank > maxRank:
                        maxRank = u.rank
                        
        # do unranked links
        for i in A:
            if h == None:
                h = A[i]
            else:
                h = self.link(h, A[i])                
        return h
    # aux methods
    
    def makeNode(self, k, v):
        u = HollowNode(k, v)
        self.vals[v] = u
        return u
        
    def link(self, v, w):
        if v.key >= w.key:
            self.addChild(v, w)
            return w
        else:
            self.addChild(w, v)
            return v
                
    @staticmethod
    def addChild(v, w):
        v.next = w.child
        w.child = v