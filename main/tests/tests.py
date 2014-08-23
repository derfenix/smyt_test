import datetime
from django.db.models.loading import get_model
from django.test import TestCase
from django.test.client import Client
from django.utils import timezone


class Test(TestCase):
    def test_builder(self):
        users = get_model('main', 'users')
        self.assertTrue(users)
        rooms = get_model('main', 'rooms')
        self.assertTrue(rooms)

        rooms = get_model('main', 'room')
        self.assertFalse(rooms)

    def test_models(self):
        users = get_model('main', 'users')
        user = users(name="test", paycheck=1000, date_joined=timezone.now())
        user.save()

        user = users.objects.first()
        self.assertEqual(user.paycheck, 1000)
        self.assertEqual(user.name, 'test')

        rooms = get_model('main', 'rooms')
        room = rooms(department="test", spots=1000, owner='Budda')
        room.save()

        room = rooms.objects.first()
        self.assertEqual(room.spots, 1000)
        self.assertEqual(room.department, 'test')
        self.assertEqual(room.owner, 'Budda')

    def test_get_pages(self):
        client = Client()

        users = client.get('/users/')
        self.assertEqual(users.status_code, 200)

        rooms = client.get('/rooms/')
        self.assertEqual(rooms.status_code, 200)

    def test_save_new(self):
        client = Client()
        users = get_model('main', 'users')
        rooms = get_model('main', 'rooms')

        data = {'new': True, "name": "test", "paycheck": 100, "date_joined": "22-02-2012"}
        res = client.post('/users/', data=data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, 'error')
        user = users.objects.first()
        self.assertEqual(user.paycheck, 100)
        self.assertEqual(user.name, u'test')

        data = {'new': True, "department": "test", "spots": 200, "owner": "Budda"}
        res = client.post('/rooms/', data=data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, 'error')
        room = rooms.objects.first()
        self.assertEqual(room.department, u"test")
        self.assertEqual(room.spots, 200)
        self.assertEqual(room.owner, u"Budda")

        data = {'new': True, "name": "test", "paycheck": 'aaa', "date_joined": "2012-02-22"}
        res = client.post('/users/', data=data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'error')

        data = {'new': True, "name": "test", "paycheck": 100, "date_joined": "20120222"}
        res = client.post('/users/', data=data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Enter a valid date.')

        data = {'new': True, "department": "test", "spots": 'aaa', "owner": "Budda"}
        res = client.post('/rooms/', data=data)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Enter a whole number')

    def test_update_items_users(self):
        client = Client()

        users = get_model('main', 'users')
        user = users(name="test", paycheck=1000, date_joined=timezone.now())
        user.save()

        data = {'id': 1, 'field': 'name', 'value': "test2"}
        res = client.post('/users/', data)
        self.assertEqual(res.content, '0')
        self.assertEqual(users.objects.first().name, 'test2')

        data = {'id': 1, 'field': 'paycheck', 'value': "500"}
        res = client.post('/users/', data)
        self.assertEqual(res.content, '0')
        self.assertEqual(users.objects.first().paycheck, 500)

        data = {'id': 1, 'field': 'paycheck', 'value': "bbb"}
        res = client.post('/users/', data)
        self.assertEqual(res.content, 'Value is in wrong format')

        data = {'id': 1, 'field': 'date_joined', 'value': "10-05-2012"}
        res = client.post('/users/', data)
        self.assertEqual(res.content, '0')
        self.assertEqual(users.objects.first().date_joined, datetime.date(2012, 5, 10))

        data = {'id': 1, 'field': 'date_joined', 'value': "10052012"}
        res = client.post('/users/', data)
        self.assertEqual(res.content, 'Value is in wrong format')

    def test_update_items_rooms(self):
        client = Client()

        rooms = get_model('main', 'rooms')
        room = rooms(department="test", spots=1000, owner='Budda')
        room.save()

        data = {'id': 1, 'field': 'department', 'value': "test2"}
        res = client.post('/rooms/', data)
        self.assertEqual(res.content, '0')
        self.assertEqual(rooms.objects.first().department, 'test2')

        data = {'id': 1, 'field': 'spots', 'value': "500"}
        res = client.post('/rooms/', data)
        self.assertEqual(res.content, '0')
        self.assertEqual(rooms.objects.first().spots, 500)

        data = {'id': 1, 'field': 'spots', 'value': "bbb"}
        res = client.post('/rooms/', data)
        self.assertEqual(res.content, 'Value is in wrong format')

        data = {'id': 1, 'field': 'owner', 'value': "Boom"}
        res = client.post('/rooms/', data)
        self.assertEqual(res.content, '0')
        self.assertEqual(rooms.objects.first().owner, "Boom")