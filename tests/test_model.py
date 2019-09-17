import textwrap

from priolib.model import Task


class TestTask:

    def test_to_json(self):
        t = Task(
            id_='foo',
            title='bar',
            target='baz',
            status='foo',
            created='2007-01-25T12:00:00Z',
            modified='2007-01-25T12:00:00Z',
        )
        json = (
            '{'
            '"id": "foo", '
            '"status": "foo", '
            '"targetLink": "baz", '
            '"title": "bar"'
            '}'
        )
        assert json == t.toJSON()
