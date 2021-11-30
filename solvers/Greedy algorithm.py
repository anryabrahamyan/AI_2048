from heuristic import *
from game_class import *
import game_class
import heuristic


# TODO connect heuristic file
# TODO add applicable actions logic to game class

class Greedy:
    def __init__(self, heuristics=[], game=None):
        self.heuristics = heuristics
        if game is None:
            self.game = game_class.GAME()
            self.game.start_game()
        else:
            self.game = game

    def search_one_step(self):
        applicable_actions = self.game.get_applicable_actions()
        step = {i: 0 for i in applicable_actions}
        same = True
        i = 0
        while same and i != len(self.heuristics) - 1:
            heuristic = self.heuristics[i]
            for action in step.keys():
                new_board = GAME(board=self.game.mat)
                if action == 'left':
                    new_board.move_left()
                if action == 'right':
                    new_board.move_right()
                if action == 'up':
                    new_board.move_up()
                else:
                    new_board.move_down()

                if new_board.get_current_state == 'WON' or new_board.get_current_state == 'LOSS':
                    return new_board.get_current_state

                step[action] = heuristic(new_board.mat)

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
    a = Greedy(heuristics=[heuristic.Heuristic.empty, heuristic.Heuristic.random])
    print(a.search_one_step())
