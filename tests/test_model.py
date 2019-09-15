import textwrap

from priolib.model import Task


class TestTask:

    def test_to_json(self):
        t = Task(
            id_='foo',
            title='bar',
            target='baz',
            urgency='foo',
            created='bar',
            modified='baz',
        )
        json = (
            '{'
            '"createdDate": "bar", '
            '"id": "foo", '
            '"modifiedDate": "baz", '
            '"targetLink": "baz", '
            '"title": "bar", '
            '"urgencyLevel": "foo"'
            '}'
        )
        assert json == t.toJSON()
