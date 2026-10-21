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
        state_actual = state.board
        color_yo = state.player_max.label
        if color_yo == "W":
            color_rival = "B"
        else:
            color_rival = "W"

        valores_esquina_yo = 0
        valores_esquina_rival = 0
        esquinas = [(1,1), (1,8), (8,1), (8,8)] #esquinas, valen mas
        bordes = [(1,3),(1,4),(1,5),(1,6),
                  (8,3),(8,4),(8,5),(8,6),
                  (3,1),(4,1),(5,1),(6,1),
                  (3,8),(4,8),(5,8),(6,8)
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

        bordes_peligrosos={(1,2),(2,1),(7,1),(7,8),(1,7),(2,8),(7,8),(8,7) }
        bordesp_yo = 0
        bordesp_rival = 0

        for pos in bordes_peligrosos:
            if state_actual.get(pos) == color_yo:
                bordesp_yo += 1
            elif state_actual.get(pos) == color_rival:
                bordesp_rival += 1

        diferencia_bordesp = bordesp_yo - bordesp_rival
        return (50 * resultado_esquinas
            + 5 * diferencia_movilidad
            + 3 * diferencia_bordes
            - 8 * diferencia_bordesp)
    



class Solution2(StudentHeuristic):

    def get_name(self) -> str:
        return "kiwi_australiano_bo"

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
        esquinas = [(1,1), (1,8), (8,1), (8,8)] #esquinas, valen mas

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
        
        fy = sum(1 for v in state_actual.values() if v == color_yo)
        fr = sum(1 for v in state_actual.values() if v == color_rival)
        n = fy + fr
        peso = -0.5 if n < 25 else (0.7 if n < 50 else 3.6)

        return (
            diferencia_fichas
            + 5 * diferencia_movilidad
            - 8 * diferencia_bordes
            + peso * (fy-fr)
        )


def dummy(n: int) -> int:
            return n + 1


def valor_movimiento(board, move,color, color_rival) -> float:
    x,y= move
    esquinas = {(1, 1), (1, 8), (8, 1), (8, 8)}
    casilla_diagonal= {(2, 2): (1, 1), (7, 2): (8, 1), (2, 7): (1, 8), (7, 7): (8, 8)}
    casilla_perpendicular= {(1, 2): (1, 1), (2, 1): (1, 1), (7, 1): (8, 1), (8, 2): (8, 1),
             (1, 7): (1, 8), (2, 8): (1, 8), (7, 8): (8, 8), (8, 7): (8, 8)}
    if move in esquinas:
        puntos = 50
    elif move in casilla_diagonal and casilla_diagonal[move] not in board:
        puntos = -25
    elif move in casilla_perpendicular and casilla_perpendicular[move] not in board:
        puntos = -10
    elif x in (1,8) or y in (1,8):
        puntos = 5
    else:
        puntos = 0
    conquista = enemy_captured_by_move(board, move, color, color_rival, 'O', False)
    return puntos + len(conquista)


class Solution3(StudentHeuristic):
    def get_name(self) -> str:
        return "delemon_dream_lions"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        state_actual = state.board
        color_yo = state.player_max.label
        if color_yo == "W":
            color_rival = "B"
        else:
            color_rival = "W"

        fichas_yo = sum(1 for v in state_actual.values() if v == color_yo)
        fichas_rival = sum(1 for v in state_actual.values() if v == color_rival)
        suma_fichas = fichas_yo + fichas_rival


        movimientos_yo = get_valid_moves(
            state_actual, 8, 8, color_yo, color_rival, 'O', False
        )
        movimientos_rival = get_valid_moves(
            state_actual, 8, 8, color_rival, color_yo, 'O', False
        )
        mejor_yo = 0
        for m in movimientos_yo:
            valor_aux = valor_movimiento(state_actual, m, color_yo, color_rival) 
            if valor_aux > mejor_yo:
                mejor_yo = valor_aux
        mejor_rival = 0
        if suma_fichas < 24:
            return 10 * len(movimientos_yo)- 10 * len(movimientos_rival)

        for m in movimientos_rival:
            valor_aux = valor_movimiento(state_actual, m, color_rival, color_yo) 
            if valor_aux > mejor_rival:
                mejor_rival = valor_aux
        movilidad = len(movimientos_yo) - len(movimientos_rival)
        return (mejor_yo - mejor_rival) + 5 * movilidad

