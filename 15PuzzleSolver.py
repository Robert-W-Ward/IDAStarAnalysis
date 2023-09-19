import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from time import sleep
from heapq import heappop, heappush

class PuzzleNode:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        # Represents the current state of the puzzle
        self.state = state
        # Parent node which led to this state
        self.parent = parent
        # Action that led to this state
        self.action = action
        # Total path cost to reach this state
        self.path_cost = path_cost
        # The goal state for 15-puzzle
        self.goal = (np.arange(1, 17).reshape(4, 4) % 16).tolist()
        # Heuristic value computed using Manhattan distance
        self.heuristic = self.calculate_heuristic()
        # f is the estimated total cost of the cheapest solution through this node
        self.f = self.path_cost + self.heuristic

    def calculate_heuristic(self):
        """ Calculate Manhattan Distance for heuristic """
        m_dist = 0
        for i in range(4):
            for j in range(4):
                # Only calculate distance for tiles, not the empty space (0)
                if self.state[i][j] != 0:
                    # Determine the goal position for current tile
                    goal_x, goal_y = divmod(self.state[i][j] - 1, 4)
                    # Add the distance of current tile from its goal position
                    m_dist += abs(i - goal_x) + abs(j - goal_y)
        return m_dist

    def __lt__(self, other):
        # Custom less than operation for heap operations, based on f value
        return self.f < other.f

    def generate_successors(self):
        """ Generate successor states by moving the empty tile """
        successors = []
        actions = [('L', (0,-1)), ('R', (0, 1)), ('D', (1, 0)), ('U', (-1, 0))]
        # Find the empty tile's coordinates
        empty_x, empty_y = np.where(np.array(self.state) == 0)
        empty_x, empty_y = int(empty_x), int(empty_y)

        # Try to move the empty tile in all 4 directions
        for action, (dx, dy) in actions:
            # here dx represents the change to the first index into the matrix which is what row its in 
            # and dy represents changing the column in that row
            new_x, new_y = empty_x + dx, empty_y + dy
            # Check for boundaries
            if 0 <= new_x < 4 and 0 <= new_y < 4:
                new_state = [row.copy() for row in self.state]
                # Swap the empty tile with its neighboring tile
                new_state[empty_x][empty_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[empty_x][empty_y]
                # Add the new state as a successor
                successors.append(PuzzleNode(new_state, self, action, self.path_cost + 1))

        return successors

    def solution(self):
        """ Trace back from this node to root to get the solution """
        actions = []
        node = self
        # Traverse up the tree to get all actions
        while node.parent:
            actions.append(node.action)
            node = node.parent
        # Reverse the actions to get them in order from root to this node
        return actions[::-1]

def show_grid(state, ax, text_objects):
    ax.clear()  # Clear previous texts and other drawings
    
    # Define a color matrix. Default color is white.
    color_matrix = np.ones((4, 4, 3)) # For RGB values
    
    # Get the goal state
    goal = (np.arange(1, 17).reshape(4, 4) % 16).tolist()
    
    # Check each element in the state, if it's at its proper position (as in the goal), 
    # set the corresponding position in the color matrix to green.
    for i in range(4):
        for j in range(4):
            if state[i][j] == goal[i][j]:
                color_matrix[i, j] = [0, 1, 0]  # RGB for green
            elif state[i][j] != goal[i][j]:
                color_matrix[i,j] = [1,0,0]
            elif stat[i][j] == 0:
                color_matrix[i,j] = [1,1,0]
    
    ax.imshow(color_matrix, vmin=0, vmax=1)  # Use the color matrix as the image
    
    # Display the numbers as before
    for i in range(4):
        for j in range(4):
            text_objects[i][j] = ax.text(j, i, str(state[i][j]), ha='center', va='center',
                                         fontsize=12, color="black")
            
    ax.set_xticks([])
    ax.set_yticks([])
    plt.draw()
    plt.pause(0.1)  # you can adjust this pause as needed



def deepening_astar(initial_state):
    """ Iterative deepening A* search for 15-puzzle """
    root = PuzzleNode(initial_state)
    
    # Check if initial state is already a goal state
    if root.heuristic == 0:
        return root.solution()

    # Start with heuristic of root as initial bound
    bound = root.heuristic

    while True:
        open_list = [root]
        closed_set = set()
        found = None
        next_bound = float('inf')  # set to infinity initially

        # Main search loop
        while open_list:
            current = heappop(open_list)
            
            # If the current state is a goal state
            if current.heuristic == 0:
                found = current
                break

            # Skip nodes with f value exceeding the bound
            if current.f > bound:
                next_bound = min(next_bound, current.f)  # keep track of the smallest value exceeding current bound
                continue

            # Expand the current node and add its successors to the open list
            for successor in current.generate_successors():
                hashable_state = tuple(map(tuple, successor.state))
                if hashable_state not in closed_set:
                    heappush(open_list, successor)
                    closed_set.add(hashable_state)
                    #show_grid(np.array(successor.state), ax, text_objects)

        # If a solution was found
        if found:
            return found.solution()

        # If no node exceeded the bound, it means there's no solution
        if next_bound == float('inf'):  # if next_bound remains unchanged
            return None

        # Update the bound for the next iteration
        bound = next_bound

if __name__ == "__main__":
    # Sample initial state
    initial = [
        [1, 2, 0, 8],
        [5, 6, 4, 7],
        [9, 10, 11, 3],
        [13, 14, 15, 12]
    ]
    plt.ion() # turn on interactive mode
    fig, ax = plt.subplots()

    text_objects = [[None for _ in range(4)] for _ in range(4)]
    # Solve the puzzle and print the solution
    solution = deepening_astar(initial)
    if solution:
        print(f"Solution found: {' '.join(solution)}")
    else:
        print("No solution found")    