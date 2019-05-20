import numpy as np
import random 


class Zobrist():

    #used for indexing
    colour_to_int = {"red": 0 , "green": 1 ,"blue": 2}
    zobrist_piece = np.ndarray([7,7,3], dtype = "uint64")
    zobrist_exit = np.ndarray([5,3], dtype= "uint64")

    def __init__(self):
        self.generate_unique_pairs()

    def generate_unique_pairs(self):
        """
        generates a unique and random int64 for each combination of piece and board position
        also generates keys for the magnitude of exit for each colour
        keys are stored in the zobrist_piece and zobrist_key arrays
        """
        random_set = set()
        #ensures values remain the same for each operation
        np.random.seed(50)
        #generate a random int for every value in int64
        u64_info = np.iinfo("uint64")
        while len(random_set) < 49*3 + 5*3 +1:
            random_set.add(np.random.randint(u64_info.min, u64_info.max, dtype= "uint64"))

        for i1 in range(0, self.zobrist_piece.shape[0]):
            for i2 in range(0, self.zobrist_piece.shape[1]):
                for i3 in range(0, self.zobrist_piece.shape[2]):
                    self.zobrist_piece[i1,i2,i3]= random_set.pop()
        for j1 in range(0 , self.zobrist_exit.shape[0]):
            for j2 in range(0 , self.zobrist_exit.shape[1]):
                self.zobrist_exit[j1,j2] = random_set.pop()


    """
    helper functions for accessing keys
    """
    def get_zobrist_piece(self, piece, colour):
        return self.zobrist_piece[piece[0], piece[1], self.colour_to_int[colour]]
    def get_zobrist_exit(self, num_exits, colour):
        #print(self.zobrist_piece[num_exits, self.colour_to_int[colour]])
        return self.zobrist_exit[num_exits, self.colour_to_int[colour]]

    """
    Applies a single zobrist key to the hash of the provided state
    """
    #applys a pieces unique key to a state 
    def apply_piece(self, state, piece, colour):
        state.z_key = state.z_key ^ self.get_zobrist_piece(piece,colour)
    def apply_exit(self, state, count, colour ):
        #print(state.z_key)
        state.z_key = state.z_key ^ self.get_zobrist_exit(count, colour)
    #aincrease the zobrist key by one for the
    def increase_exit(self, state, count , colour):
        state.z_key= state.z_key ^ self.get_zobrist_exit(state.exit_counts[colour], colour)
        state.z_key = state.z_key ^ self.get_zobrist_exit(count, colour)