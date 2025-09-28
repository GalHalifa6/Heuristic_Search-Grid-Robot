import copy

import numpy as np


class grid_robot_state:
    def __init__(self, robot_location, map=None, lamp_height=-1, lamp_location=(-1, -1)):
        self.location = robot_location
        self.map = map
        self.lamp_height = lamp_height
        self.lamp_location = lamp_location
        self.stairsCost = 0


        if map is not None:
            self.map_rows = len(map)
            self.map_cols = len(map[0]) if map else 0

    def is_within_bounds(self, x, y):
        return 0 <= x < self.map_rows and 0 <= y < self.map_cols

    @staticmethod
    def is_goal_state(_grid_robot_state):
        x, y = _grid_robot_state.location
        return (_grid_robot_state.location == _grid_robot_state.lamp_location and
                _grid_robot_state.map[x][y] == _grid_robot_state.lamp_height)

    def get_neighbors(self):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        # Handle movement in all four directions
        for dx, dy in directions:
            x, y = self.location
            new_x, new_y = x + dx, y + dy

            if self.is_within_bounds(new_x, new_y) and self.map[new_x][new_y] != -1:
                move_cost = 1 + self.stairsCost
                neighbor_state = self.copy_new_loc(new_x, new_y)
                neighbor_state.stairsCost = self.stairsCost
                neighbors.append((neighbor_state, move_cost))

        # Handle picking up stairs
        if self.can_pick_up():
            pick_up_state, pick_up_cost = self.pick_up_stairs()
            neighbors.append((pick_up_state, pick_up_cost))

        # Handle placing stairs
        if self.can_place_stairs():
            place_stairs_state, place_cost = self.place_stairs()
            neighbors.append((place_stairs_state, place_cost))

        # Handle combining stairs
        if self.can_combine_stairs():
            combine_stairs_state, combine_cost = self.combine_stairs()
            neighbors.append((combine_stairs_state, combine_cost))

        return neighbors


    def can_pick_up(self):
        return self.map[self.location[0]][self.location[1]] > 0 and self.stairsCost == 0

    def pick_up_stairs(self):
        new_state = self.copy_new_map()
        new_state.stairsCost = self.map[self.location[0]][self.location[1]]
        new_state.map[self.location[0]][self.location[1]] = 0
        return new_state, 1

    def can_place_stairs(self):
        return self.stairsCost > 0 and self.map[self.location[0]][self.location[1]] == 0

    def place_stairs(self):
        new_state = self.copy_new_map()
        new_state.map[self.location[0]][self.location[1]] += self.stairsCost
        new_state.stairsCost = 0
        return new_state, 1

    def can_combine_stairs(self):
        current_tile_stairs = self.map[self.location[0]][self.location[1]]
        return self.stairsCost > 0 and current_tile_stairs > 0 and \
               self.stairsCost + current_tile_stairs <= self.lamp_height

    def combine_stairs(self):
        new_state = self.copy_new_map()
        new_state.stairsCost = self.stairsCost + self.map[self.location[0]][self.location[1]]
        new_state.map[self.location[0]][self.location[1]] = 0
        return new_state, 1

    def get_state_str(self):
        return  self.location

    def __hash__(self):
        return hash((self.location, tuple(map(tuple, self.map)), self.stairsCost))

    def __eq__(self, other):
        my_npMap = np.array(self.map)
        other_npMap = np.array(other.map)
        return (self.location == other.location and
                np.array_equal(my_npMap,other_npMap) and
                self.stairsCost == other.stairsCost)

    def copy_new_loc(self, new_x, new_y):
        return (
            grid_robot_state(
                (new_x, new_y),
                self.map,
                self.lamp_height,
                self.lamp_location
            ))

    def copy_new_map(self):
        return (
            grid_robot_state(
                self.location,
                copy.deepcopy(self.map),
                self.lamp_height,
                self.lamp_location
            ))
