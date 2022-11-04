from Parse import Parse
from typing import Union, List
import numpy as np

class State:
    EMPTY = False
    BLOCK = True

    def __init__(self, Parse: Parse) -> None:
        self.Parse = Parse
        self._state = [
            [None for _ in range(Parse.width)] for _ in range(Parse.height)
        ]

    def _check_limits(self, row: int, column: int) -> bool:
        return (0 <= row < self.Parse.height) and \
               (0 <= column < self.Parse.width)

    def set(self, row: int, column: int, value: Union[bool, None]) -> None:
        assert self._check_limits(row, column)
        self._state[row][column] = value

    def set_row(self, row: int, values: List[bool]) -> None:
        assert len(values) == self.Parse.width
        self._state[row] = values
        # print(self.__str__())

    def get(self, row: int, column: int) -> Union[bool, None]:
        assert self._check_limits(row, column)
        return self._state[row][column]

    def __str__(self) -> str:
        return "\n".join(
            [ "┌" + "".join('─' for _ in range(self.Parse.width)) + "┐" ] + \
            [ "│" + "".join(
                        "█" if self._state[i][j] else " " for j in range(self.Parse.width) 
                    ) + "│"
                    for i in range(self.Parse.height) ] + \
            [ "└" + "".join('─' for _ in range(self.Parse.width)) + "┘"]
        )
        
    def validate(self, completed_rows: int) -> bool:
        if completed_rows <= 0:
            return True
        completed_rows += 1
        for i in range(self.Parse.width):
            column_Parse = self.Parse.columns[i]
            if len(column_Parse) == 0:
                for j in range(completed_rows):
                    if self.get(j, i):
                        return False
                continue
            in_block = False 
            block_index = 0 
            num_cells = None 
            for j in range(completed_rows):
                if self.get(j, i): 
                    if in_block:
                        num_cells -= 1 
                        if num_cells < 0:
                            return False
                    else:
                        if block_index >= len(column_Parse):
                            return False 
                        num_cells = column_Parse[block_index] - 1
                        block_index += 1
                        in_block = True
                elif in_block:
                    if num_cells != 0: 
                        return False 
                    in_block = False
            if completed_rows == self.Parse.height and block_index != len(column_Parse):
                return False 
            remaining_cells = self.Parse.height - completed_rows
            remaining_Parse = column_Parse[block_index:]
            if sum(remaining_Parse) + len(remaining_Parse) - 1 > remaining_cells:
                return False
        return True 
    
