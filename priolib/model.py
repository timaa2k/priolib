from typing import Optional

import json


class Task:

    def __init__(
        self,
        id_: int,
        title: str,
        target: str,
        urgency: Optional[str] = None,
        created: Optional[str] = None,
        modified: Optional[str] = None,
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
        o = {}
        o['id'] = self.id
        o['title'] = self.title
        o['targetLink'] = self.target
        if self.urgency is not None:
            o['urgencyLevel'] = self.urgency
        if self.urgency is not None:
            o['createdDate'] = self.created
        if self.urgency is not None:
            o['modifiedDate'] = self.modified
        return json.dumps(obj=o, sort_keys=True)
