import unittest

from todo_app import create_app, users, todos
from todo_app.models import Degree, Tag, User

app = create_app()

test_user = User(
    # this is not the actual user id as /signup generates a
    # uuid automatically
    id="",
    email="example@example.com",
    password="ExamplePass123",
    name="Example name")


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        self.register_and_login()

    def tearDown(self):
        self.ctx.pop()
        users.delete_one(dict(id=test_user.id))
        todos.delete_many(dict(userid=test_user.id))

    def register_and_login(self):
        self.client.post('/signup', data=dict(test_user))
        # replace id with actual id generated by /signup
        test_user.id = users.find_one({"email": test_user.email})["id"]
        self.client.post('/login', data=dict(test_user))

    def test_get_profile(self):
        response = self.client.get('/profile')
        self.assertIn(f'Welcome {test_user.name}!', response.text)

    def test_send_todo(self):
        response = self.send_todo('go walking', Degree.IMPORTANT, Tag.PERSONAL)
        self.assertEqual(response.status_code, 200)

    def test_get_todo(self):
        self.send_todo('go walking', Degree.IMPORTANT, Tag.PERSONAL)

        response = self.client.get('/')

        self.assertIn('go walking', response.text)
        self.assertIn('Important', response.text)
        self.assertIn('Personal', response.text)

    def test_todos_sorting(self):
        names = ['1st todo', '2nd todo', '3rd todo', '4th todo']
        # randomise send order to make sure it actually sorts them
        self.send_todo(names[2], Degree.UNIMPORTANT, Tag.WORK)
        self.send_todo(names[0], Degree.IMPORTANT, Tag.WORK)
        self.send_todo(names[3], Degree.UNIMPORTANT, Tag.PERSONAL)
        self.send_todo(names[1], Degree.IMPORTANT, Tag.PERSONAL)

        page = self.client.get('/').text
        positions = []
        for name in names:
            positions.append(page.index(name))

        # assert positions are sorted
        self.assertEqual(sorted(positions), positions,
                         "Todo sorting is not working")

    def send_todo(self, content: str, degree: Degree, tag: Tag):
        return self.client.post(
            '/',
            data=dict(
                content=content,
                degree=str(degree),
                tag=str(tag),
            ),
            follow_redirects=True
        )


if __name__ == "__main__":
    unittest.main()
