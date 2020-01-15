# delivery

For delivery companies, it is crucial to deliver packages efficiently.  This project is designed to solve a specific delivery problem: find the best route to deliver 40 packages using 2 trucks.  Some packages have special requirements, which must be incorporated in the program heuristically. 

This is an example of the Traveling Salesman Problem, which is NP-hard.  As a result, it will be extremely time consuming to find the optimal solution.  Nevertheless, it is possible to achieve near-optimal performance by using a much faster algorithm.  

The algorithm used in this project is the greedy algorithm.  It is an intuitive algorithm which makes decisions based on the locally optimal choice at any stage.  In this project, when choosing the package to be delivered next, the greedy algorithm always chooses the package with the shortest distance from the current location of the truck. Big-O anlaysis shows that this algorithm takes O(N^2) time and O(N) space, which is plausible even when data is large.

The structure of the project is as follows
* data/          
  Contains two excel files with package and distance data
* packages/     
  Contains helper modules
* main.py       
  Main module
* test.py       
  Unit test module
