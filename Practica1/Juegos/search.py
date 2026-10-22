"""Implementation of search functions for reversi.

    Authors:
        Alejandro Bellogin <alejandro.bellogin@uam.es>
"""

import search
import random

from timeit import default_timer as timer
from datetime import timedelta

import util
from reversi import (
    get_valid_moves, 
    enemy_captured_by_move,
    create_standard_board,
    )


class CornerReversiState:
    """
    This class defines the mechanics of a Reversi game.
    The task of recasting this game state as a search problem is left to
    the CornerReversiSearchProblem class.
    """

    def __init__(self, board: dict, player1='B', player2='W', cur_player='B', height=8, width=8, ignore_block_cells_in_captures: bool = False):
        "Creates a new CornerReversiState, very similar to Reversi."
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.blocked_cell_label = 'O'
        self.cur_player = cur_player
        self.height = height
        self.width = width
        self.ignore_block_cells_in_captures = ignore_block_cells_in_captures

    def isGoal(self, min_corners=1):
        """
          Checks to see if any of the players have conquered min_corners in the board.
        """
        corners = [self.board.get((1, 1)), self.board.get((1, self.height)),
                   self.board.get((self.width, 1)), self.board.get((self.width, self.height))]
        return corners.count(self.player1) + corners.count(self.player2) >= min_corners

    def legalMoves(self):
        """
          Returns a list of legal moves from the current state.
        """
        next_player = self.player2 if self.cur_player == self.player1 else self.player1
        return  get_valid_moves(self.board, self.height, self.width, self.cur_player, next_player, self.blocked_cell_label, self.ignore_block_cells_in_captures) # RETURN THE LIST OF VALID MOVES

    def result(self, move):
        """
          Returns a new board with the current state updated based on the provided move.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        result_board = self.board.copy()  # shallow copy is enough
        # show the move on the board
        adversary = self.player2 if self.cur_player == self.player1 else self.player1
        result_board[move] = self.cur_player
        # flip enemy
        for enemy in enemy_captured_by_move(self.board, move, self.cur_player, adversary, self.blocked_cell_label, self.ignore_block_cells_in_captures):
            result_board[enemy] =  self.cur_player # update the board
        return CornerReversiState(
            result_board, self.player1, self.player2, adversary,
            self.height, self.width, self.ignore_block_cells_in_captures) # RETURN THE NEW STATE CONSIDERING THE UPDATES

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '=='.
        """
        return self.board == other.board

    def __hash__(self):
        return hash(self.__getAsciiString())

    def __getAsciiString(self):
        """
          Returns a display string for the state
        """
        adversary = self.player2 if self.cur_player == self.player1 else self.player1
        moves = get_valid_moves(self.board, self.height, self.width, self.cur_player, adversary, self.blocked_cell_label, self.ignore_block_cells_in_captures)
        lines = []
        for y in range(0, self.height + 1):
            rowLine = ''
            for x in range(0, self.width + 1):
                if x > 0 and y > 0:
                    if (x, y) in moves:
                        rowLine = rowLine + self.board.get((x, y), '_',)
                    else:
                        rowLine = rowLine + self.board.get((x, y), '.',)
                if x == 0:
                    if y > 0:
                        rowLine = rowLine + str(y) + ' '
                if y == 0:
                    rowLine = rowLine + (chr(x+96) if x > 0 else '  ')
            lines.append(rowLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        raise NotImplementedError

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        raise NotImplementedError

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of tuples, 
        (successor, action), where 'successor' is a successor to the current
        state, and 'action' is the action required to get there.
        """
        raise NotImplementedError


class CornerReversiSearchProblem(SearchProblem):
    """
      Implementation of a SearchProblem for Reversi

      Each state is represented by an instance of a valid Reversi board.
      The problem is solved when at least one corner is captured.
    """

    def __init__(self, reversi_state: CornerReversiState):
        "Creates a new ReversiSearchProblem which stores search information."
        self.state = reversi_state

    def getStartState(self):
        return self.state

    def isGoalState(self, state):
        return state.isGoal(1)

    def getSuccessors(self, state):
        """
          Returns list of (successor, action) pairs where
          each succesor is a new board from the original state
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a))
        return succ


class AllCornersReversiSearchProblem(CornerReversiSearchProblem):
    """
      Implementation of a SearchProblem for Reversi

      Each state is represented by an instance of a valid Reversi board.
      The problem is solved when every corner is captured.
    """

    def isGoalState(self, state):
        return state.isGoal(4)


