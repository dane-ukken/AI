from typing import List
from collections import Counter
import sys


W = 'W'
B = 'B'
empty_value = 'x'
INF = float('inf')
MINUS_INF = float('-inf')

mill_dictionary = {
    0: [[6, 18]],
    1: [[11, 20]],
    2: [[7, 15]],
    3: [[10, 17]],
    4: [[8, 12]],
    5: [[9, 14]],
    6: [[0, 18], [7, 8]],
    7: [[6, 8], [2, 15]],
    8: [[6, 7], [4, 12]],
    9: [[5, 14], [10, 11]],
    10: [[9, 11], [3, 17]],
    11: [[1, 20], [9, 10]],
    12: [[4, 8], [13, 14]],
    13: [[16, 19], [12, 14]],
    14: [[12, 13], [5, 9]],
    15: [[16, 17], [2, 7]],
    16: [[15, 17], [13, 19]],
    17: [[15, 16], [3, 10]],
    18: [[0, 6], [19, 20]],
    19: [[18, 20], [13, 16]],
    20: [[1, 11], [18, 19]]
}

mill_positions_list = [
    [0, 6, 18], [1, 11, 20], [2, 7, 15], [4, 8, 12], [5, 9, 14], [3, 10, 17],
    [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20]
]


def count_potential_mill(board):
    potential_mill_count_white = 0
    potential_mill_count_black = 0
    for mill_positions in mill_positions_list:
        if board[mill_positions[0]] == board[mill_positions[1]] and board[mill_positions[2]] == empty_value:
            if board[mill_positions[0]] == B:
                potential_mill_count_black += 1
            elif board[mill_positions[0]] == W:
                potential_mill_count_white += 1
            else:
                continue
        if board[mill_positions[1]] == board[mill_positions[2]] and board[mill_positions[0]] == empty_value:
            if board[mill_positions[1]] == B:
                potential_mill_count_black += 1
            elif board[mill_positions[1]] == W:
                potential_mill_count_white += 1
            else:
                continue
        if board[mill_positions[0]] == board[mill_positions[2]] and board[mill_positions[1]] == empty_value:
            if board[mill_positions[0]] == B:
                potential_mill_count_black += 1
            elif board[mill_positions[0]] == W:
                potential_mill_count_white += 1
            else:
                continue
    potential_mill_count_list = [
        potential_mill_count_white, potential_mill_count_black]
    return potential_mill_count_list


neighbor_dictionary = {
    0: [1, 6],
    1: [0, 11],
    2: [3, 7],
    3: [2, 10],
    4: [5, 8],
    5: [4, 9],
    6: [0, 7, 18],
    7: [2, 6, 8, 15],
    8: [4, 7, 12],
    9: [5, 10, 14],
    10: [3, 9, 11, 17],
    11: [1, 10, 20],
    12: [8, 13],
    13: [12, 14, 16],
    14: [9, 13],
    15: [7, 16],
    16: [13, 15, 17, 19],
    17: [10, 16],
    18: [6, 19],
    19: [16, 18, 20],
    20: [11, 19],
}


def get_input_string(input_file_path):
    file_path = input_file_path
    with open(file_path, "r") as file:
        input_string = file.read()
    return input_string


def write_output_string(output_string, output_file_path):
    file_path = output_file_path
    with open(file_path, "w") as file:
        file.write(output_string)


def get_board_from_input_string(input_string, board):
    for c in input_string:
        board.append(c)


def get_output_string_from_board(board):
    output_string = ""
    for element in board:
        output_string += element
    return output_string


def get_swapped_board(board):
    swapped_board = [empty_value] * 21
    for i in range(len(board)):
        if board[i] == W:
            swapped_board[i] = B
        elif board[i] == B:
            swapped_board[i] = W
        else:
            swapped_board[i] = board[i]
    return swapped_board


def get_static_estimate_for_opening(board):
    counter = Counter(board)
    return counter[W] - counter[B]


def get_static_estimate_for_midgame_endgame(board, black_moves_count):
    counter = Counter(board)
    white_pieces_count, black_pieces_count = counter[W], counter[B]
    if black_pieces_count <= 2:
        return 10000
    elif white_pieces_count <= 2:
        return -10000
    elif black_moves_count == 0:
        return 10000
    else:
        return 1000*(white_pieces_count - black_pieces_count) - black_moves_count


