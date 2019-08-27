import json
import requests
from typing import List

from .model import Task


DEFAULT_TIMEOUT = (3.05, 27)


class APIError(Exception):
    pass


class APIClient:

    def __init__(self, host: str, port: int = None) -> None:
        if port:
            self.addr = '{host}:{port}'.format(host=host, port=port)
        else:
            self.addr = host

    def create_task(self, title: str, target: str) -> int:
        headers = {'Content-Type': 'application/json'}
        payload = {'title': title, 'target': target}
        result = requests.post(
            url='{addr}/tasks'.format(addr=self.addr),
            headers=headers,
            data=json.dumps(payload),
            verify=False,
            timeout=DEFAULT_TIMEOUT,
        )
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError:
            raise APIError

        task_location = result.headers['Location']
        task_id = task_location.split('/')[-1]
        return int(task_id)

    def get_task(self, task_id: int) -> Task:
        headers = {'Accept': 'application/json'}
        result = requests.get(
            url='{addr}/tasks/{id_}'.format(addr=self.addr, id_=task_id),
            headers=headers,
            verify=False,
            timeout=DEFAULT_TIMEOUT,
        )
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError:
            raise APIError

        payload = result.json()
        t = Task(
            id_=payload['id'],
            title=payload['title'],
            target=payload['target'],
        )
        return t

    def delete_task(self, task_id: int) -> None:
        result = requests.delete(
            url='{addr}/tasks/{id_}'.format(addr=self.addr, id_=task_id),
            verify=False,
            timeout=DEFAULT_TIMEOUT,
        )
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError:
            raise APIError

    def update_task(self, task: Task) -> None:
        headers = {'Content-Type': 'application/json'}
        result = requests.patch(
            url='{addr}/tasks/{id_}'.format(addr=self.addr, id_=task.id),
            headers=headers,
            data=task.toJSON(),
            verify=False,
            timeout=DEFAULT_TIMEOUT,
        )
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError:
            raise APIError

    def list_tasks(self, start: int, count: int) -> List[Task]:
        headers = {'Accept': 'application/json'}
        result = requests.get(
            url='{addr}/tasks'.format(addr=self.addr),
            headers=headers,
            verify=False,
            timeout=DEFAULT_TIMEOUT,
        )
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError:
            raise APIError

        payload = result.json()

        tasks = []
        for item in payload['contents']:
            tasks.append(Task(
                id_=item['id'],
                title=item['title'],
                target=item['target'],
            ))
        return tasks
