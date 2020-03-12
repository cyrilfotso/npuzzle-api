"""
Created on Thu Feb 20 11:29:29 2020

@author: c106763
"""

import time
import heapq
from State import State


class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


def trace_path(state):
    path = [state.config]    
    actions = [state.from_dir]
    if state.parent is not None:
        state = state.parent
    while state.parent:
        path.append(state.config)
        actions.append(state.from_dir)
        state = state.parent
            
    return [i for i in reversed(path)], [i for i in reversed(actions)]


def a_star_search(start, debug=False):
    # if not start.is_solvable():
    #     print('Not solvable puzzle state')
    #     return False, 'Not Solvable'

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start.config] = None
    cost_so_far[start.config] = 0
    found = False
    
    start = time.time()
    duration = 0
    path = []
    action = []

    while not frontier.empty():
        current = frontier.get()
        
        if current.is_solved():
            found = True
            end = time.time()
            path, action = trace_path(current)
            duration = "Search time is {} s".format(round(float(end-start), 3))
            depth = "Depth is {}".format(current.moves)
            break
        
        for next_move_item in current.possible_moves():
            next_move = next_move_item['config']
            from_dir = next_move_item['from_dir']
            next_state = State(config=next_move, type_heuristic=current.type_heuristic,
                               parent=current, goal_mode=current.goal_mode, 
                               moves=current.moves+1, size=current.size, from_dir=from_dir)
            if debug:
                print(next_state.config, next_state.f())
            new_cost = cost_so_far[current.config] + 1
            if next_state.config not in cost_so_far or new_cost < cost_so_far[next_move]:
                cost_so_far[next_move] = new_cost
                priority = new_cost + next_state.h()
                frontier.put(next_state, priority)
                came_from[next_move] = current
    
    return found, came_from, cost_so_far, path, action, duration, depth


def ida_star_helper(q, max_distance, visited):
    count = 0
    current_distance = -1
    while not q.empty():
        count += 1
        current = q.get()
        if current.is_solved():
            visited_nodes = "No of Nodes visited: {}".format(count)
            path, action = trace_path(current)
            depth = "Depth is {}".format(current.moves)
            return True, visited_nodes, path, action, depth

        if current.f() > max_distance:
            if current_distance != -1 and current.f() < current_distance:
                current_distance = current.f()
            elif current_distance == -1:
                current_distance = current.f()
            continue
        possible_moves = current.possible_moves()

        for next_move_item in possible_moves:
            next_move = next_move_item['config']
            from_dir = next_move_item['from_dir']
            if next_move not in visited:
                next_state = State(config=next_move, type_heuristic=current.type_heuristic,
                                   parent=current, goal_mode=current.goal_mode, 
                                   moves=current.moves+1, size=current.size, from_dir=from_dir)
                
                q.put(next_state, next_state.f())
                visited[next_move] = current

    return current_distance, False


def ida_star_search(start, debug=False):
    start_t = time.time()
    var = (start.h(), False)

    # if not start.is_solvable():
    #     print('Not solvable puzzle state')
    #     return False, 'Not Solvable'

    while True:
        visited = {}
        queue = PriorityQueue()
        queue.put(start, 0)
        visited[start.config] = None
        if debug:
            print("Threshold: ", var)
        var = ida_star_helper(queue, var[0], visited)
        if isinstance(var[0], bool):
            end = time.time()
            duration = "Search time is {} s".format(round(float(end-start_t), 3))
            return tuple(list(var) + [duration])
        elif isinstance(var[0], int):
            if var == -1:
                return False, 'Not Found'


