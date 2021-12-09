# AI_2048
 implementation of 2048 and its solving methods.<br />
 The following code base consists of two source folders.
 
 ##game src folder
 Consists of the game implemenetation algorithm that contains the rules and the methods for interacting with the game.
 
 #solvers src folder
 Consists of the algorithms that aim to achieve the highest score while using the game class from the game src folder.
 
 ##running the code
 To run the code first clone the repository so that the game src folder files are also recognized as python files, otherwise put them in the same folder.
 ###Greedy local search algorithm
 To produce the data on the Greedy local search algorithm, run the Greedy_algorithm.py file which will output a csv file containing information regarding the runs for each configuration.
 ###Expectimax and Monte Carlo simulations
 The same way you can run the expecimax and the montecarlo simulations.

##Example of running a solver 
 ```bash
python Greedy_algorithm.py
```