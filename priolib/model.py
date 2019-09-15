import json


class Task:

    def __init__(self, id_: int, title: str, targetLink: str) -> None:
        self.id = id_
        self.title = title
        self.targetLink = targetLink

    def __str__(self) -> str:
        return f'({self.id}, {self.title}, {self.targetLink})'

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
        )
