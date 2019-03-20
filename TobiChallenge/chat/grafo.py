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

    def print_adj_list(self, node):
        if node in self.adj:
            print(self.adj[node])

    def get_most_prob(self, node):
        best_node = -1
        max_val = -1
        total = 0
        if node not in self.adj:
            return None, None
        for el in self.adj[node]:
            total += self.adj[node][el]
            if self.adj[node][el] > max_val and el != node:
                max_val = self.adj[node][el]
                best_node = el
        return best_node, max_val/total
