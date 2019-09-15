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
            '"created": "bar", '
            '"id": "foo", '
            '"modified": "baz", '
            '"target": "baz", '
            '"title": "bar", '
            '"urgency": "foo"'
            '}'
        )
        assert json == t.toJSON()
