from priolib.model import Task


class TestTask:

    def test_to_json(self):
        t = Task(id_=1, title='foo', target='bar')
        json = '{"id": 1, "target": "bar", "title": "foo"}'
        assert json == t.toJSON()
