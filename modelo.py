import math
from copy import copy as cp

class Estado(): # Clase que representa el estado del juego.

    VALOR_ASCII_BASE = 64
    valor_id_actual = list([VALOR_ASCII_BASE])

    def __init__(self, board):
        self._id = self._generarId()
        self._padre = None
        self._board = list(board.copy())
        self.hijos = []

    def __str__(self):
        return f'Estado {self._id,}: {self._board}'

    @classmethod
    def resetearID(cls):
        cls.valor_id_actual = list([cls.VALOR_ASCII_BASE])

    @property
    def id(self):
        return self._id

    @property
    def board(self):
        return list(self._board)

    @property
    def padre(self):
        return self._padre

    @padre.setter
    def padre(self, padre):
        self._padre = padre

    @classmethod
    def espacios_vacios(cls, board):
        espacios = 9
        for fila in range(3):
            for columna in range(3):
                if board[fila][columna] != '':
                    espacios -= 1
        if espacios == 0:
            return False
        else:
            return True
    @classmethod
    def game_over(cls, board):
        for fila in range(3):
            if board[fila][0] == board[fila][1] == board[fila][2] != '':
                return True
        for columna in range(3):
            if board[0][columna] == board[1][columna] == board[2][columna] != '':
                return True
        if board[0][0] == board[1][1] == board[2][2] != '':
            return True
        elif board[0][2] == board[1][1] == board[2][0] != '':
            return True
        elif not(cls.espacios_vacios(board)):
            return 'Empate'
        else:
            return False

    def who_wins(self):
        for fila in range(3):
            if self.board[fila][0] == self.board[fila][1] == self.board[fila][2] != '':
                return self.board[fila][0]
        for columna in range(3):
            if self.board[0][columna] == self.board[1][columna] == self.board[2][columna] != '':
                return self.board[0][columna]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        elif not(self.espacios_vacios(self.board)):
            return 'Empate'
        else:
            return ''

    def mostrar(self):
        salida = ""
        id_hijos = [str(hijo.id) for hijo in self.hijos.values() if len(self.hijos)!=0]
        salida+=f'\n\tEstado {self.id}'+"\nboard\n"
        for i in range(len(self.board)):
            if i in [0]:
                salida+="\t "
            if i not in [3, 6, 9]:
                salida += f"{self.board[i]}  "
            else:
                salida += f"\n \t {self.board[i]}  "
        salida+=f'\nPadre: {self.padre}'
        salida+=f'\nHijos: {id_hijos}\n'
        return salida

    def _generarId(self):
        if self.valor_id_actual[len(self.valor_id_actual)-1] < 90:
            self.valor_id_actual[len(self.valor_id_actual)-1] += 1
        else:
            if len(self.valor_id_actual) == 1:
                self.valor_id_actual[0] = self.VALOR_ASCII_BASE+1
                self.valor_id_actual.append(self.VALOR_ASCII_BASE+1)
            else:
                i = len(self.valor_id_actual) - 1
                while i >= 0 and self.valor_id_actual[i] == 90:
                    self.valor_id_actual[i] = self.VALOR_ASCII_BASE+1
                    i -= 1
                if i >= 0 and not(self.valor_id_actual[i] == 90):
                    self.valor_id_actual[i] += 1
                else:
                    self.valor_id_actual.append(self.VALOR_ASCII_BASE + 1)
        return "".join([chr(elemento) for elemento in self.valor_id_actual])

class Algoritmo():

    puntajes = {'X': 1, 'O': -1, 'Empate': 0}
    nodos_generados = 0
    impresion = ""
    contenido = ""

    def __init__(self, board, algoritmo, profundidad, maximizador):
        self.board = board
        self.algoritmo = algoritmo
        self.profundidad = profundidad
        self.maximizador = maximizador
        self.estado_inicial = Estado(self.board)
        self.nodos_ejecucion = 0
        self.estados = list()
        self.jugadas = list()
        self.jugada = None
        self.estados.append(self.estado_inicial)

    @classmethod
    def restart_nodos(cls):
        cls.nodos_generados = 0

    @classmethod
    def clean_print(cls):
        cls.impresion = ""

    @classmethod
    def clear_content(cls):
        cls.contenido = ""

    def _obtener_sucesores(self, estado_actual, maximizador):
        sucesores = []
        for i in range(3):
            for j in range(3):
                if estado_actual.board[i][j] == '':
                    matriz = [elem[:] for elem in estado_actual.board]
                    sucesor = Estado(matriz)
                    sucesor.padre = estado_actual
                    sucesor.board[i][j] = 'X' if maximizador else 'O'
                    sucesores.append(sucesor)
                    self.estados.append(sucesor)
                    self.jugadas.append({'Pos':(int(i),int(j)), 'board':list(sucesor.board).copy()})
        return sucesores

    def choose_best_move(self):
        mejor_puntaje = -math.inf if self.maximizador else math.inf
        sucesores = self._obtener_sucesores(self.estado_inicial, self.maximizador)
        for sucesor in sucesores:
            if self.algoritmo == 'Mini-Max':
                puntaje = self._minimax(sucesor, self.profundidad, not(self.maximizador))
            else:
                puntaje = self._alfabeta(sucesor, self.profundidad, -math.inf, math.inf, not(self.maximizador))
            if self.maximizador:
                if puntaje > mejor_puntaje:
                    mejor_puntaje = puntaje
                    self.jugada = list(elem for elem in self.jugadas if elem['board'] == sucesor.board)
            else:
                if puntaje < mejor_puntaje:
                    mejor_puntaje = puntaje
                    self.jugada = list(elem for elem in self.jugadas if elem['board'] == sucesor.board)
        self.nodos_ejecucion = len(self.estados)
        self.nodos_generados+=self.nodos_ejecucion

    def _minimax(self, estado, profundidad, es_maximizador):
        fin_juego = estado.who_wins()
        if fin_juego != '' or profundidad == 0:
            return self.puntajes[fin_juego]

        if es_maximizador:
            maximo_puntaje = -math.inf
            sucesores = self._obtener_sucesores(estado, es_maximizador)
            for sucesor in sucesores:
                puntaje = self._minimax(sucesor, profundidad-1, False)
                maximo_puntaje = max(maximo_puntaje, puntaje)
            return maximo_puntaje
        else:
            minimo_puntaje = math.inf
            sucesores = self._obtener_sucesores(estado, es_maximizador)
            for sucesor in sucesores:
                puntaje = self._minimax(sucesor, profundidad-1, True)
                minimo_puntaje = min(minimo_puntaje, puntaje)
            return minimo_puntaje


    def _alfabeta(self, estado, profundidad, alfa, beta, es_maximizador):
        fin_juego = estado.who_wins()
        if fin_juego != '' or profundidad == 0:
            return self.puntajes[fin_juego]

        if es_maximizador:
            maximo_puntaje = -math.inf
            sucesores = self._obtener_sucesores(estado, es_maximizador)
            for sucesor in sucesores:
                puntaje = self._alfabeta(sucesor, profundidad-1, alfa, beta, False)
                maximo_puntaje = max(maximo_puntaje, puntaje)
                alfa = max(alfa, puntaje)
                if beta <= alfa:
                    break
            return maximo_puntaje
        else:
            minimo_puntaje = math.inf
            sucesores = self._obtener_sucesores(estado, es_maximizador)
            for sucesor in sucesores:
                puntaje = self._alfabeta(sucesor, profundidad-1, alfa, beta, True)
                minimo_puntaje = min(minimo_puntaje, puntaje)
                beta = min(beta, puntaje)
                if beta <= alfa:
                    break
            return minimo_puntaje