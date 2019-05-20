from random import randint
from zo_table.GameMechanics import *
from zo_table.transposition_table import*


class MIN_MAX():
    game_mechanics = GameMechanics()
    t_table = T_table()
    player_increment={"red": "blue" , "blue": "green" , "green": "red"}


    def alpha_beta( self, state , depth , alpha , beta , current_colour, max_colour):
 

        #not sure why 
        alpha_original = alpha
        #lookup for transposition table
        t_score , t_flag, t_best = self.t_table.lookup_score(state.z_key, depth)
        #if an entry was found 
        if(t_score != None):
            #exact value
            if t_flag == 0:
                #this state has been explored to sufficent depth
                #return 
                return t_score, t_best
            #lower_bound
            elif t_flag == 1:
                alpha = max(alpha, t_score)
            elif t_flag == 2:
                alpha = min(beta, t_score)
            #if this causes a cut off return values found in table
            #ie this node has been pruned
            if alpha >=beta:
                #print("cut")
                return t_score, t_best

        if(depth == 0 or self.is_terminal_state(state)):
            #exit state cannot have a best child state
            return self.heuristic_value(state, max_colour), None



        pos_states = []
        if t_best != None:
            temp_state = state.copy()
            #print(t_best)
            self.game_mechanics.update_node(temp_state, max_colour, self.game_mechanics.get_move_from_tuple(t_best))
            pos_states.append((temp_state, t_best ))
        # maximising player
        if(current_colour == max_colour):
            value = float("-inf")
            best_move = None
            for child_state, move in (pos_states + self.game_mechanics.get_all_possible_states(state, current_colour)):
                if(child_state!= None):
                    temp_value, _ = self.alpha_beta(child_state, depth -1 , alpha , beta, self.player_increment[current_colour], max_colour)
                    #update value and best child
                    if(temp_value > value):
                        value = temp_value
                        best_move = move
                    alpha = max( alpha , value)

                    if ( alpha >= beta ):
                        break

        #minimising players
        else:
            value = float("inf")
            best_move = None
            for child_state, move in (pos_states +self.game_mechanics.get_all_possible_states(state, current_colour)):
                if(child_state!= None):
                    temp_value, _ = self.alpha_beta(child_state, depth -1 , alpha , beta, self.player_increment[current_colour], max_colour)
                    if(temp_value < value):
                        value = temp_value
                        best_move = move
                    beta = min(beta, value)

                    if(alpha >= beta):
                        break
        #add to transposition table
        if value <= alpha_original:
            self.t_table.replace_entry(state.z_key, value, depth,best_move , 1)
        elif value >= beta:
            self.t_table.replace_entry(state.z_key, value, depth,best_move , 2)
        else:
            self.t_table.replace_entry(state.z_key, value, depth,best_move , 0)

        #print(self.t_table.match_count)
        #returns the best score and child of this current state 
        return value , best_move


    def is_terminal_state(self, state):
        for colour in state.exit_counts:
            if(state.exit_counts[colour] == 4):
                return 1; 
        return 0; 


    #testing purposes
    def heuristic_value(self, state, max_colour):
        MAX_DISTANCE = 24
        weight = 0
        feature_total = 0
        distance_apart = 0 
        for colour in state.piece_nodes:
            distance_list = []
            if(colour == max_colour):
                weight = 1
            else:
                weight = -1

            distance = list()

            num_pieces = len(state.piece_nodes[colour])
            for piece in state.piece_nodes[colour]:
                distance.append((6-self.manhattan_distance(piece,colour)))

            distance.sort()
            closest4 = 0
            otherpieces = 0 
            for i in range(0 , min(4, num_pieces)):
                closest4+= (distance[i])
            for i in range(4 , num_pieces):
                otherpieces+= (distance[i])

            feature_total += weight* closest4/4
            feature_total += weight*otherpieces/8
            if num_pieces + state.exit_counts[colour] < 4: 
                feature_total+= weight* - 50

            if(num_pieces >0):
                feature_total+=  weight* state.exit_counts[colour]* (closest4/num_pieces)*(closest4/num_pieces)

            #feature_total+=  weight* state.exit_counts[colour]* (closest4/4)*(closest4/4)

            if(state.exit_counts[colour]==4):
                feature_total += 100*weight

        return feature_total


    def manhattan_distance(self, coord, colour):
        '''returns the min possible moves from each node to any exit nodes
            Note doesn't inlcude cost of exiting board'''

        #coefficents for line cf[0]q + cf[1]r + cf[2] = 0 
        cf = {"blue" : [1,1,3] , "red": [1,0,-3], "green" : [0,1,-3]}
        
        #Shortest number of nodes between the node and any exit node
        stepCost = abs(cf[colour][0]*coord[0] + cf[colour][1]*coord[1] + cf[colour][2])
        

        #jumpCost = stepCost//2 + stepCost%2 +1
        return stepCost +1


    def is_adjacent(self, coord1, coord2):
        if self.get_dist(coord1, coord2) <= sqrt(2):
            return 1
        else:
            return 0

    def get_dist(self,  node_1, node_2):
        """
        Returns the Euclidean distance between two nodes.
        """

        return sqrt((node_1[0] - node_2[0])**2 + (node_1[1] - node_2[1])**2)

 

