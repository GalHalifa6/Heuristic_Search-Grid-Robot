import heapq
from heapq import heapify

from search_node import search_node
from grid_robot_state import grid_robot_state



def create_open_set():
    return ({},[])

def create_closed_set():
    return dict() # Use hashable states for quick membership checks

# Add a node to the open set
def add_to_open(vn, open_set):
    open_set[0][vn.state] = vn
    heapq.heappush(open_set[1],(vn.f,vn))

# Check if the open set is not empty
def open_not_empty(open_set):
    return len(open_set[1]) > 0

# Get the node with the smallest f-value
def get_best(open_set):
    return heapq.heappop(open_set[1])[1]

# Add a state to the closed set
def add_to_closed(vn, closed_set):
    closed_set[vn] = vn.g

#returns False if curr_neighbor state not in open_set or has a lower g from the node in open_set
#remove the node with the higher g from open_set (if exists)
def duplicate_in_open(vn, open_set):
    my_dict,my_heap = open_set
    if(vn.state in my_dict):
        node = my_dict[vn.state]
        if(node.g <= vn.g):
            return True
        else:
            my_dict[vn.state] = vn
            return False
    return False

#returns False if curr_neighbor state not in closed_set or has a lower g from the node in open_set
#remove the node with the higher g from closed_set (if exists)
def duplicate_in_closed(vn, closed_set):
    if( vn.state in closed_set):
        if (closed_set[vn.state] <= vn.g):
            return True
        else:
            closed_set[vn.state] = vn.g
            return False
    else:
        closed_set[vn.state] = vn.g
    return False


def print_path(path):
    for i in range(len(path) - 1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")
    print(path[-1].state.get_state_str())

def search(start_state, heuristic):
    open_set = create_open_set()
    closed_set = create_closed_set()
    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_set)

    while open_not_empty(open_set):
        current = get_best(open_set)

        if grid_robot_state.is_goal_state(current.state):
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            return path

        add_to_closed(current, closed_set)
        for neighbor, edge_cost in current.get_neighbors():
            curr_neighbor = search_node(neighbor, current.g + edge_cost, heuristic(neighbor), current)
            if not duplicate_in_open(curr_neighbor, open_set) and not duplicate_in_closed(curr_neighbor, closed_set):
                add_to_open(curr_neighbor, open_set)
    return
