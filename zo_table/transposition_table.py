

import numpy as np
import array

class T_table():
    match_count= 0 


    num_entries = np.uint64(100000)
    #key = np.zeros([1,1], dtype= "int64")
    t_key = np.zeros([1,num_entries], dtype = "uint64")
    #t_move = np.ndarray([1,num_entries])
    t_move = np.ndarray([1,num_entries], dtype = [('start_move', np.int16, (1,2)), ("end_move", np.int16, (1,2))])
    t_score = np.ndarray([1,num_entries], dtype = "int16")
    t_depth = np.ndarray([1,num_entries], dtype = "int8")
    #t_ancient = np.full([1, num_entries], 1 , dtype = "bool")
    t_flag = np.ndarray([1, num_entries], dtype = "int8")


    def lookup_score(self, key, depth):

        index = self.get_index(key)
        #print(index)
        if key == self.t_key[0,index] and self.t_depth[0,index]>=depth:
            #print("match\n")
            #self.match_count+=1
            #print("match")
            return self.t_score[0,index], self.t_flag[0,index] , self.return_tuple(index)
        else:
            return None, None, None

    def replace_entry(self, key, score ,depth, action, flag):

        index = self.get_index(key)
        self.t_key[0,index] = key
        self.t_score[0,index]= score
        self.t_depth[0,index] = depth
        self.t_flag[0,index]= flag
        #adding tuple indicating move

        self.t_move[0,index]["start_move"][0, 0] = action[0][0]
        self.t_move[0,index]["start_move"][0, 1] = action[0][1]
        self.t_move[0,index]["end_move"][0, 0] = action[1][0]
        self.t_move[0,index]["end_move"][0, 1] = action[1][1]

        #self.t_move[0,index] = move
    def get_index(self, key):
        #print(key)
        #print(key%self.num_entries)
        return key%self.num_entries

    def return_tuple(self,  index):
        a= ((self.t_move[0,index]["start_move"][0,0], self.t_move[0,index]["start_move"][0,1]) , (self.t_move[0,index]["end_move"][0,0], self.t_move[0,index]["end_move"][0,1]))
        #print(a)
        return a






