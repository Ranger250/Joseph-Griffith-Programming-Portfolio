# Joseph Griffith

# Tic Tac Toe

# imports
import CommonGameFunctions as cgf
import random

# constants
MAX_SQUARES = 9
EMPTY_TOKEN = " "
X_TOKEN = "X"
O_TOKEN = "O"
human_player = "h"
comp_player = "c"

# functions list
# display_instructions
def display_inst():
    """displays the instructions for tic tac toe to the user. to us, type display_inst"""
    print(
        """
             Welcome to the greatest intellectual challenge of all time: Tic-Tac-Toe.
             This will be a showdown between your human brain and my silicon processor.
             You will make your move known by entering a number, 0 - 8. The number
             will correspond to the board position as illustrated:

                        1 | 2 | 3
                        ---------
                        4 | 5 | 6
                        ---------
                        7 | 8 | 9

            Prepare yourself, human. The ultimate battle is about to begin. \n
            """)
# new_board
def new_board():
    """create a new empty board full of empty tokens"""
    board = []
    for i in range(MAX_SQUARES):
        board.append(EMPTY_TOKEN)
    return board
# display board
def display_board(game_board):
    """displays the current state of he board to the user"""
    print(str.format("""
     {} | {} | {} 
    -----------
     {} | {} | {} 
    -----------
     {} | {} | {} 
    
    """, game_board[0], game_board[1], game_board[2],
                     game_board[3], game_board[4], game_board[5],
                     game_board[6], game_board[7], game_board[8]))
# assign tokens
def assign_tokens():
    global human_player
    global comp_player
    answer = cgf.ask_yes_no("Do you want to go first? ")
    if answer == "yes":
        human_player = X_TOKEN
        comp_player = O_TOKEN
        print("You are going to need any advantage you can get.")
    else:
        comp_player = X_TOKEN
        human_player = O_TOKEN
        print("Your kindness will be your down fall.")
    first_player = answer
    return first_player
# human move
def human_move(board, token):
    print("It's your turn you worthless human place your " + human_player)
    while True:
        pos = cgf.get_num_in_range("Where would you like to go", 1, 9) - 1
        if board[pos] == EMPTY_TOKEN:
            place_token(token, board, pos)
            break
        else:
            print("Are you blind or just stupid, there is already a token there you dope.")
# comp move
def comp_move(board, token, first_player, diff = "2 player"):
    # replace with AI
    pos_moves = legal_move(board)

    # Easy
    if diff == "Easy":
        spot = random.choice(pos_moves)
        print("Now it's my turn to show you how to play, I'll place my " + comp_player + " at " + str(spot+1))
        place_token(token, board, spot)

    # Medium
    if diff == "Medium":
        BEST_MOVES = (4, 0, 2, 6, 8, 1, 3, 5, 7)
        temp_board = board[:]
        # if comp can win
        for move in pos_moves:
            place_token(token, temp_board, move)
            if check_win(temp_board) == comp_player:
                spot = move
                print("Now it's my turn to show you how to play, I'll place my " + comp_player + " at " + str(spot + 1))
                place_token(token, board, spot)
                return
            else:
                temp_board[move] = EMPTY_TOKEN
        # if player can win
        for move in pos_moves:
            place_token(human_player, temp_board, move)
            if check_win(temp_board) == human_player:
                spot = move
                print("Now it's my turn to show you how to play, I'll place my " + comp_player + " at " + str(spot + 1))
                place_token(token, board, spot)
                return
            else:
                temp_board[move] = EMPTY_TOKEN

        for move in BEST_MOVES:
            if move in pos_moves:
                spot = move
                print("Now it's my turn to show you how to play, I'll place my " + comp_player + " at " + str(spot + 1))
                place_token(token, board, spot)
                return

    # impossible
    if diff == "Impossible":
        if first_player == "yes":
            BEST_MOVES = (4, 1, 3, 5, 7, 0, 2, 6, 8)
        else:
            BEST_MOVES = (0, 8, 2, 6, 1, 3, 5, 7)
        temp_board = board[:]
        # if comp can win
        for move in pos_moves:
            place_token(token, temp_board, move)
            if check_win(temp_board) == comp_player:
                spot = move
                print("Now it's my turn to show you how to play, I'll place my " + comp_player + " at " + str(spot + 1))
                place_token(token, board, spot)
                return
            else:
                temp_board[move] = EMPTY_TOKEN
        # if player can win
        for move in pos_moves:
            place_token(human_player, temp_board, move)
            if check_win(temp_board) == human_player:
                spot = move
                print("Now it's my turn to show you how to play, I'll place my " + comp_player + " at " + str(spot + 1))
                place_token(token, board, spot)
                return
            else:
                temp_board[move] = EMPTY_TOKEN

        for move in BEST_MOVES:
            if move in pos_moves:
                spot = move
                print("Now it's my turn to show you how to play, I'll place my " + comp_player + " at " + str(spot + 1))
                place_token(token, board, spot)
                return

    if diff == "2 player":
        print("Player 2 place your " + comp_player)
        while True:
            pos = cgf.get_num_in_range("Where would you like to go", 1, 9) - 1
            if board[pos] == EMPTY_TOKEN:
                place_token(token, board, pos)
                break
            else:
                print("Are you blind or just stupid, there is already a token there you dope.")
