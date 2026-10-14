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
                valores_esquina_yo += 1
            elif state_actual.get(a) == color_rival:
                valores_esquina_rival += 1
        resultado_esquinas = valores_esquina_yo - valores_esquina_rival

        for b in peligroso:
            if state_actual.get(b) == color_yo:
                valores_peligroso_yo+= 1
            elif state_actual.get(b) == color_rival:
                valores_peligroso_rival+= 1
        resultado_peligrosos = valores_peligroso_yo - valores_peligroso_rival
        return resultado_esquinas * 50 - resultado_peligrosos * 5
    


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
        diagonal_1 = [(3,3),(4,4),(5,5),(6,6)]
        diagonal_2 = [(6,3),(5,4),(4,5),(3,6)]
        sub_diagonal2= [(6,2),(5,3),(4,4),(3,5),(2,6),(7,3),(6,4),(5,5),(4,6),(3,7)]
        sub_diagonal1= [(2,3),(3,4),(4,5),(5,6),(6,7),(3,2),(4,3),(5,4),(6,5),(7,6)]
        otros_importantes=[(1,4),(1,5),(4,1),(5,1),(4,8),(5,8),(8,4),(8,5)]

        for a in esquinas:
            if state_actual.get(a) == color_yo:
                valores_esquina_yo += 1
            elif state_actual.get(a) == color_rival:
                valores_esquina_rival += 1
        resultado_esquinas = valores_esquina_yo - valores_esquina_rival
        for a in centro_muy_valioso:
            if state_actual.get(a) == color_yo:
                valores_centro_yo += 1
            elif state_actual.get(a) == color_rival:
                valores_centro_rival += 1
        resultado_centro = valores_centro_yo - valores_centro_rival
        for a in centro_valioso:
            if state_actual.get(a) == color_yo:
                valores_centroS_yo += 1
            elif state_actual.get(a) == color_rival:
                valores_centroS_rival += 1
        resultado_centroS = valores_centroS_yo - valores_centroS_rival
        for a in diagonal_1 + diagonal_2:
            if state_actual.get(a) == color_yo:
                valores_diagonalP_yo += 1
            elif state_actual.get(a) == color_rival:
                valores_diagonalP_rival += 1
        resultado_diagonalP = valores_diagonalP_yo - valores_diagonalP_rival
        for a in sub_diagonal1 + sub_diagonal2:
            if state_actual.get(a) == color_yo:
                valores_diagonalS_yo += 1
            elif state_actual.get(a) == color_rival:
                valores_diagonalS_rival += 1
        resultado_diagonalS = valores_diagonalS_yo - valores_diagonalS_rival
        for a in otros_importantes:
            if state_actual.get(a) == color_yo:
                valores_otros_yo += 1
            elif state_actual.get(a) == color_rival:
                valores_otros_rival += 1
        resultado_otros = valores_otros_yo - valores_otros_rival


        return resultado_esquinas * 30 + resultado_centro * 30 + resultado_centroS * 10 + resultado_diagonalP * 15 + resultado_diagonalS * 8 + resultado_otros * 6



    
class Solution3(StudentHeuristic):

    def get_name(self) -> str:
        return "solution3"

    def evaluation_function(self, state: TwoPlayerGameState) -> float:
        board = state.board
        color_yo = state.player_max.label
        color_rival = "B" if color_yo == "W" else "W"

        esquinas = [(1, 1), (1, 8), (8, 1), (8, 8)]

        valores_esquina_yo = 0
        valores_esquina_rival = 0

        for pos in esquinas:
            if board.get(pos) == color_yo:
                valores_esquina_yo += 1
            elif board.get(pos) == color_rival:
                valores_esquina_rival += 1

        return 30 * (valores_esquina_yo - valores_esquina_rival)
    
def dummy(n: int) -> int:
            return n + 1



class Solution4(StudentHeuristic):
    def get_name(self) -> str:
        return "solution4" #  En realidad es solucion 4 pero se mantiene asi para probar mas facil


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



        ######################################################
        # Obtener cantidad de fichas 

            # Obtener del jugador
            # Obtener del oponente




        ######################################################
        ######################################################

        # Obtener cantidad de Movimientos del jugador
        mov_yo = get_valid_moves(board, 8, 8, color_yo, color_rival, bloqueadas, False)
        num_mov_yo = len(mov_yo)
        # Obtener cantidad de movimientos del opponente
        mov_rival = get_valid_moves(board, 8, 8, color_rival, color_yo, bloqueadas, False)
        num_mov_rival = len(mov_rival)


        #print(f"Movimientos del jugador: {mov_yo}\n Movimientos del Enemigo: {mov_rival}")


        # Obtener cantidad de piezas en las esquinas
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


        # malos puntos si en esquinas esta en mov legales del oponente 




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





        # buenos(?) puntos si en esquinas esta en mov legales del oponente y esquina esta vacio(?)











        return (  50 * (valores_esquina_yo - valores_esquina_rival) 
                + 30 * (valores_posibles_esquina_yo - valores_posibles_esquina_rival)
                + 20 * (valores_bordes_yo - valores_bordes_rival)
                + 20 * (valores_peligro_yo - valores_peligro_rival)) 
                # + Valores de fichas totales?
    

    def dummy(n: int) -> int:
            return n + 1

