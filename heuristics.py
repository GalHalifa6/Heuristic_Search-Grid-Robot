from collections import deque

from grid_robot_state import grid_robot_state

def base_heuristic(_grid_robot_state):
    robotX, robotY = _grid_robot_state.location
    lampX, lampY = _grid_robot_state.lamp_location
    return abs(robotX-lampX) + abs(robotY-lampY)

def advanced_heuristic(_grid_robot_state):
    stairCost = _grid_robot_state.stairsCost
    base_value = base_heuristic(_grid_robot_state)
    height_diff = abs(_grid_robot_state.lamp_height - stairCost)

    # Refinement strategies:
    # 1. Precision height matching
    precision_factor = 1 - (height_diff / max(_grid_robot_state.lamp_height, 1))

    # 2. Movement efficiency bonus
    movement_efficiency_bonus = 0
    if stairCost < _grid_robot_state.lamp_height:
        movement_efficiency_bonus = (stairCost / _grid_robot_state.lamp_height)

    # Combine with subtle weighting
    return base_value + base_value * stairCost + height_diff * precision_factor + movement_efficiency_bonus

