class Grafo:
    def __init__(self):
        self.adj = {}
        self.where = -1
    
    def add_edge(self, a, b, p):
        if a in self.adj:
            self.adj[a].append((p, b))
        else:
            self.adj[a] = []
            self.adj[a].append((p, b))

    def mod_edge(self, a, b, p):
        for i in range(len(self.adj[a])):
            if self.adj[a][i][1] == b:
                self.adj[a][i][0] = p

    def get_most_prob(self):
        a = self.where
        m = 0
        idx = -1
        for i in range(len(self.adj[a])):
            if self.adj[a][i][0] > m:
                m = self.adj[a][i][0]
                idx = self.adj[a][i][1]
        return idx

    def move(self, b):
        self.where = b

g = Grafo()
g.add_edge(0, 1, 0.5)
g.add_edge(1, 2, 0.9)
print(g.get_most_prob())