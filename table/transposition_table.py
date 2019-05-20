

import numpy as np
import array
import random

class T_table():
    match_count= 0 
    #zobrist = np.ndarray([7,7,3], dtype = "int64")
    num_entries = 100000
    #key = np.zeros([1,1], dtype= "int64")
    t_key = np.ndarray([1,num_entries], dtype = "S49")
    t_best = np.ndarray([1,num_entries], dtype = "S49")
    t_score = np.ndarray([1,num_entries], dtype = "int16")
    t_depth = np.ndarray([1,num_entries], dtype = "int8")
    #t_ancient = np.full([1, num_entries], 1 , dtype = "bool")
    t_flag = np.ndarray([1, num_entries], dtype = "int8")

    def sorting_rep(self, state):
        #creates a string indicating the board state
        string_rep = 49*"e"
        for colour in state.piece_nodes:
            for piece in state.piece_nodes[colour]:
                index = (piece[0]+3)*7 +(piece[1]+3)
                string_rep= string_rep[:index] +colour[0]+ string_rep[index+1:]

        return np.dtype("S49").type(string_rep)



    def lookup_score(self, state, depth):
        string_rep = self.sorting_rep(state)

        index = self.get_index(string_rep)
        #if(string_rep== self.t_key[0,index]):
            #print("match")
        #print(f" calculated: {string_rep}\n  stored: {self.t_key[0,index]}\n")
        if string_rep ==self.t_key[0,index] and self.t_depth[0,index]==depth:
            #print("match\n")
            #self.match_count+=1
            return self.t_score[0,index], self.t_flag[0,index] , self.t_best[0,index]
        else:
            return None, None, None

    def replace_entry(self, state, score ,depth, best_child, flag):
        string_rep = self.sorting_rep(state)
        index = self.get_index(string_rep)
        self.t_key[0,index] = string_rep
        self.t_score[0,index]= score
        self.t_depth[0,index] = depth
        self.t_best[0,index]= self.sorting_rep(best_child)
        self.t_flag[0,index]= flag

    def get_index(self, string_rep):
        return hash(string_rep)%self.num_entries

"""
    def inverse_state(string_rep):
        piece_nodes = dict()
        exit_counts= dict()
        colours = ["red", "green", "blue"]
        for colour in colours:
            piece_nodes[colour]=set()
            exit_counts[colour]= 0

        coord_range = range(-3, 3+1)
        for q in coord_range:
            for r in coord_range:
                if( -q-r in coord_range):
                    index = (piece[0]+3)*7 +(piece[1]+3)
                    for colour in colours:
                        if string_rep[i] == colour[0]:
                            piece_nodes[colour].add((q,r))
"""












