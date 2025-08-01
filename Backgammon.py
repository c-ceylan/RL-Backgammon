from Dice import Dice
from Board import Board

class Backgammon():
    def __init__(self, dice_seed=None, 
                 get_possible_moves_on_turn=False,
                 check_moves_before_move=False):
        
        self.Dice = Dice(6, dice_seed)
        self.Board = Board()
        
        self.get_moves_on_turn = get_possible_moves_on_turn
        self.check_moves_before_move = check_moves_before_move
        
        # White: P0, Black: P1
        self.get_initial_player_turn()
        self.get_next_dice_roll()
        
    def __repr__(self):
        return self.Board.__repr__()
    
    def get_initial_player_turn(self):
        # Determine Player Turn 
        P0, P1 = 0, 0
        
        while P0 == P1:
            P0, P1 = self.Dice.get_roll()
            
            if P0 > P1: 
                print(f'White rolled {P0}, Black rolled {P1}.', 
                      'White begins.', sep='\n')
                self.P0 = 1
                self.P1 = 0
            elif P1 > P0:
                print(f'White rolled {P0}, Black rolled {P1}.', 
                      'Black begins.', sep='\n')
                self.P0 = 0
                self.P1 = 1
                 
    def get_next_dice_roll(self):
        print(self.Board)
        
        self.dice1, self.dice2 = self.Dice.get_roll()
        
        if self.P0 == 1:
            color, color_str = 0, 'White'
        else:
            color, color_str = 1, 'Black'
        
        print(f"\nIt's {color_str}'s turn.", 
              f"Dice has rolled: {self.dice1, self.dice2}", 
              sep='\n')
            
        if self.get_moves_on_turn:
            self.possible_moves = self.Board.get_all_moves(
                self.dice1, self.dice2, color)
    
    def move(self, moves_list):
        if self.check_moves_before_move:
            if moves_list not in self.possible_moves:
                raise ValueError('Invalid move entered.')
            
        for move in moves_list:
            self.Board.make_move_on_board(move[0], move[1])
        
        if not self.check_game_end():
            # Update player turn.
            self.P0, self.P1 = self.P1, self.P0
            
            self.get_next_dice_roll()
            
        else:
            winner_code = self.check_game_end()
            
            print(self.Board)
            
            winner = {0: 'White', 1: 'Black'}[winner_code]
            print(f"{winner} has won!")
            
            return winner_code
        
    def check_game_end(self):
        if self.Board.check_won() == -1:
            return False
        else:
            return self.Board.check_won()
        
        
if __name__ == "__main__":
    BG = Backgammon()
    
    # TODO: Play a few games by picking a random move.
    # Make sure there are no bugs.
    