def get_improved_static_estimate_for_opening(board):
    counter = Counter(board)
    white_pieces_count, black_pieces_count = counter[W], counter[B]
    potential_white_mills_count, potential_black_mills_count = count_potential_mill(
        board)
    if potential_white_mills_count == 0 and potential_black_mills_count == 1:
        return 1000*(white_pieces_count - black_pieces_count)

    return 1000*(white_pieces_count - black_pieces_count) + 50*(potential_white_mills_count - potential_black_mills_count)


def get_improved_static_estimate_for_midgame_endgame(board, black_moves_count):
    counter = Counter(board)
    white_pieces_count, black_pieces_count = counter[W], counter[B]
    if black_pieces_count <= 2:
        return 100000
    elif white_pieces_count <= 2:
        return -100000
    elif black_moves_count == 0:
        return 100000
    else:
        potential_white_mills_count, potential_black_mills_count = count_potential_mill(
            board)
        if potential_white_mills_count == 0 and potential_black_mills_count == 1:
            return 1000*(white_pieces_count - black_pieces_count) + 50*(get_close_mill_difference(board))
        if potential_white_mills_count == 1 and potential_black_mills_count == 1:
            potential_black_mills_count = 0
        return 1000*(white_pieces_count - black_pieces_count) + (-black_moves_count) + 50*(get_close_mill_difference(board)) + 2000*(potential_white_mills_count - potential_black_mills_count)


def close_mill(board, j):
    j_value = board[j]
    if j_value not in [B, W]:
        print('close_mill received X value')
        return
    list_of_neighbor_lists = mill_dictionary[j]

    for neighbor_list in list_of_neighbor_lists:
        if j_value == board[neighbor_list[0]] and j_value == board[neighbor_list[1]]:
            return True
    return False


def get_close_mill_difference(board):
    white_mill_count = 0
    black_mill_count = 0
    for i in range(len(board)):
        if board[i] == B:
            if close_mill(board, i):
                black_mill_count += 1
        if board[i] == W:
            if close_mill(board, i):
                white_mill_count += 1
    return white_mill_count - black_mill_count


def generate_remove(board, list_of_boards):
    has_added_board = False
    for location in range(len(board)):
        if board[location] == B:
            if not close_mill(board, location):
                board_copy = board[:]
                board_copy[location] = empty_value
                list_of_boards.append(board_copy)
                has_added_board = True

    if not has_added_board:
        list_of_boards.append(board)


def generate_add(board):
    list_of_boards = []
    for location in range(len(board)):
        if board[location] == empty_value:
            board_copy = board[:]
            board_copy[location] = W
            if close_mill(board_copy, location):
                generate_remove(board_copy, list_of_boards)
            else:
                list_of_boards.append(board_copy)
    return list_of_boards


def generate_moves_opening(board):
    list_of_boards = []
    list_of_boards = generate_add(board)
    return list_of_boards


def generate_move(board):
    list_of_boards = []
    for location in range(len(board)):
        if board[location] == W:
            neighbor_list = neighbor_dictionary[location]
            for neighbor_location in neighbor_list:
                if board[neighbor_location] == empty_value:
                    board_copy = board[:]
                    board_copy[location] = empty_value
                    board_copy[neighbor_location] = W
                    if close_mill(board_copy, neighbor_location):
                        generate_remove(board_copy, list_of_boards)
                    else:
                        list_of_boards.append(board_copy)
    return list_of_boards


def generate_hopping(board):
    list_of_boards = []
    for location in range(len(board)):
        if board[location] == W:
            for i in range(len(board)):
                if board[i] == empty_value:
                    board_copy = board[:]
                    board_copy[location] = empty_value
                    board_copy[i] = W
                    if close_mill(board_copy, i):
                        generate_remove(board_copy, list_of_boards)
                    else:
                        list_of_boards.append(board_copy)
    return list_of_boards


def generate_moves_midgame_endgame(board):
    counter = Counter(board)
    if counter[W] == 3:
        return generate_hopping(board)
    else:
        return generate_move(board)


def printBoard(board):
    print(board[18], "-----", board[19], "-----", board[20], sep='')
    print("|     |     |")
    print("| ", board[15], "---", board[16], "---", board[17], " |", sep='')
    print("| |   |   | |")
    print("| | ", board[12], "-", board[13], "-", board[14], " | |", sep='')
    print("| | |   | | |")
    print(board[6], "-", board[7], "-", board[8], "   ",
          board[9], "-", board[10], "-", board[11], sep='')
    print("| | |   | | |")
    print("| | ", board[4], "---", board[5], " | |", sep='')
    print("| |       | |")
    print("| ", board[2], "-------", board[3], " |", sep='')
    print("|           |")
    print(board[0], "-----------", board[1], sep='')
