#include <iostream>
#include <vector>
#include <array>
#include <unordered_set>
#include <queue>
#include <chrono>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <optional>

using State = std::vector<int>;
using Action = std::pair<char,int>;

struct Node {
    Node* parent;
    State currentState;
    Action previousAction;
    int g; // Cost to reach current node
    int h; // heuristic cost
    int f;// total cost
    Node(){};
    Node(State init){
        this->parent = nullptr;
        currentState = init;
        previousAction = {' ',0};
        g = 0;
        h = calculateManhattanDistance();
        f = g + h;
        }
    Node(Node* parent,State newState, Action action, int pathCost){
        this->parent = parent;
        currentState = newState;
        previousAction = action;
        g = pathCost;
        h = calculateManhattanDistance();
        f = g + h;
    }

    std::vector<Action> traceBackSolution(){
        std::vector<Action> actions;
        Node* node = this;
        while(node->parent){
            actions.push_back(node->previousAction);
            node = node->parent;
        }
        return actions;
    }

    std::vector<Node*> generateSuccessors(){
        std::vector<Node*> successors;
        std::vector<Action> actions = {
            {'L',-1},
            {'R',1},
            {'D',4},
            {'U',-4}
        };

        int emptyPos = std::find(currentState.begin(),currentState.end(),0) - currentState.begin();

        for(const auto& action: actions){
            int newPos = emptyPos + action.second;

            if(0<= newPos && newPos < 16){
                State newState = currentState;
                std::swap(newState[emptyPos],newState[newPos]);
                successors.push_back(new Node(this,newState,action,g+1));
            }
        }
        return successors;

    }

    int calculateManhattanDistance() const {
        int distance = 0;
        for (int i = 0; i < 16; i++) {
            if(currentState[i]!=0){
                int goal_x = (currentState[i] - 1) / 4;
                int goal_y = (currentState[i] - 1) % 4;
                int current_x = i / 4;
                int current_y = i % 4;
                distance += std::abs(current_x - goal_x) + std::abs(current_y - goal_y);
            }
            
        }
        return distance;
    }

    bool operator<(const Node& other) const {
        return calculateManhattanDistance() < other.calculateManhattanDistance();
    }

   
};

std::tuple<std::vector<Action>,int,size_t> IDAStar(std::vector<int> initalState){
    Node root = Node(initalState);
    int depth = 0;
    size_t memory = 0;
    if(root.h == 0)
        return std::make_tuple(root.traceBackSolution(),depth,memory);

    int bound = root.h;

    while (true)
    {
        std::priority_queue<Node*> openList;
        openList.push(&root);
        std::unordered_set<std::string> closedSet;
        Node* found = nullptr;
        int nextBound = INT32_MAX;
        while (!openList.empty())
        {
            Node* current = openList.top();
            openList.pop();
            depth = std::max(depth,current->g);
            memory = std::max(memory,sizeof(openList));

            if(current->h == 0){
                found = current; 
                break;
            }   
            
            if (current->f > bound){
                nextBound = std::min(nextBound,current->f);continue;
            }
                

            for(Node* successor : current->generateSuccessors()){
                std::string hasableState = "";
                for(auto num : successor->currentState){
                    hasableState += std::to_string(num) + " ";
                }

                if(closedSet.find(hasableState) == closedSet.end()){
                    openList.push(successor);
                    closedSet.insert(hasableState);
                }
            }
           

           
        }
        if (found){
            return std::make_tuple(found->traceBackSolution(),depth,memory);
        }
        if (nextBound == INT32_MAX){
            return std::make_tuple(std::vector<Action>(),depth,memory);
        }
        bound = nextBound;
        
    }
    

}


std::vector<std::vector<int>> readPuzzleFile(const std::string& filename){

    std::vector<std::vector<int>> puzzles;
    std::ifstream file(filename);
    if (file.is_open()) {
        std::string line;
        while (std::getline(file, line)) {
            std::vector<int> puzzle;
            std::stringstream ss(line);
            int num;
            
            while (ss >> num)
                puzzle.push_back(num);
            
            if(puzzle.size() == 16)
                puzzles.push_back(puzzle);
            else
                break;
        }
        file.close();
    }

    return puzzles;

}
void writeSolutionFile(){

}


int main() {
    std::string filename = "puzzles.txt";
    std::vector<std::vector<int>> puzzles = readPuzzleFile("puzzles.txt");
    std::vector<std::tuple<std::vector<Action>,int,size_t,std::chrono::nanoseconds>> outputData;
    
    std::ofstream outfile("solutions.txt");

    for (size_t i = 0; i < puzzles.size(); i++)
    {
        auto startTime = std::chrono::high_resolution_clock::now();
        auto[solution,depth,memoryUsed] = IDAStar(puzzles[i]);
        auto elasped = std::chrono::high_resolution_clock::now() - startTime;
        outputData.push_back(std::make_tuple(solution,depth,memoryUsed,elasped));
    }


    for (const auto& data : outputData)
    {
        // Destructure the data tuple
        const auto& [solution, depth, memoryUsed, elapsed] = data;

        // Write solution steps
        for (const auto& step : solution)
        {
            outfile << step.first <<" ";
        }
        outfile << "\n";

        // Write other information
        outfile << "Depth: " << depth << "\n";
        outfile << "Memory Used: " << memoryUsed << "\n";
        outfile << "Time Elapsed (ns): " << elapsed.count() << "\n";
        outfile << "-----------------------\n";  // Separating each puzzle's result
    }
    
    outfile.close();  // Close the file when done writing
    
}
