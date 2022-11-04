from typing import List, Dict, Tuple, Any, Type

class Parse:

    def __init__(self, width: int, height: int, rows: List[List[int]], columns: List[List[int]]) -> None:
        self.width = width
        self.height = height
        self.rows = rows
        self.columns = columns

    @staticmethod
    def validate_json(json_object: Dict[str, Any]) -> Tuple[List[str], "Parse"]:
        return [], Parse(json_object['width'],
                               json_object['height'],
                               json_object['rows'],
                               json_object['columns'])
