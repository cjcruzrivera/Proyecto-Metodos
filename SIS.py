#!/usr/bin/env python
import networkx as nx
import math
import csv
import random as rand
import random
import sys
import thread
import time
import matplotlib.pyplot as plt
import matplotlib.pyplot as blt
import copy
import matplotlib.animation as animation
"""
Religiones:
0: No religion
1: Religion catolica
2: Religion protestante
"""


"""

La religion catolica al tratar de transferirse no genera ninguna resistencia en quien se va a transferir
pero sus seguidores tienen un decremento en su grado de transferencia en un 0.7x, y ademas el grado de percepcion
de otras ideas agenas a su religion se mantiene igual

La religion protestante por su parte genera una resistencia del 1.5x en quien se va a transferir pero genera
un grado de transferencia del 1.5x, y ademas el grado de percepcion de otras ideas ajenas a su religion disminuye
a la mitad

"""
print (time.strftime("%I:%M:%S"))

NO_RELIGION = 0
RELIGION_CATOLICA = 1
RELIGION_PROTESTANTE = 2
MULTIPLICADOR_TRANSFERENCIA_CATOLICA = 1
MULTIPLICADOR_TRANSFERENCIA_PROTESTANTE = 1.5
MULTIPLICADOR_PERCEPCION_PROTESTANTE = 1
MULTIPLICADOR_RESISTENCIA_A_CONVERTIRSE_PROTESTANTE = 1
MULTIPLICADOR_RESISTENCIA_A_CONVERTIRSE_CATOLICO = 1.0

def configuracion_protestantes_poco_perceptivos():
      MULTIPLICADOR_PERCEPCION_PROTESTANTE = 0.5

def configuracion_catolicos_poco_transferentes():
      MULTIPLICADOR_TRANSFERENCIA_CATOLICA = 0.5
def configuracion_resistencia_contra_protestantes():
      MULTIPLICADOR_RESISTENCIA_A_CONVERTIRSE_PROTESTANTE = 1.5

def configuracion1():
      configuracion_catolicos_poco_transferentes()
      configuracion_protestantes_poco_perceptivos()
      configuracion_resistencia_contra_protestantes()

def configuracion_no_resistencia_contra_protestantes():
      MULTIPLICADOR_RESISTENCIA_A_CONVERTIRSE_PROTESTANTE = 1

def configuracion_catolicos_transferentes():
      MULTIPLICADOR_TRANSFERENCIA_CATOLICA = 1

def configuracion2():
      configuracion_no_resistencia_contra_protestantes()

#configuracion1()
configuracion2()

# Animation funciton
def animate(i):
    colors = ['r', 'b', 'g', 'y', 'w', 'm']
    nx.draw_circular(G, node_color=[random.choice(colors) for j in range(9)])




def independent_cascade(G, seeds, steps=0):
  """Return the active nodes of each diffusion step by the independent cascade
  model

  Parameters
  -----------
  G : graph
    A NetworkX graph
  seeds : list of nodes
    The seed nodes for diffusion
  steps: integer
    The number of steps to diffuse.  If steps <= 0, the diffusion runs until
    no more nodes can be activated.  If steps > 0, the diffusion runs for at
    most "steps" rounds

  Returns
  -------
  layer_i_nodes : list of list of activated nodes
    layer_i_nodes[0]: the seeds
    layer_i_nodes[k]: the nodes activated at the kth diffusion step

  Notes
  -----
  When node v in G becomes active, it has a *single* chance of activating
  each currently inactive neighbor w with probability p_{vw}

  Examples
  --------
  >>> DG = nx.DiGraph()
  >>> DG.add_edges_from([(1,2), (1,3), (1,5), (2,1), (3,2), (4,2), (4,3), \
  >>>   (4,6), (5,3), (5,4), (5,6), (6,4), (6,5)], relacion_personas=0.2)
  >>> H = nx.independent_cascade(DG,[6])

  References
  ----------
  [1] David Kempe, Jon Kleinberg, and Eva Tardos.
      Influential nodes in a diffusion model for social networks.
      In Automata, Languages and Programming, 2005.
  """
  if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
      raise Exception( \
          "independent_cascade() is not defined for graphs with multiedges.")

  # make sure the seeds are in the graph
  for s in seeds:
    if s not in G.nodes():
      raise Exception("seed", s, "is not in graph")
  validar_semillas(seeds)
  # change to directed graph
  if not G.is_directed():
    DG = G.to_directed()
  else:
    DG = copy.deepcopy(G)

  # init activation probabilities
  for e in DG.edges():
    if 'relacion_personas' not in DG[e[0]][e[1]]:
      DG[e[0]][e[1]]['relacion_personas'] = 1
      
    elif DG[e[0]][e[1]]['relacion_personas'] >  1:
      raise Exception("edge activation probability:", \
          DG[e[0]][e[1]]['relacion_personas'], "cannot be larger than 1")

  # perform diffusion
  A = copy.deepcopy(seeds)  # prevent side effect
  if steps <= 0:
    # perform diffusion until no more nodes can be activated
    return _diffuse_all(DG, A)
  # perform diffusion for at most "steps" rounds
  return _diffuse_k_rounds(DG, A, steps)


