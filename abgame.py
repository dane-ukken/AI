import morrishelpers as helpers
import sys

static_estimator_call_count = 0


def alpha_beta_max_min(board, depth, max_depth, alpha, beta):
    global static_estimator_call_count
    if depth == max_depth:
        static_estimator_call_count += 1
        # getting moves for black
        black_moves_count = len(helpers.generate_moves_midgame_endgame(
            helpers.get_swapped_board(board)))
        return [helpers.get_static_estimate_for_midgame_endgame(board, black_moves_count), board]
    else:
        best_val = helpers.MINUS_INF
        best_list = [best_val, []]
        list_of_potential_boards = helpers.generate_moves_midgame_endgame(
            board)
        for potential_board in list_of_potential_boards:
            best_potential_result = alpha_beta_min_max(
                potential_board, depth + 1, max_depth, alpha, beta)
            if best_list[0] < best_potential_result[0]:
                best_list = [best_potential_result[0], potential_board]
            if best_list[0] >= beta:
                return best_list
            else:
                alpha = max(alpha, best_list[0])
        return best_list


def alpha_beta_min_max(board, depth, max_depth, alpha, beta):
    global static_estimator_call_count
    if depth == max_depth:
        static_estimator_call_count += 1
        # getting moves for black
        black_moves_count = len(helpers.generate_moves_midgame_endgame(
            helpers.get_swapped_board(board)))
        return [helpers.get_static_estimate_for_midgame_endgame(board, black_moves_count), board]
    else:
        swapped_board = helpers.get_swapped_board(board)
        best_val = helpers.INF
        best_list = [best_val, []]
        list_of_potential_boards = helpers.generate_moves_midgame_endgame(
            swapped_board)
        for potential_board in list_of_potential_boards:
            swapped_potential_board = helpers.get_swapped_board(
                potential_board)
            best_potential_result = alpha_beta_max_min(
                swapped_potential_board, depth + 1, max_depth, alpha, beta)
            if best_list[0] > best_potential_result[0]:
                best_list = [best_potential_result[0], swapped_potential_board]
            if best_list[0] <= alpha:
                return best_list
            else:
                beta = min(beta, best_list[0])
        return best_list


def main():
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    max_depth = int(sys.argv[3])

    input_string = helpers.get_input_string(input_file_path)
    board = []
    helpers.get_board_from_input_string(input_string, board)
    print("Input Board:")
    helpers.printBoard(board)
    optimum_list = alpha_beta_max_min(
        board, 0, max_depth, helpers.MINUS_INF, helpers.INF)
    print("Input Board Position: ", helpers.get_output_string_from_board(board))
    print("Static Estimate", optimum_list[0])
    print("Output Board Position: ",
          helpers.get_output_string_from_board(optimum_list[1]))
    print("Positions Evaluated", static_estimator_call_count)
    print("Output Board:")
    helpers.printBoard(optimum_list[1])
    helpers.write_output_string(
        helpers.get_output_string_from_board(optimum_list[1]), output_file_path)


# Call the main function
if __name__ == "__main__":
    main()
