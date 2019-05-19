from random import randint
from amie.GameMechanics import *


class MIN_MAX():
    game_mechanics = GameMechanics()
    player_increment={"red": "blue" , "blue": "green" , "green": "red"}


    def alpha_beta( self, state , depth , alpha , beta , current_colour, max_colour):
 
        if(depth == 0 or self.is_terminal_state(state)):
            #exit state cannot have a best child state
            return self.heuristic_value(state, max_colour), None
        # maximising player
        if(current_colour == max_colour):
            value = float("-inf")
            best_child = None
            for child_state in self.game_mechanics.get_all_possible_states(state, current_colour):
                temp_value, _ = self.alpha_beta(child_state, depth -1 , alpha , beta, self.player_increment[current_colour], max_colour)
                #update value and best child
                if(temp_value > value):
                    value = temp_value
                    best_child = child_state
                alpha = max( alpha , value)

                if ( alpha >= beta ):
                    break
            #returns the best score and child of this current state 
            return value ,best_child
        #minimising players
        else:
            value = float("inf")
            best_child = None
            for child_state in self.game_mechanics.get_all_possible_states(state, current_colour):
                (temp_value, _) = self.alpha_beta(child_state, depth -1 , alpha , beta, self.player_increment[current_colour], max_colour)
                if(temp_value < value):
                    value = temp_value
                    best_child = child_state
                beta = min(beta, value)

                if(alpha >= beta):
                    break
            #returns the best score and child of this current state 
            return value , best_child

    def is_terminal_state(self, state):
        for colour in state.exit_counts:
            if(state.exit_counts[colour] == 4):
                return 1; 
        return 0; 


    #testing purposes
    def heuristic_value(self, state, max_colour):
        MAX_DISTANCE = 6
        weight = 0
        feature_total = 0
        for colour in state.piece_nodes:

            if(colour == max_colour):
                weight = 1
            else:
                weight = -1

            for coord in state.piece_nodes[colour]:
                feature_total += weight*(MAX_DISTANCE-self.manhattan_distance(coord,colour))
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


    
 

