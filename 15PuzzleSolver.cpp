#include <iostream>
#include <vector>
#include <limits>
#include <algorithm>
#include <string>
#include <fstream>
#include <sstream>
#include <chrono>
#include <cmath>


#define USELINEAR

const int INF = std::numeric_limits<int>::max();
const int FOUND = -1;
const int SIZE = 4;
int nodesExpanded = 0;
std::chrono::time_point<std::chrono::high_resolution_clock> start_time;
int max_depth = 0;

struct Node {
    std::vector<int> state; // Flat 1x16 vector representing the puzzle
    std::string steps; // Moves taken to get to this state
    int blankPos; // Position of the blank tile in the state vector
    int heuristic;
    bool operator==(const Node& other) const {
        return state == other.state;
    }
};

std::vector<Node> path; 


int ManhattanDistancePlusLinearDistance(Node node) {
    int distance = 0;
    int linearConflict = 0;

    for (int i = 0; i < SIZE * SIZE; i++) {
        if (node.state[i] != 0) {
            int currentRow = i / SIZE;
            int currentCol = i % SIZE;
            int targetRow = (node.state[i] - 1) / SIZE;
            int targetCol = (node.state[i] - 1) % SIZE;
            distance += abs(currentRow - targetRow) + abs(currentCol - targetCol);

            // Checking linear conflict in row
            for (int j = currentRow * SIZE; j < (currentRow + 1) * SIZE; j++) {
                if (j > i && node.state[j] != 0) { // Avoid reverse pair checking
                    int targetJRow = (node.state[j] - 1) / SIZE;
                    if(currentRow == targetJRow && (j % SIZE) > targetCol) 
                        linearConflict += 2;
                }
            }

            // Checking linear conflict in column
            for (int j = currentCol; j < SIZE * SIZE; j += SIZE) {
                if (j > i && node.state[j] != 0) {
                    int targetJCol = (node.state[j] - 1) % SIZE;
                    int targetJRow = (node.state[j] - 1) / SIZE;
                    if(currentCol == targetJCol && (j / SIZE) > targetRow) 
                        linearConflict += 2;
                }
            }
        }
    }

    return distance + linearConflict;
}



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
    nodesExpanded++;
    #ifdef USELINEAR
        node.heuristic = ManhattanDistancePlusLinearDistance(node);
    #elif
        node.heuristic = h(node);
    #endif
    int f = g + node.heuristic;
    max_depth = std::max(max_depth,g);
    if (f > bound) return f;
    if (is_goal(node)) return FOUND;

    //std::cerr << "Depth: " << max_depth << ", Nodes Expanded: " << nodesExpanded <<", Bound: " << bound<< std::endl;

    int min = INF;
    for (const Node& succ : successors(node)) {
        if (std::find(path.begin(), path.end(), succ) == path.end()) {
            path.push_back(succ);
            int t = search(g + 1, bound);
            if (t == FOUND) return FOUND;
            if (t < min) min = t;
            path.pop_back();
        }
    }

    return min;
}

std::pair<std::vector<Node>, int> ida_star(const Node& root) {
    start_time = std::chrono::high_resolution_clock::now();
    nodesExpanded = 0;
    #ifdef USELINEAR
        int bound = ManhattanDistancePlusLinearDistance(root);
    #else
        int bound = h(root);
    #endif
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
    for (int i = 0,j=i+1;i<state.size()-1;i++,j=i+1){
        int a = state[i];
        int b = state[j];
        if ((a && b) && a > b){
            inversions++;
        }
    }
    std::cerr<< inversions <<std::endl;
    return inversions;
}

bool isSolvable(const Node& node) {
    int inversions = countInversions(node.state);
    auto iter = std::find(node.state.begin(),node.state.end(),0);
    if (iter == node.state.end()) return false; //zero isn't even in the configuration so definately not solvable
    auto blankPos = std::distance(node.state.begin(),iter);
    int rowWithBlankNum = std::floor(blankPos/SIZE);// counted from the top starting at zero or from the bottom started at 1 either way the parity is the same
    if (SIZE % 2 == 0 ){
        if ((rowWithBlankNum %2 == 0 && inversions %2!=0)||(rowWithBlankNum%2!=0 && inversions %2==0))
            return true;
    }
    else{
        if (inversions %2 ==0){
            return true;
        }
    }
    return false;
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
    std::vector<Node> puzzles = readFromFile("solvedConfigurations.txt");

    for (int i = 0; i < puzzles.size(); i++) {
        //commented out be cause only going to operate on known solvable puzzles
        // if (!isSolvable(puzzles[i])) {
        //     std::cout << "Puzzle ";
        //     for (auto i : puzzles[i].state){
        //         std::cout << i << ' ';
        //     }
            
        //     std::cout<< " is not solvable." << std::endl;
        //     std::cout <<"\n"<<std::endl;
        //     continue;
        // }
        std::cout << "Solving puzzle " << i + 1 << ": ";
        for (auto i : puzzles[i].state)
        {
            std::cout<<i<<" ";
        }
        std::cout<<"\n";
        

       

        max_depth=0;
        auto result = ida_star(puzzles[i]);
        auto current_time = std::chrono::high_resolution_clock::now();
        auto inMiliseconds = std::chrono::duration_cast<std::chrono::milliseconds>(current_time-start_time);
        if (result.second != INF) {
            std::cout << "Path found with steps: " << result.first.back().steps << std::endl;
        } else {
            std::cout << "Path not found for puzzle " << i + 1 << "!" << std::endl;
        }
        std::cout << "Max search depth reached for puzzle " << i + 1 << ": " << max_depth << std::endl;
        std::cout << "Time taken " << inMiliseconds.count() << " ms"<<std::endl;
        std::cout<< "Nodes expanded " << nodesExpanded << std::endl;
        std::cout <<"\n"<<std::endl;
    }

    return 0;
}
