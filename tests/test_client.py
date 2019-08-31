import pytest
import responses
from http import HTTPStatus

from priolib.client import APIClient, APIError
from priolib.model import Task


class TestAPIClient:

    @responses.activate
    def test_create_task(self):
        api = APIClient(addr='https://taskpr.io')
        responses.add(
            method=responses.POST,
            url='https://taskpr.io/tasks',
            headers={'Location': 'https://taskpr.io/tasks/0'},
            status=HTTPStatus.CREATED.value,
        )
        api.create_task(
            title='First task',
            target='https://example.com',
        )
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == 'https://taskpr.io/tasks'

    @responses.activate
    def test_create_task_failed(self):
        api = APIClient(addr='https://taskpr.io')
        responses.add(
            method=responses.POST,
            url='https://taskpr.io/tasks',
            json={
                'reason': 'Internal Server Error',
                'message': 'Task could not be created.',
                'details': 'A task storage error occurred.',
            },
            status=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
        with pytest.raises(APIError):
            api.create_task(
                title='First task',
                target='https://example.com',
            )
        assert len(responses.calls) == 3
        assert responses.calls[0].request.url == 'https://taskpr.io/tasks'

    @responses.activate
    def test_get_task(self):
        api = APIClient(addr='https://taskpr.io')
        responses.add(
            method=responses.GET,
            url='https://taskpr.io/tasks/0',
            json={
                'kind': 'Task',
                'self': 'https://taskpr.io/tasks/0',
                'id': 0,
                'title': 'First task',
                'target': 'https://example.com',
            },
            status=HTTPStatus.OK.value,
        )
        task = api.get_task(task_id=0)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == 'https://taskpr.io/tasks/0'
        assert task.id == 0
        assert task.title == 'First task'
        assert task.target == 'https://example.com'

    @responses.activate
    def test_delete_task(self):
        api = APIClient(addr='https://taskpr.io')
        responses.add(
            method=responses.DELETE,
            url='https://taskpr.io/tasks/0',
            status=HTTPStatus.NO_CONTENT.value,
        )
        api.delete_task(task_id=0)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == 'https://taskpr.io/tasks/0'

    @responses.activate
    def test_update_task(self):
        api = APIClient(addr='https://taskpr.io')
        responses.add(
            method=responses.PATCH,
            url='https://taskpr.io/tasks/0',
            status=HTTPStatus.NO_CONTENT.value,
        )
        updated = Task(id_=0, title='Updated task', target='https://new.com')
        api.update_task(task=updated)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == 'https://taskpr.io/tasks/0'

    @responses.activate
    def test_list_tasks(self):
        api = APIClient(addr='https://taskpr.io')
        responses.add(
            method=responses.GET,
            url='https://taskpr.io/tasks',
            json={
                'kind': 'Collection',
                'self': 'https://taskpr.io/tasks',
                'contents': [
                    {
                        'id': 2,
                        'kind': 'Task',
                        'self': 'https://taskpr.io/tasks/2',
                        'target': 'https://swiss.com',
                        'title': 'Buy cheese',
                    },
                    {
                        'id': 3,
                        'kind': 'Task',
                        'self': 'https://taskpr.io/tasks/3',
                        'target': 'https://stuff.org',
                        'title': 'Do stuff',
                    },
                ],
            },
            status=HTTPStatus.OK.value,
        )

        tasks = api.list_tasks(start=2, count=2)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == 'https://taskpr.io/tasks'

        assert len(tasks) == 2
        assert tasks[0].id == 2
        assert tasks[0].title == 'Buy cheese'
        assert tasks[0].target == 'https://swiss.com'
        assert tasks[1].id == 3
        assert tasks[1].title == 'Do stuff'
        assert tasks[1].target == 'https://stuff.org'
