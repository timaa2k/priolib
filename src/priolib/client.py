import json
from typing import Dict, List, Optional, Tuple, Union, Any

import requests
import retrying

from .model import Encoder, Plan, Task


DEFAULT_TIMEOUT = (3.05, 27)


class ConnectionError(Exception):
    pass


class APIError(Exception):

    def __init__(self, reason: str, message: str, details: str) -> None:
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
                reason=response.reason,
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
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[str] = None,
    ) -> Union[requests.Response, Any]:
        """
        Retry HTTP request on ``ConnectionError`` and ``HTTPError``s.
        """
        @retrying.retry(
            stop_max_attempt_number=self.retries,
            retry_on_exception=lambda e: isinstance(
                e, requests.exceptions.ConnectionError) or isinstance(
                    e, requests.exceptions.HTTPError),
        )
        def do_request() -> requests.Response:
            response = requests.request(
                method=method,
                url=url,
                params=params,
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
        params: Dict[str, str] = {},
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
                params=params,
                headers=headers,
                data=data,
            )
        except requests.exceptions.ConnectionError as exc:
            raise ConnectionError from exc
        except requests.exceptions.HTTPError as exc:
            raise APIError.FromHTTPResponse(exc.response)

    def create_task(
        self,
        title: str,
        target: str,
        status: Optional[str] = '',
    ) -> str:
        """
        Create a new task on the server.

        Raises:
            APIError
        """
        payload = {'title': title, 'targetLink': target, 'status': status}
        response = self.request(
            method='POST',
            uri='/tasks',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload),
        )
        task_location = response.headers['Location']
        task_id = task_location.split('/')[-1]
        return task_id

    def get_task(self, task_id: str) -> Task:
        """
        Retrieve task from server by task ID.

        Raises:
            APIError
        """
        response = self.request(
            method='GET',
            uri=f'/tasks/{task_id}',
            headers={'Accept': 'application/json'},
        )
        payload = response.json()
        return Task.unmarshal_json(payload)

    def delete_task(self, task_id: str) -> None:
        """
        Delete task by ID.

        Raises:
            APIError
        """
        self.request('DELETE', f'/tasks/{task_id}')

    def update_task(self, task: Task) -> None:
        """
        Update task identified by the task ID of the given task object.

        Raises:
            APIError
        """
        self.request(
            method='PATCH',
            uri=f'/tasks/{task.id}',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(task, cls=Encoder, sort_keys=True),
        )

    def list_tasks(self) -> List[Task]:
        """
        List tasks ordered descending by creation date.

        Raises:
            APIError
        """
        response = self.request(
            method='GET',
            uri='/tasks',
            params={},
            headers={'Accept': 'application/json'},
        )
        tasks = []
        for item in response.json()['contents']:
            tasks.append(Task.unmarshal_json(item))
        return tasks

    def get_plan(self) -> Plan:
        """
        Get plan with tasks ordered by priority and status.

        Raises:
            APIError
        """
        response = self.request(
            method='GET',
            uri='/plan',
            params={},
            headers={'Accept': 'application/json'},
        )
        return Plan.unmarshal_json(response.json())

    def update_plan(self, plan: Plan) -> None:
        """
        Update plan with changed task status and priorities.

        Raises:
            APIError
        """
        self.request(
            method='POST',
            uri='/plan',
            params={},
            headers={'Content-Type': 'application/json'},
            data=json.dumps(plan, cls=Encoder, sort_keys=True),
        )
