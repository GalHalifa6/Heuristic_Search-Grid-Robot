# Grid Robot — A* Search with Height Constraints
A Python project that implements the A* search algorithm on a grid.
A robot navigates obstacles and stairs-like cells, using heuristics to reach a target ("lamp") under height constraints.

# Features
A* search implementation with open/closed lists.
# Two heuristics:
-**Base heuristic** → Manhattan distance.
-**Advanced heuristic** → Combines Manhattan distance with penalties/bonuses based on height cost.

# Grid-based environment with:
-Free cells,
-Walls/blocked cells,
-Special tiles that increase stairs cost.

# Controls & Map Encoding
-**0** → free cell
-**-1** → wall/blocked
-positive integers → stairs/steps tiles (increase stairs cost)
-The lamp target is defined by (lamp_location, lamp_height).
-The robot starts at robot_start_location.

# Future Improvements
Add GUI visualization for the grid and robot path.


