from priolib.client import APIClient
from priolib.model import Task
import responses


class TestAPIClient:

    @responses.activate
    def test_create_task(self):
        api = APIClient(host='https://taskpr.io')
        responses.add(
            method=responses.POST,
            url='https://taskpr.io/tasks',
            headers={'Location': 'https://taskpr.io/tasks/0'},
            status=201,
        )
        api.create_task(
            title='First task',
            target='https://example.com',
        )
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == 'https://taskpr.io/tasks'

    @responses.activate
    def test_get_tasks(self):
        api = APIClient(host='https://taskpr.io')
        responses.add(
            method=responses.GET,
            url='https://taskpr.io/tasks',
            json={
                'id': 0,
                'title': 'First task',
                'target': 'https://example.com',
            },
            status=200,
        )
        task = api.get_tasks(start=0, count=2)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == 'https://taskpr.io/tasks/0'

        assert task.title == 'First task'
        assert task.target == 'https://example.com'

    @responses.activate
    def test_get_task(self):
        api = APIClient(host='https://taskpr.io')
        responses.add(
            method=responses.GET,
            url='https://taskpr.io/tasks/0',
            json={
                'id': 0,
                'title': 'First task',
                'target': 'https://example.com',
            },
            status=200,
        )
        task = api.get_task(task_id=0)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == 'https://taskpr.io/tasks/0'

        assert task.title == 'First task'
        assert task.target == 'https://example.com'

    @responses.activate
    def test_delete_task(self):
        api = APIClient(host='https://taskpr.io')
        responses.add(
            method=responses.DELETE,
            url='https://taskpr.io/tasks/0',
            status=204,
        )
        api.delete_task(task_id=0)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == 'https://taskpr.io/tasks/0'

    @responses.activate
    def test_update_task(self):
        api = APIClient(host='https://taskpr.io')
        responses.add(
            method=responses.PATCH,
            url='https://taskpr.io/tasks/0',
            status=204,
        )
        updated = Task(id_=0, title='Updated task', target='https://new.com')
        api.update_task(task=updated)
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == 'https://taskpr.io/tasks/0'
