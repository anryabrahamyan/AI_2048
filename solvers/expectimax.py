from heuristic import *
from game_class import *
import game_class
import heuristic

class expectimax_solver:
    def __init__(self, heuristic, game=None,depth=2):
        self.heuristic = heuristic
        if game is None:
            self.game = game_class.GAME()
            self.game.start_game()
        else:
            self.game = game
        self.depth=depth

    def solve(self):
        while self.game.get_current_state() == CONTINUE:
            action = self.search_one_step()
            # if action == WON:
            #     return WON
            if action == 'left':
                self.game.move_left()

            if action == 'right':
                self.game.move_right()
            if action == 'up':
                self.game.move_up()
            elif action =='down':
                self.game.move_down()
            # print(self.game.mat)
            self.game.add_new_2()#check add new 2

        return self.game.mat, self.game.score

    def search_one_step(self):
        steps = {i: 0 for i in self.game.get_applicable_actions()}
        for action in steps.keys():
            copy = GAME(board=self.game.mat)
            if action == 'left':
                copy.move_left()
            if action == 'right':
                copy.move_right()
            if action == 'up':
                copy.move_up()
            elif action=='down':
                copy.move_down()
            value = self.random_value(copy, 2)
            steps[action] = value
        return max(steps,key=steps.get)

    def max_value(self,game,depth):
        game=GAME(board=game.mat,score=game.score)
        if depth>2*self.depth:
            return self.heuristic(game.mat,game.score)
        steps={i:0 for i in game.get_applicable_actions()}
        if len(game.get_applicable_actions())==0:
            return 0
        for action in steps.keys():
            if action == 'left':
                game.move_left()
            if action == 'right':
                game.move_right()
            if action == 'up':
                game.move_up()
            elif action =='down':
                game.move_down()
            value=self.random_value(game,depth+1)
            steps[action]=value
        return max(steps.values())

    def random_value(self,game,depth):
        empty_=set([tuple(i) for i in np.argwhere(game.mat==0)])
        empty_tiles={i:0 for i in empty_}
        for tile in empty_tiles.keys():
            choice=[]
            for number in [(0.9,2),(0.1,4)]:
                game.mat[tile[0],tile[1]]=number[1]
                choice.append(number[0]*self.max_value(game,depth+1))
            empty_tiles[tile]=np.mean(choice)
        return np.mean(list(empty_tiles.values()))

if __name__=='__main__':
    from tqdm import tqdm
    import pandas as pd
    total_df=pd.DataFrame({'Configuration':[],'mean':[],'median':[],'max':[],'all_values':[]})
    heuristics=[heuristic.Heuristic.greedy,heuristic.Heuristic.empty,heuristic.Heuristic.uniform,heuristic.Heuristic.monoton,weighted_heuristic(np.array([[1,2,3,4],[8,7,6,5],[9,10,11,12],[16,15,14,13]]))]
    for depth in tqdm(range(1,5)):
        for heuristic in tqdm(heuristics):
            lst = []
            for i in tqdm(range(150)):
                b = expectimax_solver(heuristic=heuristic,depth=depth)
                lst.append(b.solve()[1])
            experiment=pd.DataFrame({'Configuration':[str(heuristics)+str(depth)],'mean':[np.mean(lst)],'median':[np.median(lst)],'max':[np.max(lst)],'all_values':[[lst]]})
            total_df=pd.concat([total_df,experiment])
        total_df.to_csv('Expectimax_combination_scores.csv',index=False)