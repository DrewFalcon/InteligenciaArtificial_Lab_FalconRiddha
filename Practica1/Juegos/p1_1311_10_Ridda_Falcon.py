from game import (
    TwoPlayerGameState,
)
from heuristic import (
    simple_evaluation_function,
)
from tournament import (
    StudentHeuristic,
)
from reversi import (
    get_valid_moves, 
    enemy_captured_by_move,
    create_standard_board,
    )


def func_glob(n: int, state: TwoPlayerGameState) -> float:
    return n + simple_evaluation_function(state)


class Solution1(StudentHeuristic):
    def get_name(self) -> str:
        return "ruleta_neozelandesa"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        # let's use an auxiliary function
        state_actual = state.board
        color_yo = state.player_max.label
        if color_yo == "W":
            color_rival = "B"
        else:
            color_rival = "W"

        valores_esquina_yo = 0
        valores_esquina_rival = 0
        esquinas = [(1,1), (1,8), (8,1), (8,8)] #esquinas, valen mas
        bordes = [(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),
                  (8,2),(8,3),(8,4),(8,5),(8,6),(8,7),
                  (2,1),(3,1),(4,1),(5,1),(6,1),(7,1),
                  (2,8),(3,8),(4,8),(5,8),(6,8),(7,8)
                  ]
        for a in esquinas:
            if state_actual.get(a) == color_yo:
                valores_esquina_yo += 1
            elif state_actual.get(a) == color_rival:
                valores_esquina_rival += 1
        resultado_esquinas = valores_esquina_yo - valores_esquina_rival

        movimientos_yo = get_valid_moves(
            state_actual, 8, 8, color_yo, color_rival, 'O', False
        )
        movimientos_rival = get_valid_moves(
            state_actual, 8, 8, color_rival, color_yo, 'O', False
        )

        diferencia_movilidad = len(movimientos_yo) - len(movimientos_rival)

        bordes_yo = 0
        bordes_rival = 0

        for pos in bordes:
            if state_actual.get(pos) == color_yo:
                bordes_yo += 1
            elif state_actual.get(pos) == color_rival:
                bordes_rival += 1

        diferencia_bordes = bordes_yo - bordes_rival

        return (50 * resultado_esquinas
            + 5 * diferencia_movilidad
            + 2 * diferencia_bordes)
    



class Solution2(StudentHeuristic):

    def get_name(self) -> str:
        return "kiwi_australiano_borde"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        state_actual = state.board
        color_yo = state.player_max.label
        if color_yo == "W":
            color_rival = "B"
        else:
            color_rival = "W"

        fichas_yo = sum(1 for v in state_actual.values() if v == color_yo)
        fichas_rival = sum(1 for v in state_actual.values() if v == color_rival)
        diferencia_fichas = fichas_yo - fichas_rival

        movimientos_yo = get_valid_moves(
            state_actual, 8, 8, color_yo, color_rival, 'O', False
        )
        movimientos_rival = get_valid_moves(
            state_actual, 8, 8, color_rival, color_yo, 'O', False
        )

        diferencia_movilidad = len(movimientos_yo) - len(movimientos_rival)

        bordes_esquinas = [
            ((1, 1), [(1, 2), (2, 1)]),
            ((1, 8), [(1, 7), (2, 8)]),
            ((8, 1), [(7, 1), (8, 2)]),
            ((8, 8), [(7, 8), (8, 7)])
        ]

        bordes_yo = 0
        bordes_rival = 0

        for esquina, posiciones in bordes_esquinas:
            if state_actual.get(esquina) is None:
                for pos in posiciones:
                    if state_actual.get(pos) == color_yo:
                        bordes_yo += 1
                    elif state_actual.get(pos) == color_rival:
                        bordes_rival += 1

        diferencia_bordes = bordes_yo - bordes_rival

        return (
            diferencia_fichas
            + 5 * diferencia_movilidad
            - 5 * diferencia_bordes
        )


def dummy(n: int) -> int:
            return n + 1



