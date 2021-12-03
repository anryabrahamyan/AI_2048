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
            if action == WON:
                return action
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
                new_board = GAME(board=self.game.mat)
                new_board.score=self.game.score
                if action == 'left':
                    new_board.move_left()
                if action == 'right':
                    new_board.move_right()
                if action == 'up':
                    new_board.move_up()
                else:
                    new_board.move_down()

                if new_board.get_current_state == WON:
                    return new_board.get_current_state

                step[action] = heuristic(new_board.mat,new_board.score)

            i += 1
            if len(set(step.values())) == len(step.keys()):
                return max(step, key=step.get)
                same = False
            else:
                step = {i: value for i, value in step.items() if value == max(step, key=step.get)}
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
    a = Greedy(heuristics=[heuristic.Heuristic.empty, heuristic.Heuristic.random])
    lst = []
    for i in tqdm(range(1000)):
        b = Greedy(heuristics=[heuristic.Heuristic.empty, heuristic.Heuristic.random])
        lst.append(b.solve())
    print(np.mean(lst))