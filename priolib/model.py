import json


class Task:

    def __init__(self, id_: int, title: str, target: str) -> None:
        self.id = id_
        self.title = title
        self.target = target

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
        )
