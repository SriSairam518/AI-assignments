# Problem 
 
**You are given an n × n binary matrix grid. Your task is to implement and compare two
search algorithms to find a path from the top-left cell (0, 0) to the bottom-right cell (n- 1, n - 1).**

**A clear path is defined as:**
1. All visited cells along the path must have a value of 0.
2. Moves can be made 8-directionally — i.e., from a cell, you may move to another
cell that is horizontally, vertically, or diagonally adjacent.
3. The length of the path is the total number of visited cells.

---

## State Representation

- A State class is defined to represent a position in the grid.

- Each state holds:

    - The grid itself.

    - Current coordinates ( i , j ).

    - The list of visited cells.

- Methods include:

    - goalTest(): Checks if the goal (n-1, n-1) is reached.

    - moveGen(): Generates valid child states by moving in 8 possible directions.

    - h(): Heuristic function that estimates distance to goal ( Euclidean or Manhattan distance to the goal ).

    - k_step_cost(): Returns the cost to move to a neighboring cell (set to 1 for uniform cost).

## Best First Search (BFS)
Uses only the heuristic h(n) to choose the next node.

Procedure:

- Start from (0,0) and put it into the open list.

- At each step, pick the node with the smallest h(n).

- If the goal is reached, return the path.

- Otherwise, expand the node and add unvisited children to the open list.

This approach greedily follows the heuristic and ignores the actual cost so far.

## A* Search
Uses both the cost so far g(n) and the heuristic h(n) to evaluate nodes with:

    f(n) = g(n) + h(n)

Procedure:

- Start from (0,0) with g(start)=0.

- At each step, pick the node with the smallest f(n).

- If the goal is reached, return the path.

- Otherwise, expand the node, update costs for children, and propagate improvements if a better path is found.

This ensures optimal paths if the heuristic is admissible.



## Difference between BFS and A*

- Best First Search relies only on the heuristic and making decisions based on how close a node appears to be to the goal.

    - faster exploration.
    - does not give optimal solution.
    - less efficient


- A Search*, combines the actual path cost with the heuristic. It balances progress toward the goal.

    - slower than BFS
    - gives optimal solution
    - more efficient

---

### Author
**Valakati Sri Sairam**