def build_game_tree(search_problem, max_depth):
    """
    Greates a game tree from a search problem until max_depth.
    
    Returns:
    root: the root node of the tree
    stats: a dictionary with the computed statistics
    """
    stats = {
        "nodes": 0,
        "leaves": 0,
        "max_depth": 0,
        "branching_sum": 0,
        "internal_nodes": 0,
        }


    # Okay first idea, create all possible end results of a position first
    # Num of total options (from player to enemy)
    # Max_ depth I will add for every child I create. For every for loop.

    # Gonna have to be a a recursive function(?)

    # Get initial state and create root node
    root_state = search_problem.getStartState()
    root = {
        'state': root_state,
        'depth': 0,
        'action': None,
        'children': []
    }

    # Initialize values
    stats['nodes'] = 1
    stats['max_depth'] = 0

    # Create Queue
    queue = util.Queue()
    queue.push(root)


    """
    VAMOS A INTENTAR HACER UNA SEQUENCIA DE BREADTH/ANCHURA FIRST EN VEZ DE PROFUNDIDAD
    1)Generate succesors in current move
    2)add max_depth 1

    3)create empty list of first sucesors UTILIZANDO COLAS QUEUE FIRST IN FIRST OUT
    4.1) create a counter for current uhhhhhhh nodes of this level


    4)for every succesor in succesors THAT ARENT AT END GAME:
        5.1) add += stats.nodes
        5)generate succesors
        6)add to list IF ITS NOT AT END GAME
        6.2) minus one to the counter
    7) add max depth 1
    8) if list isnt empty, 
        8.1) update the counter (which should be at 0), to reflect the CURRENT LEVEL OF NODES
        8.2) continue the loop at the new amount of things
    """

    # Expandir mientras haya nodos en la cola
    while not queue.isEmpty():
        node = queue.pop()
        current_depth = node['depth']

        # Only expanding if max depth hasnt been reached
        if current_depth < max_depth:
            successors = search_problem.getSuccessors(node['state'])

            if successors:

                stats['internal_nodes'] += 1
                stats['branching_sum'] += len(successors)

                for succ_state, action in successors:
                    child = {
                        'state': succ_state,
                        'depth': current_depth + 1,
                        'action': action,
                        'children': []
                    }
                    node['children'].append(child)
                    stats['nodes'] += 1
                    stats['max_depth'] = max(stats['max_depth'], current_depth + 1)
                    queue.push(child)

            # Else:  #es nodo hoja
                # stats['leaves'] += 1

    # Calculate leaves
    stats['leaves'] = stats['nodes'] - stats['internal_nodes']

    return root, stats


