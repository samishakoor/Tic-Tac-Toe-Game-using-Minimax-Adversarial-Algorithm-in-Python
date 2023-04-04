from math import inf as infinity
from random import choice
import platform
import numpy as np
from os import system



Human = -1
Computer = +1
draw = 0



#Initialize empty board
board = np.zeros((3,3),dtype=np.int32)


def evaluate(curr_state):
    if wins(curr_state, Computer):
        score = +1
    elif wins(curr_state, Human):
        score = -1
    else:
        score = 0   
    return score


def wins(curr_state, player):

  horizontal_wins=[
        [curr_state[0][0], curr_state[0][1], curr_state[0][2]],
        [curr_state[1][0], curr_state[1][1], curr_state[1][2]],
        [curr_state[2][0], curr_state[2][1], curr_state[2][2]]
  ]
  vertical_wins=[
        [curr_state[0][0], curr_state[1][0], curr_state[2][0]],
        [curr_state[0][1], curr_state[1][1], curr_state[2][1]],
        [curr_state[0][2], curr_state[1][2], curr_state[2][2]]    
  ]

  diagonal_wins=[
        [curr_state[0][0], curr_state[1][1], curr_state[2][2]],
        [curr_state[2][0], curr_state[1][1], curr_state[0][2]]
  ]

  player_state=[player, player, player]

  if player_state in horizontal_wins:
    return True
  if player_state in vertical_wins:
    return True
  if player_state in diagonal_wins:
    return True
  return False



def game_over(curr_state):
    
    #human wins
    if wins(curr_state, Human):
        return True
    #computer wins
    elif wins(curr_state, Computer):
        return True
    # game drawn 
    elif len(empty_cells(curr_state)) == 0:
        return True
    return False
      

def empty_cells(curr_state):
    
    empty_cells_list = []
    for i in range(3):
        for j in range(3):
            if curr_state[i][j] == 0:
                empty_cells_list.append((i,j))
    return empty_cells_list


def valid_move(x,y):
    if (x, y) in empty_cells(board):
        return True
    else:
        return False

def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False
    
    
def minimax(curr_state, depth, player):
 
    if game_over(curr_state) or depth == 0:
        score = evaluate(curr_state)
        return [None, None, score]
    
    if player:   # maximizing player
        max_score = -infinity
        best_row, best_col = None, None
        for row, col in empty_cells(curr_state):
            curr_state[row][col] = Computer
            temp_row, temp_col, score = minimax(curr_state, depth-1, False)
            curr_state[row][col] = 0
            if score > max_score:
                max_score = score
                best_row, best_col = row, col
        return [best_row, best_col, max_score]
    
    else:   # minimizing player 
        min_score = +infinity
        best_row, best_col = None, None
        for row, col in empty_cells(curr_state):
            curr_state[row][col] = Human
            temp_row, temp_col, score = minimax(curr_state, depth-1, True)
            curr_state[row][col] = 0
            if score < min_score:
                min_score = score
                best_row, best_col = row, col
        return [best_row, best_col, min_score]
    


def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def printBoard(curr_state, comp_choice, human_choice):

    chars = {
        -1: human_choice,
        +1: comp_choice,
        0: ' '
    }
    str_line = '---------------'
    print('\n' + str_line)
    for row in curr_state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def computer_turn(comp_choice, human_choice):
   
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return
    
    print("\n ------------------------- Computer's turn -------------------------")
    if depth == 9:            # if computer has first turn
        x = choice([0,1,2])
        y = choice([0,1,2])
    else:
        computer_move = minimax(board, depth, Computer)
        x, y = computer_move[0], computer_move[1]
    
    set_move(x, y, Computer)
    printBoard(board, comp_choice, human_choice)


def human_turn(comp_choice, human_choice):

    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return
    
    print("\n ------------------------- Human's turn -------------------------\n")
    valid = False
    while not valid:
        human_move = input('Enter coordinates (x,y) : ')
        x,y = human_move.split(',')
        x = int(x)
        y = int(y)
        valid = valid_move(x,y)
        if not valid:
            print('Invalid move, try again.\n')
    set_move(x, y, Human)
    printBoard(board, comp_choice, human_choice)


def main():
   
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    h_choice = input('Choose X or O\nChosen: ').upper()
    
    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'
    
    # Ask human want to start first: Y or N
    clean()
    first = input('First to start?[y/n]: ').upper()

    while not game_over(board):
        if first == 'N':
            computer_turn(c_choice, h_choice)
            first = ''

        human_turn(c_choice, h_choice)
        computer_turn(c_choice, h_choice)

   
    if wins(board, Human):
        print('\nYOU WIN !')
    elif wins(board, Computer):
        print('\nYOU LOSE !')
    else:
        print('\nDRAW !')


 #Call main function here
if __name__ == '__main__':
    main()    
    