capas_creyentes = []
def _diffuse_all(G, A):
  tried_edges = set()
  layer_i_nodes = [ ]
  layer_i_nodes.append([i for i in A])  # prevent side effect
  capas_creyentes.append(copy.deepcopy(creyentes))
  while True:
    len_old = len(A)
    (A, activated_nodes_of_this_round, cur_tried_edges) = \
        _diffuse_one_round(G, A, tried_edges)
    layer_i_nodes.append(activated_nodes_of_this_round)
    capas_creyentes.append(copy.deepcopy(creyentes))
    #if len(A) == len_old:
    #  break
  return layer_i_nodes

def _diffuse_k_rounds(G, A, steps):
  tried_edges = set()
  layer_i_nodes = [ ]
  layer_i_nodes.append([i for i in A])
  capas_creyentes.append(copy.deepcopy(creyentes))
  #while steps > 0 and len(A) < len(G):
  while steps > 0 :
    len_old = len(A)
    (A, activated_nodes_of_this_round, cur_tried_edges) = \
        _diffuse_one_round(G, A, tried_edges)
    layer_i_nodes.append(activated_nodes_of_this_round)
    capas_creyentes.append(copy.deepcopy(creyentes))
    tried_edges = tried_edges.union(cur_tried_edges)
    #if len(A) == len_old:
     # break
    steps -= 1
  return layer_i_nodes

def _diffuse_one_round(G, A, tried_edges):
  activated_nodes_of_this_round = set()
  catolicos_este_round = set()
  protestantes_este_round = set()
  cur_tried_edges = set()
 
  for s in A:
    for nb in G.successors(s):
      #if nb in A or (s, nb) in tried_edges or (s, nb) in cur_tried_edges:
      #if  (s, nb) in cur_tried_edges:
      #  continue
      (conversion_echa, religion_resultado) = _prop_success(G,s,nb)
      if conversion_echa and religion_resultado == RELIGION_CATOLICA:
        activated_nodes_of_this_round.add(nb)
        catolicos_este_round.add(nb)
      if conversion_echa and religion_resultado == RELIGION_PROTESTANTE:
        protestantes_este_round.add(nb)
        activated_nodes_of_this_round.add(nb)
      cur_tried_edges.add((s, nb))
  activated_nodes_of_this_round = list(activated_nodes_of_this_round)
  A.extend(activated_nodes_of_this_round)
  return A, activated_nodes_of_this_round, cur_tried_edges

def validar_semillas(semillas):
      """
      Cada semilla debe pertenecer a una religion
      """
      for semilla in semillas:
            if(creyentes[semilla]['religion'] != RELIGION_CATOLICA and creyentes[semilla]['religion'] != RELIGION_PROTESTANTE):
                  raise "Error: La semilla " +  str(creyentes[semilla]['id']) + "no tiene religion"
            else:
                  continue

