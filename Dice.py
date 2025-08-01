import numpy as np
import time

class Dice():
    def __init__(self, max_val=6, set_seed=None):
        self.max_val = max_val
        
        if set_seed:
            np.random.seed = set_seed
        else:
            # For reproducibility.
            self.__seed = time.time_ns()
            print(f'\nSeed: {self.__seed}\n')
            
            np.random.seed = self.__seed
        
    def get_roll(self):
        return np.random.randint(1, self.max_val+1), \
            np.random.randint(1, self.max_val+1)

