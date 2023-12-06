class Graph():
    def __init__(self,nNode):
        self.adj = [[None]*nNode for i in range(nNode)]
        self.nNode = nNode
    def link(self,start,end,weight = 1):
        self.adj[start][end] = weight
        self.adj[end][start] = weight
    
    def bfs(self,start):
        visited = [False]*self.nNode
        queue = []
        queue.append(start)
        visited[start] = True
        print(start)

        while (len(queue)>0):
            cur = queue.pop(0)
            for i in range(self.nNode):
                if self.adj[cur][i] != None and visited[i] == False:
                    queue.append(i)
                    visited[i] = True
                    print(i)

    def get_degree(self,cur):
        count = 0
        for i in range(self.nNode):
            if self.adj[cur][i] != None:
                count += 1
        return count
    def get_degree_all(self):
        degree = []
        for i in range(self.nNode):
            temp = self.get_degree(i)
            degree.append(temp)
        return degree