def cambiarse_a_catolica(nodo):
  creyentes[nodo]['religion'] = RELIGION_CATOLICA
  if(creyentes[nodo]['religion'] == RELIGION_CATOLICA):
      creyentes[nodo]['grad_transferencia'] =  creyentes[nodo]['grad_transferencia']
  else: 
    creyentes[nodo]['grad_transferencia'] =  creyentes[nodo]['grad_transferencia'] * \
    MULTIPLICADOR_TRANSFERENCIA_CATOLICA
  
def cambiarse_a_protestante(nodo):
  creyentes[nodo]['religion'] = RELIGION_PROTESTANTE
  nuevo_grad_transferencia = creyentes[nodo]['grad_transferencia'] * MULTIPLICADOR_TRANSFERENCIA_PROTESTANTE
  if (creyentes[nodo]['religion'] == RELIGION_PROTESTANTE):
    nuevo_grad_percepcion = creyentes[nodo]['grad_percepcion'] 
  else:
    nuevo_grad_percepcion = creyentes[nodo]['grad_percepcion'] * MULTIPLICADOR_PERCEPCION_PROTESTANTE
  creyentes[nodo]['grad_transferencia'] = nuevo_grad_transferencia if nuevo_grad_transferencia <= 1 else 1 
  creyentes[nodo]['grad_percepcion'] =   nuevo_grad_percepcion if nuevo_grad_percepcion <= 1 else 1

def _prop_success(G, src, dest):
      
      multiplicador_recistencia_percepcion = MULTIPLICADOR_RESISTENCIA_A_CONVERTIRSE_PROTESTANTE if \
      creyentes[src]['religion'] == RELIGION_PROTESTANTE else MULTIPLICADOR_RESISTENCIA_A_CONVERTIRSE_CATOLICO
      if(creyentes[src]['religion'] == creyentes[dest]['religion']):
            return False, -1
      if (random.random() <= G[src][dest]['relacion_personas']  and 
      random.random() <= creyentes[src]['grad_transferencia'] and 
      random.random() <= creyentes[dest]['grad_percepcion']  ): 
            if(creyentes[src]['religion'] == RELIGION_CATOLICA):
              cambiarse_a_catolica(dest)
              return True, RELIGION_CATOLICA
            if(creyentes[src]['religion'] == RELIGION_PROTESTANTE):
              cambiarse_a_protestante(dest)
              return True, RELIGION_PROTESTANTE
      else:
            return False, -1


      
class creyente(dict):
  """
  id = id del creyente leido de el archivo de texto
  grad_transferencia: probabilidad de que el nodo desee tratar de convencer a sus vecinos
  de su religion
  religion: 0 1 o 2, 0 no tiene 1 catolica, 2 protestante
  grad_transferencia: probablidad de que desee compartir sus creencias
  grad_percepcion = probabilidad de que cambie sus creencias por otras
  """
  def __init__(self):
    return None
  


#this method just reads the graph structure from the file
def buildG(G, file_, delimiter_):
    global Nodospajek
    global creyentes 
    creyentes = {}
    Nodospajek = []
    #construct the weighted version of the contact graph from cgraph.dat file
    #reader = csv.reader(open("/home/kazem/Data/UCI/karate.txt"), delimiter=" ")
    reader = csv.reader(open(file_), delimiter=delimiter_)
    Arcos = 0
    cont = 0
    for line in reader:
        if Arcos == 0 and  line[0] != "*Arcs" and cont != 0:
            Nodospajek.append(line)
            creyente_obj = creyente()
            creyente_obj['religion'] = int(line[4])
            creyente_obj['grad_transferencia'] = float(line[3])
            creyente_obj['grad_percepcion'] = float(line[2])
            creyente_obj['id'] = int(line[0])
            creyentes[int(line[0])] = creyente_obj  
        if Arcos == 1:
           if len(line) >  2:
              if float(line[2]) != 0.0:
                #line format: u,v,w
                G.add_edge(int(line[0]),int(line[1]),relacion_personas=float(line[2]))
           else:
            #line format: u,v
               G.add_edge(int(line[0]),int(line[1]),weight=1.0)
        if line[0] == "*Arcs" : Arcos = 1
        cont = 1    


