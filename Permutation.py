from typing import List, Dict
from State import State as State
from Parse import Parse    
    
class Permutation:
    def __init__(self, Parse: Parse) -> None:
        self.Parse = Parse
        self.cache: Dict[int, List[List[bool]]] = dict()

    def get_permutations(self, row: int) -> List[bool]:
        if row in self.cache:
            return self.cache[row]

        blocks: List[int] = self.Parse.rows[row]
        if not blocks:
            return [[State.EMPTY for _ in range(self.Parse.width)]]

        positions = [0]
        for block in range(1, len(blocks)):
            positions.append(positions[-1] + blocks[block - 1] + 1)
        self.cache[row] = []
        self._next_permutation(row, positions, len(positions) - 1)
        return self.cache[row]

    def _positions_to_row(self, row: int, positions: List[int]) -> List[bool]:
        blocks = [State.EMPTY for _ in range(self.Parse.width)]
        for index, pos in enumerate(positions):
            length = self.Parse.rows[row][index]
            blocks[pos:pos+length] = [State.BLOCK for _ in range(length)]
        
        return blocks

    def _can_shift(self, row: int, positions: List[int], block_index: int) -> bool:
        if block_index + 1 == len(positions):
            return positions[block_index] + self.Parse.rows[row][block_index] < self.Parse.width
        
        return positions[block_index] + self.Parse.rows[row][block_index] + 1 < positions[block_index + 1]

    def _next_permutation(self, row: int, positions: List[int], block_index: int) -> None:
        self.cache[row].append(self._positions_to_row(row, positions))
        if block_index < 0:
            return

        while self._can_shift(row, positions, block_index):
            positions[block_index] += 1
            self._next_permutation(row, [p for p in positions], block_index - 1)
        

        
