from typing import Any, Dict, List, Optional

import iso8601
import json


class Task:

    def __init__(
        self,
        id_: str,
        title: Optional[str] = None,
        target: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
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

    def marshal_json(self) -> Dict[str, Any]:
        o = {}
        o['id'] = self.id
        if self.title:
            o['title'] = self.title
        if self.target:
            o['targetLink'] = self.target
        if self.status:
            o['status'] = self.status
        return o

    @classmethod
    def unmarshal_json(cls, json: Dict[str, Any]) -> 'Task':
        return cls(
            id_=json['id'],
            title=json['title'],
            target=json['targetLink'],
            status=json['status'],
            created=json['createdDate'],
            modified=json['modifiedDate'],
        )


class Plan:

    def __init__(
        self,
        done: List[Task],
        today: List[Task],
        todo: List[Task],
        blocked: List[Task],
        later: List[Task],
    ) -> None:
        self.done = done
        self.today = today
        self.todo = todo
        self.blocked = blocked
        self.later = later

    @classmethod
    def unmarshal_json(cls, json: Dict[str, Any]) -> 'Plan':
        plan = cls([], [], [], [], [])
        for status in json['contents']:
            tasks = []
            for item in status['contents']:
                tasks.append(Task.unmarshal_json(item))
            if status['status'] == 'Done':
                plan.done = tasks
            elif status['status'] == 'Today':
                plan.today = tasks
            elif status['status'] == 'Todo':
                plan.todo = tasks
            elif status['status'] == 'Blocked':
                plan.blocked = tasks
            elif status['status'] == 'Later':
                plan.later = tasks
            else:
                raise ValueError
        return plan

    def marshal_json(self) -> Dict[str, Any]:
        o = {}
        o['done'] = self.done
        o['today'] = self.today
        o['todo'] = self.todo
        o['blocked'] = self.blocked
        o['later'] = self.later
        return o


class Encoder(json.JSONEncoder):

    def default(self, obj: Any) -> Any:
        if hasattr(obj, 'marshal_json'):
            return obj.marshal_json()
        else:
            return json.JSONEncoder.default(self, obj)
