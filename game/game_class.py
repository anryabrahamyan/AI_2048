# base from https://www.geeksforgeeks.org/2048-game-in-python/
import random
import numpy as np

CONTINUE = 'GAME NOT OVER'
WON = 'WON'
LOSS = 'LOST'


class GAME:
    def __init__(self, size=4,board=[],score=0):
        if len(board)!=0:
            self.game_size=len(board)
            self.mat=board
        else:
            self.game_size = size
            self.mat = np.zeros(shape=(size, size))
        self.score = score

    def start_game(self):
        self.add_new_2()
        self.add_new_2()

        # print(self.mat)
        # print("Commands are as follows : ")
        # print("'W' or 'w' : Move Up")
        # print("'S' or 's' : Move Down")
        # print("'A' or 'a' : Move Left")
        # print("'D' or 'd' : Move Right")

    def add_new_2(self):
        allowed_combinations = [(i, j) for i in range(self.game_size) for j in range(self.game_size)]
        random.shuffle(allowed_combinations)
        try:
            r, c = random.choice(allowed_combinations)
            allowed_combinations.remove((r, c))

            while self.mat[r, c] != 0:
                r, c = random.choice(allowed_combinations)
                allowed_combinations.remove((r, c))

            self.mat[r][c] = np.random.choice([2, 4], p=[0.9, 0.1])
        except:
            pass

    def get_current_state(self):
        for i in range(self.game_size):
            for j in range(self.game_size):
                if self.mat[i, j] == 2048:
                    return WON

        for i in range(self.game_size):
            for j in range(self.game_size):
                if self.mat[i, j] == 0:
                    return CONTINUE

        for i in range(self.game_size - 1):
            for j in range(self.game_size - 1):
                if self.mat[i, j] == self.mat[i + 1, j] or self.mat[i, j] == self.mat[i, j + 1]:
                    return CONTINUE

        for j in range(self.game_size - 1):
            if self.mat[self.game_size - 1, j] == self.mat[self.game_size - 1, j + 1]:
                return CONTINUE

        for i in range(self.game_size - 1):
            if self.mat[i, self.game_size - 1] == self.mat[i + 1, self.game_size - 1]:
                return CONTINUE

        # else we have lost the game
        return LOSS

    def compress(self):
        # bool variable to determine
        # any change happened or not
        changed = False

        # empty grid
        new_mat = np.zeros(shape=(self.game_size, self.game_size))

        # here we will shift entries
        # of each cell to it's extreme
        # left row by row
        # loop to traverse rows
        for i in range(self.game_size):
            pos = 0

            # loop to traverse each column
            # in respective row
            for j in range(self.game_size):
                if self.mat[i, j] != 0:

                    # if cell is non empty then
                    # we will shift it's number to
                    # previous empty cell in that row
                    # denoted by pos variable
                    new_mat[i, pos] = self.mat[i, j]

                    if j != pos:
                        changed = True
                    pos += 1

        self.mat = new_mat

        return changed

    def merge(self):
        changed = False

        for i in range(self.game_size):
            for j in range(self.game_size - 1):

                # if current cell has same value as
                # next cell in the row and they
                # are non empty then
                if self.mat[i, j] == self.mat[i, j + 1] and self.mat[i, j] != 0:
                    # double current cell value and
                    # empty the next cell
                    self.mat[i, j] = self.mat[i, j] * 2
                    self.mat[i, j + 1] = 0
                    self.score += self.mat[i, j]

                    # make bool variable True indicating
                    # the new grid after merging is
                    # different.
                    changed = True

        return changed

    # function to reverse the matrix
    # means reversing the content of
    # each row (reversing the sequence)
    def reverse(self):
        new_mat = np.zeros(shape=(self.game_size, self.game_size))
        for i in range(self.game_size):
            for j in range(self.game_size):
                new_mat[i, j] = self.mat[i, self.game_size - 1 - j]
                # new_mat[i].append(self.mat[i][self.game_size - 1 - j])

        self.mat = new_mat

    # function to get the transpose
    # of matrix means interchanging
    # rows and column
    def transpose(self):
        self.mat = self.mat.T
    # def transpose(self):
    #     new_mat = []
    #     for i in range(self.game_size):
    #         new_mat.append([])
    #         for j in range(self.game_size):
    #             new_mat[i].append(self.mat[j][i])
    #
    #     self.mat = new_mat

    # function to update the matrix
    # if we move / swipe left
    def move_left(self):
        # first compress the grid
        changed1 = self.compress()

        # then merge the cells.
        changed2 = self.merge()

        changed = changed1 or changed2

        # again compress after merging.
        temp = self.compress()
        # return new matrix and bool changed
        # telling whether the grid is same
        # or different
        return changed

    # function to update the matrix
    # if we move / swipe right
    def move_right(self):
        # to move right we just reverse
        # the matrix
        self.reverse()

        # then move left
        changed = self.move_left()

        # then again reverse matrix will
        # give us desired result
        self.reverse()
        return changed

    # function to update the matrix
    # if we move / swipe up
    def move_up(self):
        # to move up we just take
        # transpose of matrix
        self.transpose()

        # then move left (calling all
        # included functions) then
        changed = self.move_left()

        # again take transpose will give
        # desired results
        self.transpose()
        return changed

    # function to update the matrix
    # if we move / swipe down
    def move_down(self):
        # to move down we take transpose
        self.transpose()

        # move right and then again
        changed = self.move_right()

        # take transpose will give desired
        # results.
        self.transpose()

        return changed

    # this file only contains all the logic
    # functions to be called in main function
    # present in the other file

    def get_applicable_actions(self):
        ''' returns board config as well'''

        actions=[]

        left_board=GAME(board=self.mat).move_left()
        if left_board:
            actions.append('left')

        up_board=GAME(board=self.mat).move_up()
        if up_board:
            actions.append('up')

        right_board=GAME(board=self.mat).move_right()
        if right_board:
            actions.append('right')

        down_board = GAME(board=self.mat).move_down()
        if down_board:
            actions.append('down')

        return actions

    if __name__ == 'main':
        start_game()
