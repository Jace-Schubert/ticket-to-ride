class UnionFind:
    def __init__(self, n):
        """
        Initialize Union-Find for n nodes.
        Each node starts as its own parent (its own component).
        Rank is used to keep the tree flat (union by rank).
        """

        # parent[i] = i initially
        self.parent = list(range(n))

        # Used to keep tree balanced
        self.rank = [0] * n           

    #------------------------------------------------------
    def find(self, x):
        """
        Find the root/representative of node x.
        """

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    #------------------------------------------------------
    def union(self, x, y):
        """
        Try to merge the sets containing x and y.
        Returns False if they're already in the same set.
        """

        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False 

        # Union by rank: attach smaller tree under larger tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True 