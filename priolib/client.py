import json
import requests
import retrying
from typing import Dict, List, Optional, Tuple

from .model import Task


DEFAULT_TIMEOUT = (3.05, 27)


class ConnectionError(Exception):
    pass


class APIError(Exception):

    def __init__(self, reason, message, details) -> None:
        super().__init__()
        self.reason = reason
        self.message = message
        self.details = details

    @classmethod
    def FromHTTPResponse(cls, response: requests.Response) -> 'APIError':
        try:
            error = response.json()
            return cls(
                reason=error['reason'],
                message=error['message'],
                details=error['details'],
            )
        except (ValueError, KeyError):
            return cls(
                reason=response.status_code,
                message='Unknown error state encountered.',
                details='Failure conditions may be transitional.',
            )


class HTTPClient:

    def __init__(
        self,
        verify: bool,
        timeout: Tuple[float, float] = DEFAULT_TIMEOUT,
        retries: int = 0,
    ) -> None:
        self.verify = verify
        self.timeout = timeout
        self.retries = retries

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[str] = None,
    ) -> requests.Response:
        """
        Retry HTTP request on ``ConnectionError`` and ``HTTPError``s.
        """
        @retrying.retry(
            stop_max_attempt_number=self.retries,
            retry_on_exception=lambda e: isinstance(
                e, requests.exceptions.ConnectionError)
                or isinstance(e, requests.exceptions.HTTPError),
        )
        def do_request() -> requests.Response:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                verify=self.verify,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response
        return do_request()


class APIClient:

    def __init__(self, addr: str, retries: int = 3) -> None:
        """
        Set API client retry behavior.

        """
        self.addr = addr
        self.http = HTTPClient(verify=False, retries=retries)

    def request(
        self,
        method: str,
        uri: str,
        headers: Dict[str, str] = {},
        data: Optional[str] = None,
    ) -> requests.Response:
        """
        Retry on any HTTP error.

        """
        try:
            return self.http.request(
                method=method,
                url=self.addr + uri,
                headers=headers,
                data=data,
            )
        except requests.exceptions.ConnectionError as exc:
            raise ConnectionError from exc
        except requests.exceptions.HTTPError as exc:
            raise APIError.FromHTTPResponse(exc.response)

    def create_task(self, title: str, target: str) -> int:
        """
        Create a new task on the server.

        Raises:
            APIError
        """
        response = self.request(
            method='POST',
            uri='/tasks',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({'title': title, 'target': target}),
        )
        task_location = response.headers['Location']
        task_id = task_location.split('/')[-1]
        return int(task_id)

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve task from server by task ID.

        Raises:
            APIError
        """
        response = self.request(
            method='GET',
            uri='/tasks/{id_}'.format(id_=task_id),
            headers={'Accept': 'application/json'},
        )
        payload = response.json()
        return Task(
            id_=payload['id'],
            title=payload['title'],
            target=payload['target'],
        )

    def delete_task(self, task_id: int) -> None:
        """
        Delete task by ID.

        Raises:
            APIError
        """
        self.request('DELETE', '/tasks/{id_}'.format(id_=task_id))

    def update_task(self, task: Task) -> None:
        """
        Update task identified by the task ID of the given task object.

        Raises:
            APIError
        """
        self.request(
            method='PATCH',
            uri='/tasks/{id_}'.format(id_=task.id),
            headers={'Content-Type': 'application/json'},
            data=task.toJSON(),
        )

    def list_tasks(self, start: int, count: int) -> List[Task]:
        """
        List tasks `count` number of tasks at a time paged from
        `start` index of all available tasks to list.

        Raises:
            APIError
        """
        response = self.request(
            method='GET',
            uri='/tasks',
            headers={'Accept': 'application/json'},
        )
        tasks = []
        for item in response.json()['contents']:
            tasks.append(Task(
                id_=item['id'],
                title=item['title'],
                target=item['target'],
            ))
        return tasks
