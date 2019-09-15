from priolib.model import Task


class TestTask:

    def test_to_json(self):
        t = Task(id_='foo', title='bar', targetLink='baz')
        json = '{"id": "foo", "targetLink": "baz", "title": "bar"}'
        assert json == t.toJSON()
