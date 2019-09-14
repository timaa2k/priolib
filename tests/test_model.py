from priolib.model import Task


class TestTask:

    def test_to_json(self):
        t = Task(id_='foo', title='bar', target='baz')
        json = '{"id": "foo", "target": "baz", "title": "bar"}'
        assert json == t.toJSON()
