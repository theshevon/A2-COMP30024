from math import sqrt
from ben_c.game_state import *

class DecisionEngine():
    """
    Represents the agents 'brain' and so, decides which node to move to next.
    """

    # TODO: implement transition steps

    EXIT       = (999, 999)
    MAX_DEPTH  = 4
    colour     = None

    def __init__(self, colour):

        self.colour = colour

    def get_next_action(self, board):
        """
        Computes and returns the best possible action for the agent to take,
        given the current state of the board.
        """

        _, action = self.minimax(board, board.get_game_state(), self.MAX_DEPTH, float("-inf"), float("+inf"), self.colour, self.colour)

        if action is None:
            return ('PASS', None)
            
        return action

    def get_action_from_move(self, board, move):
        """
        Returns an action corresponding to a move.
        """
        if move[1] == self.EXIT:
            return ("EXIT", move[0])
        else:
            if board.get_euclidean_distance(move[0], move[1]) <= sqrt(2):
                return ("MOVE", move)
            return ("JUMP", move)

    def get_all_possible_actions(self, state, board, colour):
        """
        Returns a list of all the possible actions that a player can perform. 
        An exit move is a special case and is denoted by the two-tuple 
        ("EXIT", (999, 999)).
        """

        jump_moves     = []
        exit_moves     = []
        move_moves     = []
        team_nodes     = state.get_team_piece_nodes(colour)
        occupied_nodes = state.get_all_piece_nodes()       

        for node in team_nodes:

            # check if an exit is one of the possible moves
            if node in board.get_exit_nodes(colour):
                exit_moves.append((node, self.EXIT))
            
            # add neighbouring nodes to list
            for neighbouring_node in board.get_neighbouring_nodes(node):

                # if neighbouring node is occupied, look for landing spots
                if neighbouring_node in occupied_nodes:

                    landing_node=board.get_landing_node(node, neighbouring_node)
                    if (landing_node):
                        jump_moves.append((node, landing_node))
                
                else:
                    move_moves.append((node, neighbouring_node))

        # aggregate moves in the specified order
        possible_moves = exit_moves + jump_moves + move_moves
        
        if possible_moves == []:
            return [("PASS", None)]

        # convert all the moves into actions and return it
        return [self.get_action_from_move(board, move) for move in possible_moves]
   
    def get_all_successor_states(self, state, board, colour):
        """
        Returns a list of 2 tuples containing the all the possible states that 
        the game can be succeeded into, given its current state and the action
        required to move into that state.
        """

        successor_states = []

        # generate all possible_actions
        possible_actions = self.get_all_possible_actions(state, board, colour)

        # for each move, create a new game state
        for action in possible_actions:
            
            successor_state = deepcopy(state)
            successor_state.update(colour, action)
            successor_states.append((successor_state, action))
            
        return successor_states


    def piece_info(self, board, state, max_colour):

        score = 0
        enemy_colours = { "red" : ("blue" , "green") , "blue" : ("red", "green") , "green": ("red", "blue") }

        all_pieces = state.get_all_piece_nodes()

        #features to determine score on
        pieces_protected = dict() 
        pieces_capture_protected = dict()
        pieces_hanging = dict() 
        protected_by_edge =  dict() 

        #adjacent tile directions
        directions = [(1,0), (-1, 0) , (0,1) , (0,-1),(1,-1) , (1,-1)] 


        tile_counts = dict()
        distance_counts = dict()
        exit_sum = dict()
        weight =dict()
        hanging_weight = dict()

        #initialise features and weights for different colours
        for colour in state.piece_nodes:
            pieces_protected[colour]= 0 
            pieces_capture_protected[colour] = 0
            pieces_hanging[colour] = 0
            protected_by_edge[colour] =  0

        for colour in state.piece_nodes:

            if(colour == max_colour):
                weight[colour] = 1
                hanging_weight[colour] = 1
            else:
                weight[colour] = -1
                hanging_weight[colour] = 0


            #determines features such as hanging pieces and pieces_protected
            distance_counts[colour] = 0  
            for location in state.piece_nodes[colour]:
                for v in directions:
                    tile = []
                    #tile centered around ally tile
                    for step in range(1, 3):
                        tile.append((location[0] + step*v[0], location[1] +step*v[1]))


                    if not board.is_on_board(tile[0]):
                        #defended by the board edge
                        protected_by_edge[colour]+=1 
                    elif tile[0] in state.piece_nodes[colour]:
                        #defended by an allied piece
                        pieces_protected[colour] +=1
                    else:
                        #possible jump if true
                        for e_colour in enemy_colours[colour]:
                            if tile[0] in state.piece_nodes[e_colour]:
                                if not board.is_on_board(tile[1]):
                                    #capture_protected by edge
                                    pieces_capture_protected[e_colour]+=1

                                else:
                                    #pieces that could potentially be captured
                                    if tile[1] not in all_pieces:
                                        pieces_hanging[e_colour]+=1
                                    else:
                                        #number of captures currently blocked
                                        pieces_capture_protected[e_colour]+=1
                #distance for each piece
                distance_counts[colour] += (6 -board.get_min_no_of_moves_to_exit(location,colour))

            #calculating score - assigning weights to different features

            num_pieces = len(state.piece_nodes[colour])
            #0 to 6 
            score += weight[colour] * distance_counts[colour] * 1 

            if len(state.piece_nodes[colour]):
                score += weight[colour] *state.exit_counts[colour] * 8
            # [allies_protected , allies_capture_protected, enemies_hanging, enemies_protected , protected_by_edge  ]
            score += weight[colour] * pieces_protected[colour] * 0.30
            score += weight[colour] * pieces_capture_protected[colour] * 0
            score += hanging_weight[colour] * pieces_hanging[colour] * -6
            score += weight[colour] * protected_by_edge[colour] * 0.15
            #if terminal state found
            if(state.exit_counts[colour]==4):

                score+= weight[colour]*100

        return score

    def minimax(self, board, state, depth, alpha, beta, curr_colour, max_colour):

        next_colour = { "red" : "green", "green" : "blue", "blue" : "red" }

        if (depth == 0) or (state.is_terminal()):
            return self.piece_info(board, state, max_colour), None
        
        is_maximising_player = True if max_colour == curr_colour else False

        if is_maximising_player:
            
            best_utility = float("-inf")
            best_action  = None

            for child_state, action in self.get_all_successor_states(state, board, curr_colour):
                utility, _ = self.minimax(board, child_state, depth-1, alpha, beta, next_colour[curr_colour], max_colour)
                if utility > best_utility:
                    best_utility = utility
                    best_action  = action
                alpha = max(alpha, best_utility)

                if alpha >= beta:
                    break

            return best_utility, best_action

        else:

            best_utility = float("+inf")
            best_action  = None

            for child_state, action in self.get_all_successor_states(state, board, curr_colour):
                utility, _ = self.minimax(board, child_state, depth-1, alpha, beta, next_colour[curr_colour], max_colour)
                if utility < best_utility:
                    best_utility = utility
                    best_action  = action
                beta = min(beta, best_utility)

                if alpha >= beta:
                    break
            
            return best_utility, best_action
            



    




    