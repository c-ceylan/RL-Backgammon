import numpy as np
import gymnasium as gym

import time

from Dice import Dice
from Backgammon import Backgammon


SEEDS_LIST = []

class BGEnv(gym.Env):
    def __init__(self, color=0):
        dice_seed = self.get_seed_no()
        self.game = Backgammon(dice_seed=dice_seed,
                               get_possible_moves_on_turn=True)
        self.opponent_dice = Dice(6, dice_seed-1)
        
        # !!! We are always white, i.e. color = 0.
        # If needed, can invert later when playing.
        self.color = color
        
        # Opponents is starting.
        if ((self.color) == 0 and (self.game.P1==1)):
            self.opponent_move()
        elif ((self.color) == 1 and (self.game.P0==1)):
            self.opponent_move()
        
        # TODO: Add our color as observation.
        self.observation_space = gym.spaces.Dict(
            # Each row represents one column on the board.
            # Empty: -1, White: 0, Black: 1
            {'board': gym.spaces.Box(low=-1, high=1, shape=(24, 15), dtype=int),
             # For our move, also for opponent. Or not? -> shape=(2, 2)
             'dice_roll': gym.spaces.Box(low=1, high=6, shape=(2,), dtype=int),
             'broken_pieces': gym.spaces.Box(low=0, high=15, shape=(2,), dtype=int),
             'won_pieces': gym.spaces.Box(low=0, high=15, shape=(2,), dtype=int)})
        
        self.action_space = gym.spaces.Box(low=0, high=25, shape=(4, 2), dtype=int)
        
        
    def get_seed_no(self):
        DICE_SEED = time.time_ns()
        SEEDS_LIST.append(DICE_SEED)
        return DICE_SEED
        
    # TODO: Have the option to have the opponent to be another agent.
    def opponent_move(self):
        # XXX: Might consider including opponents roll and move into observation.
        # !!! Opponent moves randomly, for now.
        self.oppo_dice1, self.oppo_dice2 = self.opponent_dice.get_roll()
        
        oppo_possible_moves = self.game.Board.get_all_moves(
            self.oppo_dice1, self.oppo_dice2, {0: 1, 1: 0}[self.color])
        
        # Pick random move.
        move_pick = np.random.randint(0, len(oppo_possible_moves)+1)
        oppo_move_list = oppo_possible_moves[move_pick]
        
        # Make move.
        game_end = self.game.move(oppo_move_list)
        
        return game_end
    
    
    def _get_obs(self):
        observation_board = np.array(self.game.Board.board_encoded())
        observation_dice_roll = np.array([self.game.dice1, 
                                          self.game.dice2])
        observation_broken = np.array([self.game.Board.broken_pieces[0], 
                                       self.game.Board.broken_pieces[1]])
        observation_won = np.array([self.game.Board.won_pieces[0], 
                                    self.game.Board.won_pieces[1]])
        
        observation = {'board': observation_board, 
                       'dice_roll': observation_dice_roll, 
                       'broken_pieces': observation_broken, 
                       'won_pieces': observation_won}
        
        return observation
    
    
    def _get_info(self):
        info = {'board_str': self.game.Board.board_str(),
                'board_pieces': self.game.Board.pieces,
                'dice_roll': [self.game.dice1, self.game.dice2],
                'broken_pieces': self.game.Board.broken_pieces,
                'won_pieces': self.game.Board.won_pieces}
        
        return info
    
    
    def render(self):
        print(self.game.Board)
    
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        dice_seed = self.get_seed_no()
        self.game = Backgammon(dice_seed=dice_seed, 
                               get_possible_moves_on_turn=True)
        self.opponent_dice = Dice(6, dice_seed-1)
        
        # Opponents is starting.
        if ((self.color) == 0 and (self.game.P1==1)):
            self.opponent_move()
        elif ((self.color) == 1 and (self.game.P0==1)):
            self.opponent_move()
        
        observation = self._get_obs()
        info = self._get_info()

        return observation, info
    
    
    def step(self, action):
        if self.game.dice1 != self.game.dice2:
            move_list = action[:2].tolist()
        else:
            move_list = action.tolist()
        
        # Invalid move.
        # Board stays the same, agent receives a small negative reward.
        if move_list not in self.game.Board.get_all_moves(self.game.dice1, 
                                                          self.game.dice2, 
                                                          self.color):
            terminated = False
            truncated = False
            reward = -0.01
            observation = self._get_obs()
            info = self._get_info()
        
        # Valid move.
        else:
            agent_game_end = self.game.move(move_list)
            
            self.moves_history[len(SEEDS_LIST)].append([self.color, move_list])
            
            # Agent won.
            if agent_game_end != None:
                # Can't loose when it ends on Agent's turn.
                # Don't need to check side.
                terminated = True
                truncated = False
                reward = 10
                observation = self._get_obs()
                info = self._get_info()
                
            # Game goes on, Opponent's turn.
            else:
                oppo_move_and_game_end = self.opponent_move()
                
                # Can't win when it ends on Opponent's turn.
                # Don't need to check side.
                if oppo_move_and_game_end != None:
                    terminated = True
                    truncated = False
                    reward = -10
                    observation = self._get_obs()
                    info = self._get_info()
                    
                # Game goes on.
                terminated = False
                truncated = False
                # Minor positive reward for valid move.
                reward = 0.001
                observation = self._get_obs()
                info = self._get_info()
                
                # TODO: Should add auxiliary rewards for heuristically good
                # moves, e.g. breaking opponents piece.
                
        # self.render()
        
        return observation, reward, terminated, truncated, info