#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:10:01 2020

@author: c106763
"""
from State import State
from implementation import a_star_search, ida_star_search

conf = (4, 5, 6, 7, 8, 0, 1, 2, 3)
cn_easy = (1, 2, 3, 4, 5, 6, 7, 8, 0)

state = State(config=cn_easy, type_heuristic=2, parent=None,
              goal_mode='zero_first', moves=0, size=3)

state2 = State(config=(12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 13, 14, 15),
               type_heuristic=2, parent=None, goal_mode='zero_first', moves=0, size=4)

# a_star_out_24 = a_star_search(state, True)

ida_star_out_24 = ida_star_search(state2, True)

print(ida_star_out_24)
