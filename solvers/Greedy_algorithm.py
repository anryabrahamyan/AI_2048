from heuristic import *
from game_class import *
import game_class
import heuristic


class Greedy:
    def __init__(self, heuristics=[], game=None):
        """
         The heuristics that the algorithm will use to solve the problem
        Inputs: heuristics:the heuristics used by the algorithm.
                game : the game state to solve. Creates a random one if None.
        Outputs: returns a Greedy objects
        """
        self.heuristics = heuristics
        if game is None:
            self.game = game_class.GAME()
            self.game.start_game()
        else:
            self.game = game

    def solve(self):
        """
        The method for solving the problem
        Inputs: None
        Outputs: A tuple consisting of the losing state and the final score of the game.
        """
        while self.game.get_current_state() == CONTINUE:
            #searches one step and applies it until the game state is equal to LOSS.
            action = self.search_one_step()


            if action == 'left':
                self.game.move_left()

            if action == 'right':
                self.game.move_right()
            if action == 'up':
                self.game.move_up()
            else:
                self.game.move_down()
            self.game.add_new_2()

        return self.game.mat, self.game.score

    def search_one_step(self):
        """
        Function used by the solve method for finding the best step to make
        Inputs: None
        Outputs: a string of the best step to make
        """

        #get the applicable actions for the board to not consider actions that do not change the state.
        applicable_actions = self.game.get_applicable_actions()
        #instantiate a dictionary of scores
        step = {i: 0 for i in applicable_actions}
        same = True
        i = 0
        while same and i != len(self.heuristics) - 1:
            #take the ith heuristic in from the strategy
            heuristic = self.heuristics[i]
            #loop over the actions and get their resulting boards
            for action in step.keys():
                new_board = GAME(board=self.game.mat,score=self.game.score)
                # new_board.score=self.game.score
                if action == 'left':
                    new_board.move_left()
                if action == 'right':
                    new_board.move_right()
                if action == 'up':
                    new_board.move_up()
                else:
                    new_board.move_down()
                #update the score of the remaining actions
                step[action] = heuristic(new_board.mat,new_board.score)

            i += 1
            #check for tied scores to move on to the next action
            if len(set(step.values())) == len(step.keys()):
                return max(step, key=step.get)
            else:
                
                step = {i: value for i, value in step.items() if i == max(step, key=step.get)}
        #take the action with the highest value
        action = self.heuristics[i](applicable_actions)
        return action



if __name__ == '__main__':
    #The following code generates runs for each possible Greedy local search algorithms strategy configuration
    #The output is a csv
    from tqdm import tqdm
    from itertools import combinations,permutations
    import pandas as pd
    #instantiate empty experiment
    total_df=pd.DataFrame({'Configuration':[],'mean':[],'median':[],'max':[],'all_values':[]})
    #this is the set of implemented heuristics and the weighted tile heuristic for the s shape pattern.
    heuristics=[heuristic.Heuristic.greedy,heuristic.Heuristic.empty,heuristic.Heuristic.uniform,heuristic.Heuristic.monoton,weighted_heuristic(np.array([[1,2,3,4],[8,7,6,5],[9,10,11,12],[16,15,14,13]]))]
    combs=[]
    #create all the permuations and combinations
    for n in range(len(heuristics) + 1):
        combs += list(combinations(heuristics, n))
    permutation=[]
    for config in combs:
        permutation+=list(permutations(config))
    permutation=[i+tuple([heuristic.Heuristic.random]) for i in permutation]
    for perm in tqdm(permutation):
        lst = []
        for i in tqdm(range(300)):
            b = Greedy(heuristics=perm)
            lst.append(b.solve()[1])
        #add the results of the 300 runs to the dataframe
        experiment=pd.DataFrame({'Configuration':[perm],'mean':[np.mean(lst)],'median':[np.median(lst)],'max':[np.max(lst)],'all_values':[[lst]]})
        total_df=pd.concat([total_df,experiment])
    total_df.to_csv('Greedy_combination_scores.csv',index=False)
