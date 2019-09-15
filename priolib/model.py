import json


class Task:

    def __init__(
        self,
        id_: int,
        title: str,
        target: str,
        urgency: str,
        created: str,
        modified: str,
    ) -> None:
        self.id = id_
        self.title = title
        self.target = target
        self.urgency = urgency
        self.created = created
        self.modified = modified

    def __str__(self) -> str:
        return f'({self.id}, {self.title}, {self.target}, {self.urgency}, {self.created}, {self.modified})'

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
        )
