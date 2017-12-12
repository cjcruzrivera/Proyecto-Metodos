# Proyecto-Metodos
Proyecto de propagación de ideas.
Ejemplo Religion.
Grupo de Trabajo:
Luis Gerardo Manrique Cardona
1327951
Camilo José Cruz Rivera
1428907


Formato entrada:

Primera linea:



*Arcs [Numero de actores]
[ID Actor] [Etiqueta] [Grado percepcion] [Grado transferencia] [Religion]


Colores: Protestantes = Rojos, Catolicos = Azules

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