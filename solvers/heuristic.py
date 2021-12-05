import numpy as np
import random



class Heuristic:
    @staticmethod
    def greedy(board,score):
        return score

    @staticmethod
    def empty(board,sore=0):
        return np.where (board==0,1,0).sum()


    @staticmethod
    def uniform(board,score=0):
        _,counts=np.unique(board,return_counts=True)
        return np.sum(np.power(counts[1:],3))



    @staticmethod
    def monoton(board,score=0):
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

    @staticmethod
    def random(steps):
        return random.choice(steps)

class weighted_heuristic:
    def __init__(self,weights=np.array([[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]])):
        self.weights=weights

    def __call__(self,matrix,score=0):
        return np.sum(np.multiply(self.weights,matrix))

if __name__=='__main__':
    a=np.array([[0,1,3,2],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    print(Heuristic.empty(a))
