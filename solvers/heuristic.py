import numpy as np



class Heuristic:
    @staticmethod
    def greedy(score):
        return score

    @staticmethod
    def empty(board):
        return np.where (board==0,1,0).sum()


    @staticmethod
    def uniform(board):
        _,counts=np.unique(board,return_counts=True)
        return np.sum(np.power(counts[1:],3))



    @staticmethod
    def monoton(board):
        best=-1
        for i in (1,board.shape[0]):
            current=0
            for row in (0,board.shape[0]-1):
                for col in (0,board.shape[0]-2):
                    if board[row][col]>=board[row][col+1]:
                        current+=1

            for col in (0,board.shape[0]-1):
                for row in (0,board.shape[0]-2):
                    if board[row][col]>=board[row+1][col]:
                        current+=1
            if current>best:
                best=current
            np.rot90(board,axes=(1,0))
        return best




a=np.array([[0,1,3,2],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
print(Heuristic.monoton(a))

#asds