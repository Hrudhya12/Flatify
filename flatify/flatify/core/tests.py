from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Flat, Profile, TaskHistory
from .views import rotate_profiles, get_next_user


class BaseSetup(TestCase):
    def setUp(self):
        
        self.flat = Flat.objects.create(name="Test Flat")

        
        self.u1 = User.objects.create_user(username="user1", password="pass123")
        self.u2 = User.objects.create_user(username="user2", password="pass123")
        self.u3 = User.objects.create_user(username="user3", password="pass123")

        
        Profile.objects.create(user=self.u1, flat=self.flat, order=0)
        Profile.objects.create(user=self.u2, flat=self.flat, order=1)
        Profile.objects.create(user=self.u3, flat=self.flat, order=2)


class RotationTests(BaseSetup):
    def test_rotation_changes_order(self):
        rotate_profiles(self.flat, 'cleaning')

        orders = list(Profile.objects.filter(flat=self.flat).order_by('order'))
        self.assertEqual(orders[0].user.username, "user2")
        self.assertEqual(orders[1].user.username, "user3")
        self.assertEqual(orders[2].user.username, "user1")


class FairAssignmentTests(BaseSetup):
    def test_get_next_user_initial(self):
        
        next_user = get_next_user(self.flat, 'cleaning')
        self.assertEqual(next_user.username, "user1")

    def test_get_next_user_after_history(self):
        
        TaskHistory.objects.create(flat=self.flat, user=self.u1, task_type='cleaning')
        TaskHistory.objects.create(flat=self.flat, user=self.u1, task_type='cleaning')
        TaskHistory.objects.create(flat=self.flat, user=self.u2, task_type='cleaning')

        next_user = get_next_user(self.flat, 'cleaning')
        self.assertEqual(next_user.username, "user3")  


class CompleteTaskFlowTests(BaseSetup):
    def test_complete_task_creates_history(self):
        client = Client()
        client.login(username="user1", password="pass123")

        response = client.get(reverse('complete_task', args=['cleaning']))
        self.assertEqual(response.status_code, 302)  

        history = TaskHistory.objects.filter(flat=self.flat, user=self.u1)
        self.assertEqual(history.count(), 1)

    def test_dashboard_requires_login(self):
        client = Client()
        response = client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  
