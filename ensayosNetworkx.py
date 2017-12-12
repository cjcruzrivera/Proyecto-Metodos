import networkx as nx

class Vertex:
    infectado = False
    numero = -1
    religion = ''

    
    def __init__(self, numero, infectado, religion):
        self.infectado = infectado
        self.numero = numero
        self.religion = religion

vertex1 = Vertex(True, -1)
vertex2 = Vertex(False, -1)
G = nx.Graph()
G.add_node(vertex1)
G.add_node(vertex2)
G.add_edge(vertex1, vertex2)
print (G.nodes())
