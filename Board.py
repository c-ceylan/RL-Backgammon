from Piece import Piece

from copy import deepcopy

class Board():
    def __init__(self):
        self.pieces = [Piece(1, 1), Piece(1, 1), 
                       Piece(6, 0), Piece(6, 0), Piece(6, 0), 
                       Piece(6, 0), Piece(6, 0),
                       Piece(8, 0), Piece(8, 0), Piece(8, 0), 
                       Piece(12, 1), Piece(12, 1), Piece(12, 1), 
                       Piece(12, 1), Piece(12, 1), 
                       Piece(13, 0), Piece(13, 0), Piece(13, 0), 
                       Piece(13, 0), Piece(13, 0),
                       Piece(17, 1), Piece(17, 1), Piece(17, 1),
                       Piece(19, 1), Piece(19, 1), Piece(19, 1), 
                       Piece(19, 1), Piece(19, 1), 
                       Piece(24, 0), Piece(24, 0)]
        
        self.update_board()
    
    
    def get_board(self, pieces):
        pos_dict = {i : [] for i in range(1, 25)}
        
        broken_pieces = {0: 0, 1: 0}
        won_pieces = {0: 0, 1: 0}
        
        for piece in pieces:
            if piece.pos == -1:
                broken_pieces[piece.color] += 1
                
            elif piece.pos == 0:
                won_pieces[1] += 1
                
            elif piece.pos == 25:
                won_pieces[0] += 1
                
            else:
                pos_dict[piece.pos].append(piece)
                
        return pos_dict, broken_pieces, won_pieces
    
    def update_board(self):
        pos_dict, broken_pieces, won_pieces = self.get_board(self.pieces)
        
        self.pos_dict = pos_dict
        self.broken_pieces = broken_pieces
        self.won_pieces = won_pieces


    def check_won(self):
        # White/0 win.
        if self.won_pieces[0] == 15:
            return 0
        # Black/1 win.
        elif self.won_pieces[1] == 15:
            return 1
        else:
            return -1
    
    def board_encoded(self):
        board = []
        
        for i in range(1, 25):
            l_pieces = len(self.pos_dict[i])
            
            if l_pieces > 0:
                color = self.pos_dict[i][0].color
                col_list = [color]*l_pieces + [-1]*(15-l_pieces)
                
            else:
                col_list = [-1]*15
                
            board.append(col_list[:])
            
        return board
    
    def board_str(self):
        # Get Column, Row Representation
        def gcrr(pos_dict, col, row):
            black, white, empty = " @  ", " O  ", "    "

            if len(pos_dict[col]) < row:
                return empty
            else:
                if pos_dict[col][0].color == 0:
                    return white
                elif pos_dict[col][0].color == 1:
                    return black
        
        pd = self.pos_dict
        max_row = max(5, max([len(val) for val in self.pos_dict.values()]))
        
        
        board_rep = '\n\n'
        
        #                13  14  15  16  17  18    19  20  21  22  23  24
        board_rep += "| --- --- --- --- --- --- | --- --- --- --- --- --- |\n"
        
        for r in range(1, max_row+1):
            board_rep += f'| {gcrr(pd, 13, r)}{gcrr(pd, 14, r)}{gcrr(pd, 15, r)}'
            board_rep += f'{gcrr(pd, 16, r)}{gcrr(pd, 17, r)}{gcrr(pd, 18, r)}| '
            board_rep += f'{gcrr(pd, 19, r)}{gcrr(pd, 20, r)}{gcrr(pd, 21, r)}'
            board_rep += f'{gcrr(pd, 22, r)}{gcrr(pd, 23, r)}{gcrr(pd, 24, r)}|\n'
        
        board_rep += f'| {"    "*6}|{"    "*6} |\n'
        board_rep += "| --- --- --- --- --- --- | --- --- --- --- --- --- |\n"
        board_rep += f'| {"    "*6}|{"    "*6} |\n'
        
        for r in range(max_row, 0, -1):
            board_rep += f'| {gcrr(pd, 12, r)}{gcrr(pd, 11, r)}{gcrr(pd, 10, r)}'
            board_rep += f'{gcrr(pd, 9, r)}{gcrr(pd, 8, r)}{gcrr(pd, 7, r)}| '
            board_rep += f'{gcrr(pd, 6, r)}{gcrr(pd, 5, r)}{gcrr(pd, 4, r)}'
            board_rep += f'{gcrr(pd, 3, r)}{gcrr(pd, 2, r)}{gcrr(pd, 1, r)}|\n'
        
        board_rep += "| --- --- --- --- --- --- | --- --- --- --- --- --- |\n"
        #                12  11  10   9   8   7     6   5   4   3   2   1
        
        board_rep += "\n\n"
        
        board_rep += f"Broken Pieces: \nO: {self.broken_pieces[0]}\n\
@: {self.broken_pieces[1]}\n"
        board_rep += f"\nWon Pieces: \nO: {self.won_pieces[0]}\n\
@: {self.won_pieces[1]}\n"
        
        return board_rep
    
    def __repr__(self):
        return self.board_str()
    
    def __eq__(self, other):
        return (self.pos_dict == other.pos_dict
                ) and (self.broken_pieces == other.broken_pieces
                       ) and (self.won_pieces == other.won_pieces)
    
    def make_move(self, col_from, col_to, pieces):
        target_full = False
        
        for piece in pieces:
            if piece.pos == col_from:
                color = piece.color
                
                if color == 0:
                    if ((col_to >= col_from) or (col_from-col_to > 6)):
                        raise ValueError('Invalid Move Requested.')
                else:
                    if ((col_to <= col_from) or (col_to-col_from > 6)):
                        raise ValueError('Invalid Move Requested.')
                break
            
        for piece2 in pieces:
            if piece2.pos == col_to:
                if piece2.color == color:
                    break
                else:
                    if target_full:
                        raise ValueError('Invalid Move Requested.')
                    else:
                        piece_to_break = piece2
                        target_full = True
        
        piece.update_pos(col_to)
        
        if target_full:
            piece_to_break.update_pos(-1)
            
    
    def make_move_on_board(self, col_from, col_to):
        self.make_move(col_from, col_to, self.pieces)
        self.update_board()
    
    
    # Returns a list of all possible moves.
    def get_all_moves(self, dice1, dice2, color):
        
        all_possible_moves = []
        
        def get_pos_info(pos_idx, pos_dict):
            # Returns (pos_color, no_pieces).
            
            # Empty position.
            if len(pos_dict[pos_idx]) == 0:
                return -1, 0
            else:
                return pos_dict[pos_idx][0].color, len(pos_dict[pos_idx])
        
        
        # Check if a move is valid given piece, dice and board.
        # If not, return None.
        # If so, return current column and target column.
        def check_valid_move(piece, dice, current_board_pieces):
            current_pos_dict, current_broken_pieces, \
                current_won_pieces = self.get_board(current_board_pieces)
            
            # There is a broken piece, see if it can exit.
            if current_broken_pieces[color] > 0:
                # If the piece being checked is broken.
                if piece.pos == -1:
                    # If it allows exit.
                    if color == 0:
                        target_col = 25-dice
                    else:
                        target_col = dice
                        
                    target_col_pos = get_pos_info(target_col, 
                                                  current_pos_dict)
                    
                    # Valid if Empty or 1-Occupied or Same Color
                    empty_col = (target_col_pos[0] == -1)
                    same_color = (target_col_pos[0] == color)
                    one_occupied = ((target_col_pos[0] != color
                                     ) and (target_col_pos[1] == 1))
                    
                    if empty_col or same_color or one_occupied:
                        return [piece.pos, target_col]
                    else:
                        return None
                else:
                    return None
            
            # No broken pieces, check if target column is available.
            else:
                if color == 0:
                    target_col = piece.pos-dice
                else:
                    target_col = piece.pos+dice
                
                # Regular Move
                if (0 < target_col < 25):
                    target_col_pos = get_pos_info(target_col, 
                                                  current_pos_dict)
                    
                    # Valid if Empty or 1-Occupied or Same Color
                    empty_col = (target_col_pos[0] == -1)
                    same_color = (target_col_pos[0] == color)
                    one_occupied = ((target_col_pos[0] != color
                                     ) and (target_col_pos[1] == 1))
                    
                    if empty_col or same_color or one_occupied:
                        return [piece.pos, target_col]
                    else:
                        return None
                
                
                # Piece is Won. Check if valid.
                else:
                    # Exact roll, can exit, if all are in House.
                    if ((color == 0) and (target_col == 0)):
                        # House Check
                        for i in range(24, 6, -1):
                            pos_check = get_pos_info(i, current_pos_dict)
                            # Check if there is a same color piece.
                            if pos_check[0] == color:
                                return None
                        # Didn't return, move possible.
                        return [piece.pos, target_col]
                    
                    # Exact roll, can exit, if all are in House.
                    elif ((color == 1) and (target_col == 25)):
                        # House Check
                        for i in range(1, 19):
                            pos_check = get_pos_info(i, current_pos_dict)
                            # Check if there is a same color piece.
                            if pos_check[0] == color:
                                return None
                        # Didn't return, move possible.
                        return [piece.pos, target_col]
                    
                    # Non-exact roll, can exit if no other avaliable moves.
                    # i.e. No piece behind this one.
                    else:
                        if color == 0:
                            for i in range(24, piece.pos, -1):
                                pos_check = get_pos_info(i, current_pos_dict)
                                # Check if there is a same color piece.
                                if pos_check[0] == color:
                                    return None
                            # Didn't return, move possible.
                            return [piece.pos, 0]
                        
                        else:
                            for i in range(1, piece.pos):
                                pos_check = get_pos_info(i, current_pos_dict)
                                # Check if there is a same color piece.
                                if pos_check[0] == color:
                                    return None
                            # Didn't return, move possible.
                            return [piece.pos, 25]
        
        
        # After every valid move, start iterating over the other pieces.
        
        # Uneven Dice.
        if dice1 != dice2:
            # Using dice1 first.
            for piece in self.pieces:
                if piece.color == color:
                    preview_pieces = deepcopy(self.pieces)
                    possible_move = check_valid_move(piece, dice1, preview_pieces)
                    
                    if possible_move:
                        self.make_move(possible_move[0], possible_move[1], 
                                       preview_pieces)
                        
                        # After making the first move.
                        for piece in preview_pieces:
                            if piece.color == color:
                                possible_move2 = check_valid_move(piece, dice2, 
                                                                  preview_pieces)
                                if possible_move2:
                                    all_possible_moves.append([possible_move, 
                                                               possible_move2])
                            
            # Using dice2 first.
            for piece in self.pieces:
                if piece.color == color:
                    preview_pieces = deepcopy(self.pieces)
                    possible_move = check_valid_move(piece, dice2, preview_pieces)
                    
                    if possible_move:
                        self.make_move(possible_move[0], possible_move[1], 
                                       preview_pieces)
                        
                        # After making the first move.
                        for piece in preview_pieces:
                            if piece.color == color:
                                possible_move2 = check_valid_move(piece, dice1, 
                                                                  preview_pieces)
                                if possible_move2:
                                    all_possible_moves.append([possible_move, 
                                                               possible_move2])
        
        # Double Dice. Move four times.
        else:
            for piece in self.pieces:
                if piece.color == color:
                    preview_pieces = deepcopy(self.pieces)
                    possible_move = check_valid_move(piece, dice1, preview_pieces)
                    
                    if possible_move:
                        self.make_move(possible_move[0], possible_move[1], 
                                       preview_pieces)
                        
                        # Second move.
                        for piece in preview_pieces:
                            if piece.color == color:
                                preview_pieces2 = deepcopy(preview_pieces)
                                possible_move2 = check_valid_move(piece, dice1, 
                                                                  preview_pieces2)
                                if possible_move2:
                                    self.make_move(possible_move2[0], 
                                                   possible_move2[1], 
                                                   preview_pieces2)
                                    
                                    # Third move.
                                    for piece in preview_pieces2:
                                        if piece.color == color:
                                            preview_pieces3 = deepcopy(
                                                preview_pieces2)
                                            possible_move3 = check_valid_move(
                                                piece, dice1, preview_pieces3)
                                            
                                            if possible_move3:
                                                self.make_move(possible_move3[0], 
                                                               possible_move3[1], 
                                                               preview_pieces3)
                                                
                                                # Fourth move.
                                                for piece in preview_pieces3:
                                                    if piece.color == color:
                                                        possible_move4 = \
                                                            check_valid_move(
                                                                piece, dice1, 
                                                                preview_pieces3)
                                                        
                                                        if possible_move4:
                                                            all_possible_moves.append(
                                                                [possible_move, 
                                                                 possible_move2,
                                                                 possible_move3, 
                                                                 possible_move4])
        # Remove duplicates.
        all_possible_moves_no_dup = []
        
        for move_i in all_possible_moves:
            if move_i not in all_possible_moves_no_dup:
                all_possible_moves_no_dup.append(move_i)
        
        return all_possible_moves_no_dup


if __name__ == "__main__":
    B = Board()
    print(B)