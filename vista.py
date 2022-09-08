from tkinter import font
from turtle import color
import modelo as md
import tkinter as tk
from tkinter import ttk, scrolledtext

def init_window():
    """
    Crea la ventana y configura el tamaño.
    """
    global root
    global jugadores
    global board
    root = tk.Tk()
    root.title('Triqui: Alfa-Beta | Mini-Max')
    screen_width = 460
    screen_height = 660
    x_window = (root.winfo_screenwidth() - screen_width)//2
    y_window = ((root.winfo_screenheight() - screen_height)//2)-50
    posicion = str(screen_width) + 'x' + str(screen_height) + '+' + str(x_window) + '+' + str(y_window)
    root.geometry(posicion)
    root.resizable(0, 0)
    jugadores = {'X':None,'O':None}
    board = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]

def create_board():
    """
    Crea un tablero con un botón para iniciar el juego y tres botones para cada una de las nueve casillas del tablero.
    """
    global tab_control
    global board_section
    global etiqueta1
    tab_control = ttk.Notebook(root)
    board_section = tk.Frame(tab_control)
    etiqueta1 = ttk.Label(board_section, text = 'Jugar Triqui', font = ('sans-serif', 30))
    etiqueta1.grid(row = 0, column = 0, columnspan = 3)
    btnJuego = tk.Button(board_section, text='Jugar', font=('sans-serif', 20), command = new_game, background="pink", bd="0", fg="#ffffff")
    btnJuego.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    for fila in range(3,6):
        for column in range(3):
            board[fila-3][column] = tk.Button(board_section, text="", font=('consolas', 40), width=5, height=2, state=tk.DISABLED, disabledforeground='#000000', command=lambda fila=(fila-3), column=column: next_turn(fila, column))
            board[fila-3][column].grid(row=fila, column=column)
    tab_control.add(board_section, text='Jugar')
    tab_control.pack(fill='both')

def create_game_info():
    """
    Crea una pestaña en el widget del tablero y coloca en ella un widget de texto desplazado.
    """
    global seccion_informacion
    global scroll
    seccion_informacion = ttk.Labelframe(tab_control, text='Jugadas')
    tab_control.add(seccion_informacion, text='Información')
    scroll = scrolledtext.ScrolledText(seccion_informacion, width=55, height=35, wrap=tk.WORD)
    scroll.insert(tk.INSERT,"")
    scroll.config(state='normal')
    scroll.grid(row=0, column=0)

def create_game_settings():
    """
    Crea un marco, añade una etiqueta, un combobox, otra etiqueta, una entrada, y luego añade el marco al tablero.
    """
    global settings_section
    global lista_algoritmos
    global profundidad
    global maximizador
    cant_padding = 5
    settings_section = tk.Frame(tab_control)
    validar_tipo_dato = lambda text: text.isdecimal()
    ttk.Label(settings_section, font=('consolas', 15), text="Algoritmo").grid(row=0, column=0, padx=cant_padding, pady=cant_padding, sticky='W')
    lista_algoritmos = ttk.Combobox(settings_section, state='readonly', values=['Mini-Max','Alfa-Beta'])
    lista_algoritmos.current(0)
    lista_algoritmos.grid(row=0, column=1, columnspan=2, padx=cant_padding, pady=cant_padding)
    ttk.Label(settings_section, font=('consolas', 15), text="Maximizador").grid(row=1, column=0, padx=cant_padding, pady=cant_padding, sticky='W')
    maximizador = ttk.Combobox(settings_section, state='readonly', values=['Usuario', 'Máquina'])
    maximizador.current(1)
    maximizador.grid(row=1, column=1, padx=cant_padding, pady=cant_padding)
    ttk.Label(settings_section, font=('consolas', 15), text='Profundidad').grid(row=2,column=0, padx=cant_padding, pady=cant_padding, sticky='W')
    profundidad = ttk.Entry(settings_section, validate='key', validatecommand=(settings_section.register(validar_tipo_dato), '%S'))
    profundidad.insert(tk.END, '20')
    profundidad.grid(row=2, column=1, padx=cant_padding, pady=cant_padding,  sticky='W')
    tab_control.add(settings_section, text='Configuración')
    tab_control.pack(fill='both')

def get_board():
    """
    Crea un nuevo tablero que es una copia del tablero actual, pero con el texto de los botones en lugar de
    de los botones en sí mismos
    """
    global board
    board_algoritmo = [
              ['', '', ''],
              ['', '', ''],
              ['', '', '']
            ]
    for fila in range(3):
        for column in range(3):
            board_algoritmo[fila][column] = board[fila][column]['text']
    return board_algoritmo

def buttons_state(inicio_juego):
    """
    Si el juego no está iniciado, entonces desactiva todos los botones. Si el juego está iniciado, entonces habilite todos los
    botones.
    
    :param inicio_juego: Variable booleana que indica si el juego ha comenzado o no
    """
    for fila in range(3):
        for column in range(3):
            if not(inicio_juego):
                if board[fila][column]['state']=='normal':
                    board[fila][column]['state'] = 'disabled'
                else:
                    board[fila][column]['state'] = 'normal'
            else:
                board[fila][column].config(text="", state=tk.NORMAL, bg='#F0F0F0')


