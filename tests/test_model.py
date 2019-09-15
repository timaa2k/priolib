import textwrap

from priolib.model import Task


class TestTask:

    def test_to_json(self):
        t = Task(
            id_='foo',
            title='bar',
            target='baz',
            urgency='foo',
            created='2007-01-25T12:00:00Z',
            modified='2007-01-25T12:00:00Z',
        )
        json = (
            '{'
            '"id": "foo", '
            '"targetLink": "baz", '
            '"title": "bar", '
            '"urgencyLevel": "foo"'
            '}'
        )
        assert json == t.toJSON()
