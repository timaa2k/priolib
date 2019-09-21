import datetime

from priolib.model import Task


class TestTask:

    def test_marshal_json(self) -> None:
        t = Task(
            id_='foo',
            title='bar',
            target='baz',
            status='foo',
            priority=1,
            created='2007-01-25T12:00:00Z',
            modified='2007-01-25T12:00:00Z',
        )
        json = (
            '{'
            '"id": "foo", '
            '"priority": 1, '
            '"status": "foo", '
            '"targetLink": "baz", '
            '"title": "bar"'
            '}'
        )
        assert json == t.marshal_json()

    def test_unmarshal_json(self) -> None:
        json = {}  # type = Dict[str, Any]
        json['id'] = 'foo'
        json['title'] = 'bar'
        json['targetLink'] = 'baz'
        json['status'] = 'foo'
        json['priority'] = 1
        json['createdDate'] = '2007-01-25T12:00:00Z'
        json['modifiedDate'] = '2007-01-25T12:00:00Z'
        task = Task.unmarshal_json(json)
        assert task.id == json['id']
        assert task.title == json['title']
        assert task.target == json['targetLink']
        assert task.status == json['status']
        assert task.priority == json['priority']
        assert task.created == datetime.datetime(
            2007, 1, 25, 12, 0, tzinfo=datetime.timezone.utc)
        assert task.modified == datetime.datetime(
            2007, 1, 25, 12, 0, tzinfo=datetime.timezone.utc)


class TestPlan:

    def test_unmarshal_json(self) -> None:
        pass