def update_info():
    global scroll
    scroll.insert(tk.INSERT, md.Algoritmo.impresion)

def set_player():
    """
    Establece el jugador, actualiza la información, y si el jugador es la máquina, ejecuta el algoritmo y
    hace el movimiento.
    """
    global jugadores
    global jugador
    global contador
    contador+=1
    md.Algoritmo.impresion += f"""
        Jugada # {contador}: Jugador - {jugadores[jugador]} 
       -------------------------------------------------------
    """

    # Actualizando información del juego.
    update_info()
    md.Algoritmo.clean_print()
    if jugadores[jugador] == 'Máquina':
        algoritmo = md.Algoritmo(get_board(),
                                 lista_algoritmos.get(),
                                 int(profundidad.get()),
                                 True if maximizador.get() == 'Máquina' else False)
        algoritmo.choose_best_move()
        fil = algoritmo.jugada[0]["Pos"][0] + 1
        col = algoritmo.jugada[0]["Pos"][1] + 1
        next_turn(fil-1, col-1)
    else:
        etiqueta1.config(text = ('Es tu turno'))

def new_game():
    """
    Sección para nuevo juego.
    """
    global jugadores
    global jugador
    global maximizador
    global lista_algoritmos
    global contador
    global scroll
    contador = 0
    md.Algoritmo.clean_print()
    scroll.destroy()
    tab_control.forget(2)
    create_game_info()
    jugadores["X"] = maximizador.get()
    jugadores["O"] = "Usuario" if jugadores["X"] == "Máquina" else "Máquina"
    usuario = "Maximizador ( X )" if maximizador.get() == "Usuario" else "Minimizador ( O )"
    maquina = "Maximizador ( X )" if maximizador.get()  == "Máquina" else "Minimizador ( O )"
    md.Algoritmo.impresion+=f"""\n-------------------------------------------------------
    \n\t\tINICIA LA PARTIDA
    \n-------------------------------------------------------\n
    \t   Usuario: {usuario} 
    \t   Máquina: {maquina} 
    \t   ALGORITMO: {lista_algoritmos.get()}
\n-------------------------------------------------------
    """
    jugador = "X"
    update_info()
    md.Algoritmo.clean_print()
    buttons_state(True)
    set_player()

def next_turn(fila, column):
    """
    Toma una lista de listas (una matriz) y una tupla de dos enteros (una posición) y devuelve una lista de
    tuplas de dos enteros (una lista de posiciones).
    
    :param fila: la fila de la tabla
    :param columna: la columna donde el jugador quiere poner la pieza
    """
    global jugadores
    global jugador
    global lista_algoritmos
    global maximizador
    global profundidad
    md.Algoritmo.clean_print()
    if board[fila][column]['text'] == '' and not(md.Estado.game_over(get_board())):
        board[fila][column]['text'] = jugador
        md.Algoritmo.impresion=f"""
        El jugador seleccionó la casilla ({fila+1}, {column+1})
        -------------------------------------------------------
        """
        end_of_game = md.Estado.game_over(get_board())
        if end_of_game is False:
            jugador = list(jugadores.keys())[0] if jugador == list(jugadores.keys())[1] else list(jugadores.keys())[1]
            set_player()
        elif end_of_game is True:
            if jugadores[jugador] == "Usuario":
                etiqueta1.config(text=('¡Tú ganas!'))
            else:
                etiqueta1.config(text = ('¡La ' + jugadores[jugador] + ' gana!'))
            buttons_state(False)
        elif end_of_game == 'Empate':
            etiqueta1.config(text = '¡Empate!')
            buttons_state(False)
        update_board()
        md.Estado.resetearID()
    else:
        md.Algoritmo.impresion+="""
        El jugador seleccionó una casilla ya ocupada
        """
    update_info()

def update_board():
    """
    Actualiza el tablero de juego.
    """
    global etiqueta1
    for fila in range(3):
        if board[fila][0]['text'] == board[fila][1]['text'] == board[fila][2]['text'] != '':
            board[fila][0].config(bg = 'green')
            board[fila][1].config(bg = 'green')
            board[fila][2].config(bg = 'green')
    for column in range(3):
        if board[0][column]['text'] == board[1][column]['text'] == board[2][column]['text'] != '':
            board[0][column].config(bg = 'green')
            board[1][column].config(bg = 'green')
            board[2][column].config(bg = 'green')
    if board[0][0]['text'] == board[1][1]['text'] == board[2][2]['text'] != '':
        board[0][0].config(bg = 'green')
        board[1][1].config(bg = 'green')
        board[2][2].config(bg = 'green')
    elif board[0][2]['text'] == board[1][1]['text'] == board[2][0]['text'] != '':
        board[0][2].config(bg = 'green')
        board[1][1].config(bg = 'green')
        board[2][0].config(bg = 'green')
    elif md.Estado.espacios_vacios(get_board()) is False and etiqueta1['text'] == '¡Empate!':
        for fila in range(3):
            for column in range(3):
                board[fila][column].config(bg = 'blue')

init_window()
create_board()
create_game_settings()
create_game_info()
root.mainloop()