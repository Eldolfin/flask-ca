import unittest
from todo_app import create_app
from todo_app.models import User

app = create_app()


class AppTestCase(unittest.TestCase):
    name = "Example name"

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        self.register_and_login()

    def register_and_login(self):
        email = "example@example.com"
        password = "ExamplePass123"
        self.client.post('/signup', data=dict(User(
            id="0",
            email=email,
            password=password,
            name=self.name)))

        self.client.post('/login', data=dict(
            email=email,
            password=password,
        ))

    def tearDown(self):
        self.ctx.pop()

    def test_get_profile(self):
        response = self.client.get('/profile')
        self.assertIn(f'Welcome {self.name}!', response.text)

    def test_send_todo(self):
        response = self.client.post(
            '/',
            data=dict(content='go walking',
                      degree='Important',
                      tag='Personal'),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    def test_get_todo(self):
        self.client.post(
            '/',
            data=dict(content='go walking',
                      degree='Important',
                      tag='Personal'),
            follow_redirects=True
        )

        response = self.client.get('/')

        self.assertIn('go walking', response.text)
        self.assertIn('Important', response.text)
        self.assertIn('Personal', response.text)


if __name__ == "__main__":
    unittest.main()