def depthFirstSearch(search_problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", search_problem.getStartState())
    print("Is the start a goal?", search_problem.isGoalState(search_problem.getStartState()))
    print("Start's successors:", search_problem.getSuccessors(search_problem.getStartState()))
    """
    num_visited = 0
    structure = util.Stack()
    structure.push([(search_problem.getStartState(), None)]) # DEFINE THE INITIAL STATE
    visited = []

    while not structure.isEmpty():
        path = structure.pop()
        current_state = path[-1][0] # INDEX THE CURRENT STATE

        if search_problem.isGoalState(current_state):
            return len(visited) + 1, [step[1] for step in path[1:]] # RETURN THE PATH OF STATES

        if current_state not in visited:
            visited.append(current_state)

            for successor in search_problem.getSuccessors(current_state):
                if successor[0] not in visited:
                    new_path = path + [successor] # CREATE THE NEW PATH OF STATES
                    structure.push(new_path)

    return num_visited, None


def breadthFirstSearch(search_problem):
    """Search the shallowest nodes in the search tree first."""

    #  Get initial state and 
    root_state = search_problem.getStartState()
    root = {
        'state': root_state,
        'depth': 0,
        'action': None,
        'parent': None
    }

    # Create Queue
    queue = util.Queue()
    queue.push(root)

    visited = []
    num_visited = 0

    # Expandir mientras haya nodos en la cola
    while not queue.isEmpty():
        node = queue.pop()
        current_depth = node['depth']
        current_state = node['state']


        if current_state in visited:
            continue # skipea this one

        visited.append(current_state)
        num_visited += 1

        if search_problem.isGoalState(node['state']):

            i = node
            path = []
            while i['parent'] is not None:
                path.append(i['action'])
                i = i['parent']
            path.reverse()
            return num_visited, path #node['parent'] # RETURN THE PATH OF STATES



        successors = search_problem.getSuccessors(node['state'])
        if successors:
            for succ_state, action in successors:
                child = {
                    'state': succ_state,
                    'depth': current_depth + 1,
                    'action': action,
                    'parent': node 
                        # Podria haber hecho que fuese una lista e ir haciendo
                        # parents = parents del node + node
                        # Pero temia que ocupase mucha memoria el crear varias 
                        # copias succesors por cada casilla y estado
                }

                queue.push(child)


    raise NotImplementedError



def nullHeuristic(state, search_problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def simpleHeuristic(state, search_problem=None):
    # it rewards states with more coins
    return len(state.board)

# Solucion kiwi_australiano_borde
def heuristic1(state, search_problem=None):
    "*** YOUR CODE HERE ***"

    state_actual = state.board
    
    #color_yo = state.player_max.label
    #if color_yo == "W":
    #    color_rival = "B"
    #else:
    #    color_rival = "W"

    color_yo    = state.player1
    color_rival = state.player2

    fichas_yo = sum(1 for v in state_actual.values() if v == color_yo)
    fichas_rival = sum(1 for v in state_actual.values() if v == color_rival)
    diferencia_fichas = fichas_yo - fichas_rival



    

    movimientos_yo = get_valid_moves(
        state_actual, state.height, state.width, color_yo, color_rival, state.blocked_cell_label, False
    )
    movimientos_rival = get_valid_moves(
        state_actual, state.height, state.width, color_rival, color_yo, state.blocked_cell_label, False
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


def heuristic2(state, search_problem=None):
    state_actual = state.board
    color_yo, color_rival = state.player1, state.player2

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


def heuristic3(state, search_problem=None):
        state_actual = state.board
        color_yo, color_rival = state.player1, state.player2

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


def aStarSearch(search_problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    #  Get initial state  
    root = search_problem.getStartState()

    # Create Queue
    queue = util.PriorityQueue() 
        # Se añadiran tuplas de
        # [valor funcion, valor real g, estado actual, camino recorrido]

    first_value = heuristic(root, search_problem)
    queue.push([0 + first_value, 0, root, []], first_value) 
    visited = [] 
    num_visited = 0

    while not queue.isEmpty():
        f, g, actual, camino = queue.pop()
        num_visited += 1

        if search_problem.isGoalState(actual):
            return num_visited, camino

        # Estados siguientes
        futures = search_problem.getSuccessors(actual)

        for future, action in futures:
            if future not in visited:
                nuevo_g = g + 1 # En reversi el coste es un paso (1)
                nuevo_f = nuevo_g + heuristic(future, search_problem)

                queue.push([nuevo_f, nuevo_g, future, (camino + [action]) ], nuevo_f)

        visited.append(actual)


    raise NotImplementedError


def createRandomReversiGeneralState(moves, h, w):
    puzzle = CornerReversiState(create_standard_board(h, w, 'B', 'W'), height=h, width=w)
    for _ in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle


def createSmallRandomReversiState(moves=10):
    """
      moves: number of random moves to apply

      Creates a random Othello board by applying
      a series of 'moves' random moves to a solved
      board. The size of the board is smaller than
      the default board.
    """
    return createRandomReversiGeneralState(moves, 6, 6)


def createRandomReversiState(moves=100):
    """
      moves: number of random moves to apply

      Creates a random Othello board by applying
      a series of 'moves' random moves to a solved
      board.
    """
    return createRandomReversiGeneralState(moves, 8, 8)


if __name__ == '__main__':
    ## variables to play with
    iterations_initial_state = 0
    create_small_board = True
    print_steps = False
    ##

    if create_small_board:
        reversi_state = createSmallRandomReversiState(iterations_initial_state)
    else:
        reversi_state = createRandomReversiState(iterations_initial_state)

    print('Initial state after %d iterations:' % (iterations_initial_state))
    print(reversi_state)

    problem = CornerReversiSearchProblem(reversi_state)
    # for question 1.7
    # problem = AllCornersReversiSearchProblem(reversi_state)
    print('Problem to be solved: %s' % (problem.__class__))

    # game tree
    for depth in [1, 2, 3, 4]:
        root, stats = build_game_tree(problem, depth)
        print('Depth', depth, '\t', stats)


    # search methods
    for method in ['DFS', 'BFS']:
        start = timer()
        if method == 'DFS':
            visited, path = depthFirstSearch(problem)
            # Saltado depth First Search Por ahora...

        elif method == 'BFS':
            visited, path = breadthFirstSearch(problem)
        end = timer()

        if path:
            print_path = [(chr(x+96), y) for x, y in path]
            print('%s found a path of %d moves visiting %d nodes in %s: %s' %
                  (method, len(path), visited, str(timedelta(seconds=end - start)), str(print_path)))
            
            if print_steps:
                curr = reversi_state
                i = 1
                for a in path:
                    cur_player = curr.cur_player
                    curr = curr.result(a)
                    print_a = (chr(a[0]+96), a[1])
                    print('After %d move%s by %s: %s' % (i, ("", "s")[i > 1], cur_player, print_a))
                    print(curr)
        else:
            print('%s found no path in %s' % (method, str(timedelta(seconds=end - start))))

    for h in [
        simpleHeuristic,
        heuristic1,
        heuristic2,
        heuristic3,
        ]:
        method = 'A* with ' + h.__name__
        start = timer()
        visited, path = aStarSearch(problem, h)
        end = timer()

        if path:
            print_path = [(chr(x+96), y) for x, y in path]
            print('%s found a path of %d moves visiting %d nodes in %s: %s' %
                    (method, len(path), visited, str(timedelta(seconds=end - start)), str(print_path)))

            if print_steps:
                curr = reversi_state
                i = 1
                for a in path:
                    cur_player = curr.cur_player
                    curr = curr.result(a)
                    print_a = (chr(a[0]+96), a[1])
                    print('After %d move%s by %s: %s' % (i, ("", "s")[i > 1], cur_player, print_a))
                    print(curr)
        else:
            print('%s found no path in %s' % (method, str(timedelta(seconds=end - start))))
