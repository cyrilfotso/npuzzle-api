#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 09:40:02 2020

@author: cfo
"""

EMPTY_TILE = 0


class State:
    
    def __init__(self, config, type_heuristic=0, parent=None, goal_mode='zero_first', moves=0, size=3, from_dir=None):
        """
        :param:                 
                - config: the puzzle configuration, list tile
                - type_heuristic: 
                    0: breadth-first search
                    1: number of misplaced tiles
                    2: Manhattan Distance
                - parent: the parent from where this state derives
                - moves: the number of moves require to reach this state
                - size: the size of the puzzle, for a 8 puzzle, the size is 3
        """
        self.size = size
        self.config = config
        self.parent = parent
        self.goal_mode = goal_mode        
        self.goal = self.init_goal(self.goal_mode, self.size) 
        self.moves = moves
        self.type_heuristic = type_heuristic
        self.is_solvable = self.is_state_solvable(self.config, self.goal, self.size)
        self.from_dir = from_dir
        
        if self.is_valid_input() is False:
            raise('Fail to initialize a State with configs')
    
    def is_solved(self, goal=None):
        """
        helper to check if the node is the goal 
        """
        if goal is None:
            goal = self.goal
        return self.config == goal
    
    def __lt__(self, other):
        """
        helper to check if the state is less than another state
        """
        return self.f() < other.f()

    def __gt__(self, other):
        """
        helper to check if the state is greater than another state
        """
        return self.f() > other.f()
    
    def __eq__(self,other):
        """
        helper to check if the state is euqal to another state
        """
        return self.config == other.config
    
    def __hash__(self):
        """
        helper to process the hash value of the state,
        will be use to tack the visited states 
        in a hash map to reduce the access time
        """
        return hash(str(self.config))

    def h(self, goal=None):
        """
        helper to process the heuristic of the instance
        """
        if goal is None:
            goal = self.goal
        heuristic = 0  
        if self.type_heuristic == 0:  # breadth-first search
            pass
        
        elif self.type_heuristic == 1: # heuristic -> number of misplaced tiles
            heuristic = self.hamming(self.config, goal, self.size)
            
        elif self.type_heuristic == 2: # heuristic -> Manhattan Distance
            heuristic = self.manhattan(self.config, goal, self.size)
        
        else:
            raise('type_heuristic not supported yet'+ str(self.type_heuristic))
            print('type_heuristic not supported yet'+ str(self.type_heuristic))
        
        return heuristic

    def hamming(self, candidate, solved, size): #aka tiles out of place
        res = 0
        for i in range(size*size):
            if candidate[i] != 0 and candidate[i] != solved[i]:
                res += 1
        return res

    def manhattan(self, candidate, goal, size):
        res = 0
        for i in range(size*size):
            if candidate[i] != 0 and candidate[i] != goal[i]:
                ci = goal.index(candidate[i])
                y = (i // size) - (ci // size)
                x = (i % size) - (ci % size)
                res += abs(y) + abs(x)
        return res

    def g(self):
        """
        helper to process the g value of the current state
        """
        return self.moves

    def f(self):
        """
        helper to process the f score value of the current state
        """
        return self.h() + self.g()

    def zero_first(self, size):
        """
        define the goal state for zero_first mode
        """
        return tuple([x for x in range(size*size)])

    def zero_last(self, size):
        """
        define the goal state for zero_last mode
        """
        lst = [x for x in range(1,size*size)]
        lst.append(0)
        return tuple(lst)

    def init_goal(self, goal_mode, size):
        """
        helper to create the final goal array from the goal mode
        """
        if goal_mode == 'zero_first':
            return self.zero_first(size)
        
        elif goal_mode == 'zero_last':
            return self.zero_last(size)
        
        else:  # default mode is set to zero_first
            return self.zero_first(size)

    def count_inversions(self, puzzle, goal, size):
        res = 0
        for i in range(size * size - 1):
            for j in range(i + 1, size * size):            
                    vi = puzzle[i]
                    vj = puzzle[j]
                    if goal.index(vi) > goal.index(vj):
                        res += 1
        return res

    def is_state_solvable(self, puzzle, goal, size):
        """
        helper to test if we can reach the goal from the current state
        """
        inversions = self.count_inversions(puzzle, goal, size)
        puzzle_zero_row = puzzle.index(EMPTY_TILE) // size
        puzzle_zero_column = puzzle.index(EMPTY_TILE) % size
        solved_zero_row = goal.index(EMPTY_TILE) // size
        solved_zero_column = goal.index(EMPTY_TILE) % size
        taxicab = abs(puzzle_zero_row - solved_zero_row) + abs(puzzle_zero_column - solved_zero_column)
        if taxicab % 2 == 0 and inversions % 2 == 0:
            return True
        if taxicab % 2 == 1 and inversions % 2 == 1:
            return True
        return False

    def is_valid_input(self):
        """
        helper to make sure all the input are correct to form a proper puzzle state
        """
        # size of the config vs size of the puzzle
        if len(self.config) != self.size**2:
            return False
        
        # item should have values less or equal to size**2
        generated = [x for x in range(self.size**2)]
        difference = [x for x in generated if x not in self.config]
        if len(difference) != 0:
            print('puzzle tiles must be in range from 0 to SIZE**2-1')
            return False
        
        return True

    def clone_and_swap(self, data,y0,y1):
        """
        helper to copy a state config, swap to tile based on they positions
        """
        clone = list(data)
        tmp = clone[y0]
        clone[y0] = clone[y1]
        clone[y1] = tmp
        return tuple(clone)

    def possible_moves(self):
        """
        helper to get all the possibles moves from one the current state
        """
        res = []
        data = self.config
        size = self.size
        y = data.index(EMPTY_TILE)
        if y % size > 0:
            left = self.clone_and_swap(data, y, y-1)
            res.append({'config': left, 'from_dir': {'action': 'left', 'res': list(left)}})
        if y % size + 1 < size:
            right = self.clone_and_swap(data, y, y+1)
            res.append({'config': right, 'from_dir': {'action': 'right', 'res': list(right)}})
        if y - size >= 0:
            up = self.clone_and_swap(data, y, y-size)
            res.append({'config': up, 'from_dir': {'action': 'up', 'res': list(up)}})
        if y + size < len(data):
            down = self.clone_and_swap(data, y, y+size)
            res.append({'config': down, 'from_dir': {'action': 'down', 'res': list(down)}})
        return res



































