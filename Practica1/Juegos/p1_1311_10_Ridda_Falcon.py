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
        return "solution1"

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
        valores_peligroso_yo = 0
        valores_peligroso_rival = 0
        esquinas = [(1,1), (1,8), (8,1), (8,8)] #esquinas, valen mas
        peligroso = [(1,2), (2,1), (1,7), (2,8), (7,1), (8,2), (7,8), (8,7)] #peligroso puede regalar esquina
        for a in esquinas:
            if state_actual.get(a) == color_yo:
                valores_esquina_yo = self.dummy(valores_esquina_yo)
            elif state_actual.get(a) == color_rival:
                valores_esquina_rival = self.dummy(valores_esquina_rival)
        resultado_esquinas = valores_esquina_yo - valores_esquina_rival

        for b in peligroso:
            if state_actual.get(b) == color_yo:
                valores_peligroso_yo= self.dummy(valores_peligroso_yo)
            elif state_actual.get(b) == color_rival:
                valores_peligroso_rival= self.dummy(valores_peligroso_rival)
        resultado_peligrosos = valores_peligroso_yo - valores_peligroso_rival
        return resultado_esquinas * 30 - resultado_peligrosos * 10
    



    def dummy(self, n: int) -> int:
        return n + 1


class Solution2(StudentHeuristic):
    def get_name(self) -> str:
        return "solution2"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        state_actual = state.board
        color_yo = state.player_max.label
        if color_yo == "W":
            color_rival = "B"
        else:
            color_rival = "W"
        valores_esquina_yo = 0
        valores_esquina_rival = 0
        valores_centro_yo = 0
        valores_centro_rival = 0
        valores_centroS_yo = 0
        valores_centroS_rival = 0
        valores_diagonalP_yo = 0
        valores_diagonalP_rival = 0
        valores_diagonalS_yo = 0
        valores_diagonalS_rival = 0     
        valores_otros_yo = 0
        valores_otros_rival = 0 
        esquinas = [(1,1),(1,8),(8,1),(8,8)]
        centro_muy_valioso = [(4,4),(4,5),(5,4),(5,5)]
        centro_valioso =  [(3,3), (3,4), (3,5), (3,6), (4,3), (4,6), (5,3), (5,6), (6,3), (6,4), (6,5), (6,6)]
        diagonal_1 = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)]
        diagonal_2 = [(8,1),(7,2),(6,3),(5,4),(4,5),(3,6),(2,7),(1,8)]
        sub_diagonal2= [(7,1),(6,2),(5,3),(4,4),(3,5),(2,6),(1,7),(8,2),(7,3),(6,4),(5,5),(4,6),(3,7),(2,8)]
        sub_diagonal1= [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(2,1),(3,2),(4,3),(5,4),(6,5),(7,6),(8,7)]
        otros_importantes=[(1,4),(1,5),(4,1),(5,1),(4,8),(5,8),(8,4),(8,5)]

        for a in esquinas:
            if state_actual.get(a) == color_yo:
                valores_esquina_yo = self.dummy(valores_esquina_yo)
            elif state_actual.get(a) == color_rival:
                valores_esquina_rival= self.dummy(valores_esquina_rival)
        resultado_esquinas = valores_esquina_yo - valores_esquina_rival
        for a in centro_muy_valioso:
            if state_actual.get(a) == color_yo:
                valores_centro_yo= self.dummy(valores_centro_yo)
            elif state_actual.get(a) == color_rival:
                valores_centro_rival = self.dummy(valores_centro_rival)
        resultado_centro = valores_centro_yo - valores_centro_rival
        for a in centro_valioso:
            if state_actual.get(a) == color_yo:
                valores_centroS_yo = self.dummy(valores_centroS_yo)
            elif state_actual.get(a) == color_rival:
                valores_centroS_rival = self.dummy(valores_centroS_rival)
        resultado_centroS = valores_centroS_yo - valores_centroS_rival
        for a in diagonal_1 + diagonal_2:
            if state_actual.get(a) == color_yo:
                valores_diagonalP_yo = self.dummy(valores_diagonalP_yo)
            elif state_actual.get(a) == color_rival:
                valores_diagonalP_rival = self.dummy(valores_diagonalP_rival)
        resultado_diagonalP = valores_diagonalP_yo - valores_diagonalP_rival
        for a in sub_diagonal1 + sub_diagonal2:
            if state_actual.get(a) == color_yo:
                valores_diagonalS_yo = self.dummy(valores_diagonalS_yo)
            elif state_actual.get(a) == color_rival:
                valores_diagonalS_rival = self.dummy(valores_diagonalS_rival)
        resultado_diagonalS = valores_diagonalS_yo - valores_diagonalS_rival
        for a in otros_importantes:
            if state_actual.get(a) == color_yo:
                valores_otros_yo = self.dummy(valores_otros_yo)
            elif state_actual.get(a) == color_rival:
                valores_otros_rival = self.dummy(valores_otros_rival)
        resultado_otros = valores_otros_yo - valores_otros_rival


        return resultado_esquinas * 30 + resultado_centro * 30 + resultado_centroS * 10 + resultado_diagonalP * 15 + resultado_diagonalS * 8 + resultado_otros * 6

    def dummy(self, n: int) -> int:
            return n + 1

    
class Solution3(StudentHeuristic):

    def get_name(self) -> str:
        return "solution3"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        state_actual = state.board
        color_yo = state.player_max.label
        if color_yo == "W":
            color_rival = "B"
        else:
            color_rival = "W"
        valores_esquina_yo = 0
        valores_esquina_rival = 0
        esquinas = [(1, 1), (1, 8), (8, 1), (8, 8)]
        for a in esquinas:
                    if state_actual.get(a) == color_yo:
                        valores_esquina_yo= self.dummy(valores_esquina_yo)
                    elif state_actual.get(a) == color_rival:
                        valores_esquina_rival = self.dummy(valores_esquina_rival)
        resultado_esquinas = valores_esquina_yo - valores_esquina_rival
        resultado_movilidad = len(get_valid_moves(state_actual, 8, 8, color_yo, color_rival, None, True))
        return resultado_esquinas * 30 + resultado_movilidad *10
    
    def dummy(self, n: int) -> int:
            return n + 1