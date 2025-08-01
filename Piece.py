class Piece():
    def __init__(self, initial_pos, color):
        self.pos = initial_pos
        self.color = color
        
    def __repr__(self):
        return f'Piece({self.pos}, {self.color})'
    
    def __eq__(self, other):
        return (self.pos == other.pos) & (self.color == other.color)
    
    def update_pos(self, new_pos):
        self.pos = new_pos
        
if __name__ == "__main__":
    # Colors: {White: 0, Black: 1}
    P = Piece(1, 1)