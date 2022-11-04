from typing import List
from State import State as State
from Parse import Parse
from Permutation import Permutation
import copy
import time

class PuzzleSolver:
    def __init__(self, Parse: Parse) -> None:
        self.Parse : Parse = Parse
        self.permutation: Permutation = Permutation(Parse)

    def _depth_first_search(self, row: int) -> None:
        if len(self.solutions) > 0: return  
        self.steps.append(copy.deepcopy(self.state._state))
        self.nodes += 1
        if row > self.max_row:
            self.max_row = row
            # print("Row: {}, nodes: {}, nodes/s: {:.2f}".format(
            #     self.max_row, self.nodes, self.nodes / (time.perf_counter() - self.start_time)
            # ))

        if not self.state.validate(row):
            return

        if row + 1 == self.Parse.height:
            # self.steps.append(copy.deepcopy(self.state._state))
            self.solutions.append(copy.deepcopy(self.state._state))
            return

        for perm in self.permutation.get_permutations(row+1):
            self.state.set_row(row+1, perm)
            self._depth_first_search(row+1)
            
        self.state.set_row(row+1, [None for _ in range(self.Parse.width)])
        

    def solve(self) -> List[State]:
        self.state : State = State(self.Parse)
        self.steps : List[State] = []
        self.solutions : List[State] = []
        
        self.nodes = -1
        self.max_row = 0
        self.start_time = time.perf_counter()
        self._depth_first_search(-1)

        return self.solutions, self.steps