class Solution3(StudentHeuristic):
    def get_name(self) -> str:
        return "Bordes_Peligrosos_con_un_poco_de_sal" 


    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        board = state.board
        color_yo = state.player_max.label
        color_rival = "B" if color_yo == "W" else "W"

        bloqueadas = 'O' #state.blocked_cell_label

        esquinas = [(1, 1), (1, 8), (8, 1), (8, 8)]

        # Bordes sin peligro
        bordes_left =   [(1,3), (1,4), (1,5), (1,6) ]
        bordes_right = [(8,3), (8,4), (8,5), (8,6) ]
        bordes_up = [(3,1), (4,1), (5,1), (6,1) ]
        bordes_down = [(3,8), (4,8), (5,8), (6,8) ]

        # Bordes que dejan al oponente tomar la esquina
        # y una vez que se hace esto cualquier linea que hubiese esta tomada ya
        bordes_upLeft_danger = [(1,2), (2,1), (2,2)]
        bordes_upRight_danger = [(7,1), (8, 2), (7,2)]
        bordes_downRight_danger = [(7,8), (8,7), (7,7)] 
        bordes_downLeft_danger = [(1,7), (2,8), (2,7)] 



        # Obtener cantidad de Movimientos del jugador
        mov_yo = get_valid_moves(board, 8, 8, color_yo, color_rival, bloqueadas, False)
        #num_mov_yo = len(mov_yo)
        # Obtener cantidad de movimientos del opponente
        mov_rival = get_valid_moves(board, 8, 8, color_rival, color_yo, bloqueadas, False)
        #num_mov_rival = len(mov_rival)

        # Obtener cantidad de piezas en las esquinas
        # malos puntos si en esquinas esta en mov legales del oponente 

        valores_esquina_yo = 0
        valores_esquina_rival = 0
        valores_posibles_esquina_yo = 0
        valores_posibles_esquina_rival = 0

        for a in esquinas:
            if board.get(a) == color_yo:
                valores_esquina_yo += 1
                if board.get(a) in mov_yo:
                    valores_posibles_esquina_yo += 1
            elif board.get(a) == color_rival:
                valores_esquina_rival += 1
                if board.get(a) in mov_rival:
                    valores_posibles_esquina_rival += 1



        # obtener cantidad de piezas en los bordes
            # BORDES SEGUROS

        valores_bordes_yo = 0
        valores_bordes_rival = 0

        for a in bordes_left + bordes_down + bordes_right + bordes_up:
            if board.get(a) == color_yo:
                valores_bordes_yo += 1
            elif board.get(a) == color_rival:
                valores_bordes_rival += 1


        valores_peligro_yo = 0
        valores_peligro_rival = 0


        for b in bordes_upLeft_danger:
            if (8, 8) not in board:
                if board.get(b) == color_yo:
                    valores_peligro_yo -= 1
                elif board.get(b) == color_rival:
                    valores_peligro_rival -= 1

        for b in bordes_upRight_danger:
            if (8, 8) not in board:
                if board.get(b) == color_yo:
                    valores_peligro_yo -= 1
                elif board.get(b) == color_rival:
                    valores_peligro_rival -= 1

        
        for b in bordes_downLeft_danger:
            if (8, 8) not in board:
                if board.get(b) == color_yo:
                    valores_peligro_yo -=1
                elif board.get(b) == color_rival:
                    valores_peligro_rival -= 1


        
        for b in bordes_downRight_danger:
            if (8, 8) not in board:
                if board.get(b) == color_yo:
                    valores_peligro_yo -= 1
                elif board.get(b) == color_rival:
                    valores_peligro_rival -= 1  


        return (  50 * (valores_esquina_yo - valores_esquina_rival) 
                + 30 * (valores_posibles_esquina_yo - valores_posibles_esquina_rival)
                + 20 * (valores_bordes_yo - valores_bordes_rival)
                + 20 * (valores_peligro_yo - valores_peligro_rival)) 
    