# legal move
def legal_move(board):
    moves = []
    for spot in range(len(board)):
        if board[spot] == EMPTY_TOKEN:
            moves.append(spot)
    return moves


# place_token
def place_token(token, board, pos):
    board[pos] = token
# check for win
def check_win(board):
    winner = ""
    WAYS_TO_WIN = ((0, 1, 2),
                   (3, 4, 5),
                   (6, 7, 8),
                   (0, 3, 6),
                   (1, 4, 7),
                   (2, 5, 8),
                   (0, 4, 8),
                   (2, 4, 6))
    for row in WAYS_TO_WIN:
        if board[row[0]] == board[row[1]] == board[row[2]] != EMPTY_TOKEN:
            winner = board[row[0]]
            return winner

    if EMPTY_TOKEN not in board:
        winner = "TIE"
        return winner

    return winner
# switch turn
def switch_turn(turn):
    if turn == X_TOKEN:
        turn = O_TOKEN
    else:
        turn = X_TOKEN
    return turn
# congrats winner
def congrats_winner(winner, human_player, comp_player):
    if winner != "TIE":
        print(winner, "is the winner\n")
    else:
        print("It's a Tie\n")
    if winner == comp_player:
        print("As I predicted, human, I am triumphant once more\n")
    elif winner == human_player:
        print("No! Nooo!!! It's not possible. You beat me! How did you cheat so well!?")
    else:
        print("How lucky you are that you managed to pull out a tie")


def main():
    winner = ""
    options = ["Easy", "Medium", "Impossible", "2 player"]
    diff = cgf.pick_from_menu(options)
    diff = options[diff - 1]
    # display instruction
    display_inst()
    # create board
    game_board = new_board()
    legal_move(game_board)
    # decide who is going first
    # give player tokens
    first_player = assign_tokens()
    # set turn to X
    turn = X_TOKEN
    # while playing (not 3 in a row and board has empty spaces)
    display_board(game_board)
    while not winner:
        # if turn is x
        if turn == human_player:
            # get x move
            # check that it is  legal move
            # place token
            human_move(game_board, human_player)
        # else
        else:
            # get o move
            # check that it is  legal move
            # place token
            comp_move(game_board, comp_player, first_player, diff)
        # check for win
        winner = check_win(game_board)
        # switch turn
        turn = switch_turn(turn)
        display_board(game_board)
    # congrats winner
    congrats_winner(winner, human_player, comp_player)


main()
