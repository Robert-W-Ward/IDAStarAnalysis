#include <iostream>
#include <vector>
#include <limits>
#include <algorithm>
#include <string>
#include <fstream>
#include <sstream>
#include <chrono>

const int INF = std::numeric_limits<int>::max();
const int FOUND = -1;
const int SIZE = 4;
std::chrono::time_point<std::chrono::high_resolution_clock> start_time;
int max_depth = 0;

struct Node {
    std::vector<int> state; // Flat 1x16 vector representing the puzzle
    std::string steps; // Moves taken to get to this state
    int blankPos; // Position of the blank tile in the state vector

    bool operator==(const Node& other) const {
        return state == other.state;
    }
};

std::vector<Node> path; 

// Define heuristic, goal state, cost function, and successors
int h(const Node& node) {
    int distance = 0;
    for (int i = 0; i < SIZE * SIZE; i++) {
        if (node.state[i] != 0) { 
            int currentRow = i / SIZE;
            int currentCol = i % SIZE;
            int targetRow = (node.state[i] - 1) / SIZE;
            int targetCol = (node.state[i] - 1) % SIZE;
            distance += abs(currentRow - targetRow) + abs(currentCol - targetCol);
        }
    }
    return distance;
}

bool is_goal(const Node& node) {
    for (int i = 0; i < SIZE * SIZE - 1; i++) {
        if (node.state[i] != i + 1) return false;
    }
    return node.state.back() == 0; // Blank tile is at the end
}

int cost(const Node& node, const Node& succ) {
    return 1; // Uniform cost
}

std::vector<Node> successors(const Node& node) {
    std::vector<Node> neighbors;
    std::vector<int> moves = {-1, 1, -SIZE, SIZE}; 
    std::string moveChars = "LRUD";

    for (int i = 0; i < 4; i++) {
        int newPos = node.blankPos + moves[i];
        
        // Handle grid boundaries
        if (newPos >= 0 && newPos < SIZE * SIZE) {
            // Disallow wrapping moves between rows
            if ((node.blankPos % SIZE == 0 && i == 0) || // Leftmost and moving left
                (node.blankPos % SIZE == SIZE - 1 && i == 1)) { // Rightmost and moving right
                continue;
            }

            Node newNode = node;
            std::swap(newNode.state[newPos], newNode.state[node.blankPos]);
            newNode.blankPos = newPos;
            newNode.steps += moveChars[i];
            newNode.steps += ' ';
            neighbors.push_back(newNode);
        }
    }

    return neighbors;
}

int search(int g, int bound) {
    Node node = path.back();
    int f = g + h(node);
    max_depth = std::max(max_depth,g);
    if (f > bound) return f;
    if (is_goal(node)) return FOUND;
    int min = INF;
    auto current_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::minutes>(current_time - start_time);
    if (duration.count() >= 3){
        return INF;
    }
    for (const Node& succ : successors(node)) {
        if (std::find(path.begin(), path.end(), succ) == path.end()) {
            path.push_back(succ);
            int t = search(g + cost(node, succ), bound);
            if (t == FOUND) return FOUND;
            if (t < min) min = t;
            path.pop_back();
        }
    }

    return min;
}

std::pair<std::vector<Node>, int> ida_star(const Node& root) {
    start_time = std::chrono::high_resolution_clock::now();
    int bound = h(root);
    path = {root};
    while (true) {
        int t = search(0, bound);
        if (t == FOUND) return {path, bound};
        if (t == INF) return {{}, INF}; // Return an empty path for NOT_FOUND
        bound = t;
    }
}

int countInversions(std::vector<int> state){
    int inversions = 0;
    for (int i = 0; i < SIZE * SIZE - 1; i++) {
        for (int j = i + 1; j < SIZE * SIZE; j++) {
            if(state[j] && state[i] && state[i] > state[j])
                inversions++;
        }
    }
    return inversions;
}

bool isSolvable(const Node& node) {
    int inversions = countInversions(node.state);

    if (SIZE % 2 == 1) {  // Grid width is odd.
        return inversions % 2 == 0;
    } else {
        int rowWithBlank = (node.blankPos / SIZE);
        if (rowWithBlank % 2 == 1) {  // Blank is on an even row counting from the top (0-based)
            return inversions % 2 == 0;
        } else {  // Blank is on an odd row counting from the top (0-based)
            return inversions % 2 == 1;
        }
    }
}



std::vector<Node> readFromFile(const std::string& filename) {
    std::ifstream inFile(filename);
    std::vector<Node> puzzles;

    if (!inFile.is_open()) {
        std::cerr << "Failed to open " << filename << std::endl;
        return puzzles;
    }

    std::string line;
    while (std::getline(inFile, line)) {
        Node puzzle;
        std::istringstream iss(line);

        int value;
        for (int i = 0; i < SIZE * SIZE; i++) {
            if (!(iss >> value)) {
                std::cerr << "Error reading value for puzzle. Check file format." << std::endl;
                puzzles.clear();
                return puzzles;
            }
            puzzle.state.push_back(value);
            if (value == 0) {
                puzzle.blankPos = i;
            }
        }

        puzzles.push_back(puzzle);
    }

    return puzzles;
}

int main() {
    std::vector<Node> puzzles = readFromFile("puzzles.txt");

    for (int i = 0; i < puzzles.size(); i++) {
        std::cout << "Solving puzzle " << i + 1 << "..." << std::endl;

        if (!isSolvable(puzzles[i])) {
            std::cout << "Puzzle " << i +1 << " is not solvable." << std::endl;
            continue;
        }

        max_depth=0;
        auto result = ida_star(puzzles[i]);
        auto current_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::minutes>(current_time - start_time);

        if (result.second != INF) {
            std::cout << "Path found with steps: " << result.first.back().steps << std::endl;
        } else if (duration.count() >= 3) {
            std::cout << "Timeout after 3 minutes for puzzle " << i + 1 << ". Best path so far: " << path.back().steps << std::endl;
        } else {
            std::cout << "Path not found for puzzle " << i + 1 << "!" << std::endl;
        }
        std::cout << "Max search depth reached for puzzle " << i + 1 << ": " << max_depth << std::endl;

    }

    return 0;
}
