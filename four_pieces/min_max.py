from random import randint
from four_pieces.GameMechanics import *
from four_pieces.feature_gen import *


class MIN_MAX():
    game_mechanics = GameMechanics()
    feature_gen = Feature_Gen()
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





            feature_total+=  weight* state.exit_counts[colour]* (closest4/4)*(closest4/4)

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

 

