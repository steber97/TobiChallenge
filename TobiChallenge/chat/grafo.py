class Grafo:
    def __init__(self):
        self.adj = {}

    def update_edge(self, a, b):
        if a is None:
            return
        if a not in self.adj:
            self.adj[a] = {}
            self.adj[a][b] = 1

        else:
            if b not in self.adj[a]:
                self.adj[a][b] = 1
            else:
                self.adj[a][b] += 1
        return

    def get_most_prob(self, node):
        best_node = -1
        max_val = -1
        for el in self.adj[node]:
            if self.adj[node][el] > max_val:
                max_val = self.adj[node][el]
                best_node = el
        return best_node