def main(argv):
    
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <input graph>\n" % (argv[0],))
        return 1

    graph_fn = argv[1]
    G = nx.Graph()  #let's create the graph first
    buildG(G, graph_fn, ' ')
    
    Nodos = G.nodes()
     
    n = G.number_of_nodes()    #|V|
    print(n)
    
    inisi = 0
    while inisi == 0: inisi = random.randrange(n)
    print(inisi)

    diffusion = independent_cascade(G, [4,1], steps = 55)
    
    print(diffusion)
    print(creyentes)
    print (time.strftime("%I:%M:%S"))
    #pos = nx.spectral_layout(G)
    #pos = nx.circular_layout(G)
    #pos = nx.shell_layout(G)
    #pos = nx.random_layout(G,dim=2)
    pos=nx.fruchterman_reingold_layout(G, scale=1000)
    #pos = nx.spring_layout(G, scale=2000)
    
    cf = plt.figure(2, figsize=(15,15))
    ax = cf.add_axes((0,0,1,1))
    
    #fig = plt.gcf()
    
    labels={}
    cont = 1
    for i in G.nodes():
        colr = float(cont)/n
        nx.draw_networkx_nodes(G, pos, [i] , node_size = 100, node_color = 'w',  with_labels=True)
        labels[i] = i
        cont += 1
    nx.draw_networkx_labels(G,pos,labels,font_size=5)        
    nx.draw_networkx_edges(G,pos, alpha=0.5)

    plt.ion()
    plt.draw()
    infectados = 0
    sanos = n     
    conts = 0
    infect = []
    sucep = []
    tics = []
    infect.append(infectados)
    sucep.append(sanos)
    tics.append(conts)
    print(str(len(capas_creyentes)) + "vs " + str(len(diffusion)) )
    for x in range ( 0, len(diffusion)):
        #print(i)
        infectados = infectados + len(diffusion[x])
        sanos = sanos - len(diffusion[x])
        infect.append(infectados)
        sucep.append(sanos)
        conts = conts + 1
        tics.append(conts)
        #plt.pause(0.001)
        for node in diffusion[x]:
              if  capas_creyentes[x][node]['religion'] == RELIGION_CATOLICA:
                nx.draw_networkx_nodes(G, pos, [node] , node_size = 250, node_color = 'b', with_labels=True)
                plt.draw()
              if capas_creyentes[x][node]['religion'] == RELIGION_PROTESTANTE:
                nx.draw_networkx_nodes(G, pos, [node] , node_size = 250, node_color = 'r', with_labels=True)
                plt.draw()
                    
        #nx.draw_networkx_nodes(G, pos, diffusion2[x] , node_size = 250, node_color = 'b', with_labels=True)
        plt.pause(0.5)
    plt.pause(20)
    plt.subplot(2,2,1)
    plt.title('suceptibles')
    plt.xlabel('Tics')
    plt.ylabel('Nodos')
    plt.plot(tics,sucep,'r')
    plt.subplot(2,2,2)
    plt.title('infectados')
    plt.xlabel('Tics')
    plt.ylabel('Nodos')
    plt.plot(tics,infect,'g')
    plt.subplot(2,2,3)
    plt.title('infectados y Suceptibles')
    plt.xlabel('Tics')
    plt.ylabel('Nodos')
    plt.plot(tics,sucep)
    plt.plot(tics,infect)
    plt.show()

   
    plt.pause(20)
    # Animator call
    #anim = animation.FuncAnimation(fig, animate, frames=20, interval=20, blit=True)
    print(infect,sucep,tics)    
    # Creamos una figura
    blt.plot(infect,tics)
    blt.show()
    print (time.strftime("%I:%M:%S"))

if __name__ == "__main__":
    sys.exit(main(sys.argv))
