EXIT_LINE_CFS = {   
                        "blue"  : (1, 1, 3), 
                        "red"   : (1, 0, -3), 
                        "green" : (0, 1, -3) 
                    }


def get_min_no_of_moves_to_exit(node, colour):
    """
    Returns the minimum possible moves from a node to an exit nodes.
    """
    
    cfs = EXIT_LINE_CFS[colour]
    
    # shortest number of 'move' actions to reach an exit node
    n_min_moves = abs(cfs[0] * node[0] + cfs[1] * node[1] + cfs[2])

    return n_min_moves

def get_dists():
    
    ran = range(-3, 3+1)
    for node in [(q, r) for q in ran for r in ran if -q-r in ran]:
        print(node, ",", get_min_no_of_moves_to_exit(node, "red"))

if __name__ == "__main__":
    get_dists()