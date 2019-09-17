from typing import Optional

import iso8601
import json


class Task:

    def __init__(
        self,
        id_: str,
        title: Optional[str] = None,
        target: Optional[str] = None,
        status: Optional[str] = None,
        created: Optional[str] = None,
        modified: Optional[str] = None,
    ) -> None:
        self.id = id_
        self.title = title
        self.target = target
        self.status = status
        self.created = iso8601.parse_date(created) if created else None
        self.modified = iso8601.parse_date(modified) if modified else None

    def __str__(self) -> str:
        return f'({self.id}, {self.title}, {self.target}, {self.status}, {self.created}, {self.modified})'

    def toJSON(self):
        o = {}
        o['id'] = self.id
        if self.title:
            o['title'] = self.title
        if self.target:
            o['targetLink'] = self.target
        if self.status:
            o['status'] = self.status
        return json.dumps(obj=o, sort_keys=True)
