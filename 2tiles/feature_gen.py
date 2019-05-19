
from 2tiles.GameMechanics import *
class Feature_Gen: 
    game_mechanics = GameMechanics()
    features = []
    #Should be put in main program
    weights = []


    def create_features(self, state):
        pass




    def piece_info(self, state, max_colour):

        score = 0
        enemy_colours = { "red" : ("blue" , "green") , "blue" : ("red", "green") , "green": ("red", "blue") }

        all_pieces = self.game_mechanics.get_all_piece_nodes(state)

        pieces_protected = dict() 
        pieces_capture_protected = dict()
        pieces_hanging = dict() 
        protected_by_edge =  dict() 
        #tfw had to google the plural
        directions = [(1,0), (-1, 0) , (0,1) , (0,-1),(1,-1) , (1,-1)] 

        #add pieces protected and pieces potentially threatened for each colour
        #for colour in state.piece_nodes:
            #pieces_protected[colour]= set()
            #potentially_threatening = set()
        tile_counts = dict()
        distance_counts = dict()

        exit_sum = dict()
        weight =dict()
        hanging_weight = dict()
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



            distance_counts[colour] = 0  
            for location in state.piece_nodes[colour]:
                for v in directions:
                    tile = []
                    #tile centered around ally tile
                    for step in range(1, 3):
                        tile.append((location[0] + step*v[0], location[1] +step*v[1]))


                    if not self.game_mechanics.is_on_board(tile[0]):
                        #defended by the board edge
                        protected_by_edge[colour]+=1 
                    elif tile[0] in state.piece_nodes[colour]:
                        #defended by an allied piece
                        pieces_protected[colour] +=1
                    else:
                        #possible jump if true
                        for e_colour in enemy_colours[colour]:
                            if tile[0] in state.piece_nodes[e_colour]:
                                if not self.game_mechanics.is_on_board(tile[1]):
                                    pieces_capture_protected[e_colour]+=1
                                    #capture_protected by edge
                                else:
                                    if tile[1] not in all_pieces:
                                        pieces_hanging[e_colour]+=1
                                    else:
                                        #number of captures currently blocked
                                        pieces_capture_protected[e_colour]+=1
                #distance for each piece
                distance_counts[colour] += (6 -self.manhattan_distance(location,colour))

            #calculating score
            num_pieces = len(state.piece_nodes[colour])
            #0 to 6 
            score += weight[colour] * distance_counts[colour] * 1 


            if len(state.piece_nodes[colour]):
                score += weight[colour] *state.exit_counts[colour] * ((distance_counts[colour]/num_pieces))*2
            # [allies_protected , allies_capture_protected, enemies_hanging, enemies_protected , protected_by_edge  ]
            score += weight[colour] * pieces_protected[colour] * 0.2
            score += weight[colour] * pieces_capture_protected[colour] * 0.2
            score += hanging_weight[colour] * pieces_hanging[colour] * -6
            score += weight[colour] * protected_by_edge[colour] *0.1

        #1 6 1 0 -6 0

        if(state.exit_counts[colour]==4):
            #print(f" exit_counts = {state.exit_counts[colour]}")
            score+= 100
        return score




        #testing purposes
    def heuristic_value(self, state, max_colour):
        MAX_DISTANCE = 24
        weight = 0
        feature_total = 0
        for colour in state.piece_nodes:

            if(colour == max_colour):
                weight = 1
            else:
                weight = -1

            for coord in state.piece_nodes[colour]:
                feature_total += weight*(6-self.manhattan_distance(coord,colour))

            feature_total+= 15*weight* state.exit_counts[colour]

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


    def classify_three_tiles(self, tile_counts ,tile , colour):
        allies_protected = [['A', 'A', 'empty'] , ['A', 'A', 'A']]
        allies_capture_protected = ['A' , 'A', 'O']
        enemies_hanging =['A', 'O', 'empty']
        enemies_protected = [['A', 'O' , 'O'] , ['A' , 'O' , 'A'] ,['A', 'O' , 'NA']]
        protected_by_edge = ['A', 'NA' , 'NA']

        if tile in allies_protected:
            tile_counts[colour][0] +=1

        elif tile in allies_capture_protected:
            tile_counts[colour][1]+=1

        elif tile in enemies_hanging:
            tile_counts[colour][2]+=1
        elif tile in protected_by_edge:
            tile_counts[colour][3]+=1


