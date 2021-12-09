from game_class import *
import game_class
import math
import random
import numpy as np


class MonteCarlo:
    def __init__(self,game=None):

        if game is None:
            self.game = game_class.GAME()
            self.game.start_game()
        else:
            self.game = game

    def solve(self):
        while self.game.get_current_state() == CONTINUE:
            action=self.search_one_step()
            if action == 'left':
                self.game.move_left()

            if action == 'right':
                self.game.move_right()
            if action == 'up':
                self.game.move_up()
            else:
                self.game.move_down()

            self.game.add_new_2()



        return (self.game.mat, self.game.score)


    def search_one_step(self):

        TOTAL_SIMULATIONS =40
        POSSIBLE_MOVES = ['left','right','down','up']

        moveSimulationTotalScores = [0,0,0,0]

        index=0
        for move in POSSIBLE_MOVES:

            for i in range(TOTAL_SIMULATIONS//4):
                simulation=GAME(board=self.game.mat)
                if move == 'left':
                    simulation.move_left()
                elif move == 'right':
                    simulation.move_right()
                elif move == 'up':
                    simulation.move_up()
                else:
                    simulation.move_down()
                self.game.add_new_2()


                while simulation.get_current_state() ==CONTINUE:
                    p=POSSIBLE_MOVES[math.floor(random.random() * 4)]
                    if p == 'left':
                        simulation.move_left()
                    elif p == 'right':
                        simulation.move_right()
                    elif p == 'up':
                        simulation.move_up()
                    else:
                        simulation.move_down()
                    simulation.add_new_2()



                moveSimulationTotalScores[index]+=simulation.score
            index+=1

        topScore=max(moveSimulationTotalScores)
        topScoreIndex=moveSimulationTotalScores.index(topScore)
        bestMove=POSSIBLE_MOVES[topScoreIndex]


        return(bestMove)





if __name__ == '__main__':
    from tqdm import tqdm
    import pandas as pd

    total_df = pd.DataFrame({'Configuration': [], 'mean': [], 'median': [], 'max': [], 'all_values': []})

    l=[]
    for i in tqdm(range(50)):
        a = MonteCarlo()
        l.append(a.solve()[1])


    experiment = pd.DataFrame(
    {'Configuration': [40], 'mean': [np.mean(l)], 'median': [np.median(l)], 'max': [np.max(l)],
    'all_values': [[l]]})
    total_df = pd.concat([total_df, experiment])
    total_df.to_csv('MonteCarlo_scores.csv', index=False)






