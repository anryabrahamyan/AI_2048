import game_class
from game_class import CONTINUE, LOSS, WON


def play_game():
    game = game_class.GAME()
    game.start_game()

    while True:

        # taking the user input
        # for next step
        x = input("Press the command : ")

        # we have to move up
        if x == 'W' or x == 'w':

            # call the move_up function
            flag = game.move_up()

            # get the current state and print it
            status = game.get_current_state()
            print(status)
            print(game.score)

            # if game not ove then continue
            # and add a new two
            if status == CONTINUE:
                game.add_new_2()

            # else break the loop
            elif status == WON:
                return WON

            else:
                return LOSS

        # the above process will be followed
        # in case of each type of move
        # below

        # to move down
        elif x == 'S' or x == 's':
            flag = game.move_down()
            status = game.get_current_state()
            print(status)
            print(game.score)
            if status == CONTINUE:
                game.add_new_2()

            elif status == WON:
                return WON

            else:
                return LOSS

        # to move left
        elif x == 'A' or x == 'a':
            flag = game.move_left()
            status = game.get_current_state()
            print(status)
            print(game.score)
            if status == CONTINUE:
                game.add_new_2()

            elif status == WON:
                return WON

            else:
                return LOSS

        # to move right
        elif x == 'D' or x == 'd':
            flag = game.move_right()
            status = game.get_current_state()
            print(status)
            print(game.score)
            if status == CONTINUE:
                game.add_new_2()

            elif status == WON:
                return WON

            else:
                return LOSS
        else:
            print("Invalid Key Pressed")

        # print the matrix after each
        # move.
        for i, row in enumerate(game.mat):
            print(game.mat[i])


if __name__ == '__main__':
    result = play_game()
