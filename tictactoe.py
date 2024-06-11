"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_number = 0
    o_number = 0
    empty = True
    for row in board:
        for cell in row:
            if cell != EMPTY:
                empty = False
                if cell == X:
                    x_number += 1
                else:
                    o_number += 1
    if empty:
        player = X
    else:
        if x_number > o_number:
            player = O
        else:
            player = X

    return player

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    if terminal(board):
        return None
    else:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == EMPTY:
                    possible_actions.add((i,j))
        return possible_actions
            
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action")
    
    # Make a deep copy of the board
    new_board = copy.deepcopy(board)
    
    # Determine the current player
    Player = player(board)
    
    # Update the copied board with the action
    new_board[action[0]][action[1]] = Player
    
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    utility_ = utility(board)
    if utility_ == 1:
        return X
    elif utility_ == -1:
        return O
    elif utility_ == 0:
        return None 



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if all(cell != None for row in board for cell in row):
        return True
    else:       
        if board[2][0] == board[1][1] == board[0][2] != None:
            return True
         # Diagonal check (from top left to bottom right)
        if board[0][0] == board[1][1] == board[2][2] != None:
            return True
        #horizontais e verticais
        for i in range(len(board)):
            count_horizontal = 0
            count_vertical = 0            
            for j in range(len(board)):
                value = board[i][i]
                if board[i][j] == value != None:
                    count_horizontal += 1
                if board[j][i] == value != None:
                    count_vertical += 1
            if count_vertical == 3 or count_horizontal == 3 :
                return True
        return False

                 


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if board[2][0] == board[1][1] == board[0][2] != EMPTY:
        if board[2][0] == X:
            return 1
        else:
            return -1
         # Diagonal check (from top left to bottom right)
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        if board[0][0] == X:
            return 1
        else:
            return -1
        #horizontais e verticais
    for i in range(len(board)):
            count_horizontal = 0
            count_vertical = 0            
            for j in range(len(board)):
                value = board[i][i]
                if board[i][j] == value != EMPTY:
                    count_horizontal += 1
                if board[j][i] == value != EMPTY:
                    count_vertical += 1
            if count_vertical == 3 or count_horizontal == 3 :
                if value == X:
                    return 1
                else:
                    return -1
    return 0
        


def evaluate(board,alpha,beta):
    """
    Returns the optimal action for the current player on the board. 
    """
    if terminal(board):
        return utility(board)
    else: #vou retornar a melhor ação conforme o jogador(menor utility no caso do O e maior utility no caso do X)
        Player = player(board)
        if Player == X:
            maxEval = -float('inf')
            possible_actions = actions(board)
            for possible_action in possible_actions:
                evaluation = evaluate(result(board,possible_action),alpha,beta)
                maxEval = max(maxEval,evaluation)
                alpha = max(alpha,evaluation)
                if alpha >= beta:
                    break
            return maxEval
        else:
            minEval = float('inf')
            possible_actions = actions(board)
            for possible_action in possible_actions:
                evaluation = evaluate(result(board,possible_action),alpha,beta)
                minEval = min(minEval,evaluation)
                beta = min(beta,evaluation)
                if beta <= alpha:
                    break
            return minEval

               
def minimax(board):
    alpha = -float('inf')
    beta = float('inf')
    if terminal(board):
        return None  # If it's a terminal state, return None as there's no move to make
    
    Player = player(board)  # Determine the current player
    
    if Player == X:
        best_score = -float('inf')
    else:
        best_score = float('inf')
    
    best_action = None
    
    possible_actions = actions(board)
    for action in possible_actions:
        result_board = result(board, action)
        score = evaluate(result_board,alpha,beta)
        
        # For maximizing player (X), find the action with the highest score
        if Player == X and score > best_score:
            best_score = score
            best_action = action
        
        # For minimizing player (O), find the action with the lowest score
        elif Player == O and score < best_score:
            best_score = score
            best_action = action
    
    return best_action