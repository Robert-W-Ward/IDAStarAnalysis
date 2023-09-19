import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from time import time
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
            elif state[i][j] == 0:
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
    start_time = time()
    memory_usage = sys.getsizeof(initial_state)

    root = PuzzleNode(initial_state)
    
    # Check if initial state is already a goal state
    if root.heuristic == 0:
        return root.solution(),0,time() - start_time, memory_usage

    # Start with heuristic of root as initial bound
    bound = root.heuristic

    while True:
        open_list = [root]
        closed_set = set()
        found = None
        next_bound = float('inf')  # set to infinity initially
        depth = 0 

        # Main search loop
        while open_list:
            current = heappop(open_list)
            depth = max(depth,current.path_cost)
            memory_usage = max(memory_usage,sys.getsizeof(open_list))
            
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
            return found.solution(), depth, time() - start_time, memory_usage

        # If no node exceeded the bound, it means there's no solution
        if next_bound == float('inf'):  # if next_bound remains unchanged
            return None, depth,time()-start_time,memory_usage

        # Update the bound for the next iteration
        bound = next_bound

def read_puzzles_from_file(filename):
    puzzles = []
    with open(filename, 'r') as f:
        for line in f:
            numbers = list(map(int, line.strip().split()))
            if len(numbers) != 16:  # Check if the line contains 16 numbers
                print("Warning: Invalid line encountered.")
                continue
            puzzle = [numbers[i:i+4] for i in range(0, 16, 4)]
            puzzles.append(puzzle)
    return puzzles

if __name__ == "__main__":
    # Read puzzles from a file
    filename = 'puzzles.txt'
    puzzles = read_puzzles_from_file(filename)

    with open("solutions.txt", "w") as sol_file:
        for idx, initial in enumerate(puzzles):
            print(f"Solving Puzzle {idx + 1}:")
            
            solution, depth, duration, memory = deepening_astar(initial)
            
            sol_file.write(f"Initial State for Puzzle {idx + 1}: {' '.join(map(str, [num for row in initial for num in row]))}\n")
            if solution:
                sol_file.write(f"Solution Steps: {' '.join(solution)}\n")
                sol_file.write(f"Depth of Solution: {depth}\n")
                sol_file.write(f"Time Taken: {duration:.4f} seconds\n")
                sol_file.write(f"Memory Used: {memory} bytes\n\n")
                print(f"Solution found: {' '.join(solution)}")
            else:
                sol_file.write("No solution found\n\n")
                print("No solution found")
            print("-----")