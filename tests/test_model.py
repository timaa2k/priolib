import json
import datetime

import priolib.model


class TestTask:

    def test_marshal_json(self) -> None:
        t = priolib.model.Task(
            id_='foo',
            title='bar',
            target='baz',
            status='foo',
            priority=1,
            created='2007-01-25T12:00:00Z',
            modified='2007-01-25T12:00:00Z',
        )
        json_repr = (
            '{'
            '"id": "foo", '
            '"priority": 1, '
            '"status": "foo", '
            '"targetLink": "baz", '
            '"title": "bar"'
            '}'
        )
        assert json_repr == json.dumps(t, cls=priolib.model.Encoder, sort_keys=True)

    def test_unmarshal_json(self) -> None:
        json = {}  # type = Dict[str, Any]
        json['id'] = 'foo'
        json['title'] = 'bar'
        json['targetLink'] = 'baz'
        json['status'] = 'foo'
        json['priority'] = 1
        json['createdDate'] = '2007-01-25T12:00:00Z'
        json['modifiedDate'] = '2007-01-25T12:00:00Z'
        task = priolib.model.Task.unmarshal_json(json)
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

    # FIXME: Add tests for plan
    def test_unmarshal_json(self) -> None:
        pass

    def test_marshal_json(self) -> None:
        t = priolib.model.Task(
            id_='foo',
            title='bar',
            target='baz',
            status='foo',
            priority=1,
            created='2007-01-25T12:00:00Z',
            modified='2007-01-25T12:00:00Z',
        )
        p = priolib.model.Plan(
            done=[t],
            today=[t],
            todo=[t],
            blocked=[t],
            later=[t],
        )
        print(json.dumps(p, cls=priolib.model.Encoder, sort_keys=True))
        pass
