# base from https://www.geeksforgeeks.org/2048-game-in-python/

import random

CONTINUE = 'GAME NOT OVER'
WON = 'WON'
LOSS = 'LOST'


class GAME:
    def __init__(self, size=4):
        self.game_size = size
        self.mat = []

    def start_game(self):
        self.mat = []
        for i in range(self.game_size):
            self.mat.append([0] * self.game_size)

        print("Commands are as follows : ")
        print("'W' or 'w' : Move Up")
        print("'S' or 's' : Move Down")
        print("'A' or 'a' : Move Left")
        print("'D' or 'd' : Move Right")

        self.add_new_2()

    def add_new_2(self):
        r = random.randint(0, self.game_size - 1)
        c = random.randint(0, self.game_size - 1)

        while self.mat[r][c] != 0:
            r = random.randint(0, self.game_size - 1)
            c = random.randint(0, self.game_size - 1)

            # TODO fix infinite loop case

        self.mat[r][c] = 2

    def get_current_state(self):
        for i in range(self.game_size):
            for j in range(self.game_size):
                if self.mat[i][j] == 2048:
                    return WON

        for i in range(self.game_size):
            for j in range(self.game_size):
                if self.mat[i][j] == 0:
                    return CONTINUE

        for i in range(self.game_size - 1):
            for j in range(self.game_size - 1):
                if self.mat[i][j] == self.mat[i + 1][j] or self.mat[i][j] == self.mat[i][j + 1]:
                    return CONTINUE

        for j in range(self.game_size - 1):
            if self.mat[self.game_size - 1][j] == self.mat[self.game_size - 1][j + 1]:
                return CONTINUE

        for i in range(self.game_size - 1):
            if self.mat[i][self.game_size - 1] == self.mat[i + 1][self.game_size - 1]:
                return CONTINUE

        # else we have lost the game
        return LOSS

    def compress(self):
        # bool variable to determine
        # any change happened or not
        changed = False

        # empty grid
        new_mat = []

        # with all cells empty
        for i in range(self.game_size):
            new_mat.append([0] * self.game_size)

        # here we will shift entries
        # of each cell to it's extreme
        # left row by row
        # loop to traverse rows
        for i in range(self.game_size):
            pos = 0

            # loop to traverse each column
            # in respective row
            for j in range(self.game_size):
                if self.mat[i][j] != 0:

                    # if cell is non empty then
                    # we will shift it's number to
                    # previous empty cell in that row
                    # denoted by pos variable
                    new_mat[i][pos] = self.mat[i][j]

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
                if self.mat[i][j] == self.mat[i][j + 1] and self.mat[i][j] != 0:
                    # double current cell value and
                    # empty the next cell
                    self.mat[i][j] = self.mat[i][j] * 2
                    self.mat[i][j + 1] = 0

                    # make bool variable True indicating
                    # the new grid after merging is
                    # different.
                    changed = True

        return changed

    # function to reverse the matrix
    # means reversing the content of
    # each row (reversing the sequence)
    def reverse(self):
        new_mat = []
        for i in range(self.game_size):
            new_mat.append([])
            for j in range(self.game_size):
                new_mat[i].append(self.mat[i][self.game_size - 1 - j])

        self.mat = new_mat

    # function to get the transpose
    # of matrix means interchanging
    # rows and column
    def transpose(self):
        new_mat = []
        for i in range(self.game_size):
            new_mat.append([])
            for j in range(self.game_size):
                new_mat[i].append(self.mat[j][i])

        self.mat = new_mat

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

    if __name__ == 'main':
        start_game()