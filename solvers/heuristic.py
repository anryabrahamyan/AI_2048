import numpy as np
import random


#general class that includes all the implemented heuristics
class Heuristic:

    @staticmethod
    def greedy(board,score):
        """Implementation of the Greedy heuristic"""
        return score

    @staticmethod
    def empty(board,sore=0):
        """Implementation of the empty tiles heuristic"""
        return np.where (board==0,1,0).sum()


    @staticmethod
    def uniform(board,score=0):
        """Implementation of the uniformity heuristic"""
        _,counts=np.unique(board,return_counts=True)
        return np.sum(np.power(counts[1:],3))



    @staticmethod
    def monoton(board,score=0):
        """Implementation of the monotonicity heuristic"""
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
        """Implementation of the random move terminal heuristic"""
        return random.choice(steps)

class weighted_heuristic:
    def __init__(self,weights=np.array([[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]])):
        """Inputs: a 2D array corresponding to the weights of the tiles"""
        self.weights=weights

    def __call__(self,matrix,score=0):
        return np.sum(np.multiply(self.weights,matrix))

if __name__=='__main__':
    a=np.array([[0,1,3,2],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    print(Heuristic.empty(a))
