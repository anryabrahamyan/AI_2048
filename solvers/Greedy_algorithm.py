from heuristic import *
from game_class import *
import game_class
import heuristic


class Greedy:
    def __init__(self, heuristics=[], game=None):
        self.heuristics = heuristics
        if game is None:
            self.game = game_class.GAME()
            self.game.start_game()
        else:
            self.game = game

    def solve(self):
        while self.game.get_current_state() == CONTINUE:
            action = self.search_one_step()

            # if action == WON:
            #     return action
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
        applicable_actions = self.game.get_applicable_actions()
        step = {i: 0 for i in applicable_actions}
        same = True
        i = 0
        while same and i != len(self.heuristics) - 1:
            heuristic = self.heuristics[i]
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

                # if new_board.get_current_state == WON:
                #     return new_board.get_current_state

                step[action] = heuristic(new_board.mat,new_board.score)

            i += 1
            if len(set(step.values())) == len(step.keys()):
                return max(step, key=step.get)
            else:
                step = {i: value for i, value in step.items() if i == max(step, key=step.get)}
        action = self.heuristics[i](applicable_actions)
        return action

        # perform each action and get a new game config
        # value each config and save in steps
        # if some equal then apply next heuristic
        # repeat until random or not equal scores
        # return action with the highest score or random

    # def solve(self):
    #     #search a step
    #     #apply the step
    #     #repeat until loss or win
    #     #print the board and the score each time


if __name__ == '__main__':
    from tqdm import tqdm
    from itertools import combinations,permutations
    import pandas as pd
    total_df=pd.DataFrame({'Configuration':[],'mean':[],'median':[],'max':[],'all_values':[]})
    heuristics=[heuristic.Heuristic.greedy,heuristic.Heuristic.empty,heuristic.Heuristic.uniform,heuristic.Heuristic.monoton,weighted_heuristic(np.array([[1,2,3,4],[8,7,6,5],[9,10,11,12],[16,15,14,13]]))]
    combs=[]
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
        experiment=pd.DataFrame({'Configuration':[perm],'mean':[np.mean(lst)],'median':[np.median(lst)],'max':[np.max(lst)],'all_values':[[lst]]})
        total_df=pd.concat([total_df,experiment])
    total_df.to_csv('Greedy_combination_scores.csv',index=False)
