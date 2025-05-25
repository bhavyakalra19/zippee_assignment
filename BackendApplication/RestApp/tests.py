#command to run test case :- python3 manage.py test RestApp
#this command will run test case written in particular RestApp App of django

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import TaskModel
from .serializers import TaskModelSerializer

User = get_user_model()

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

class TaskModelViewTests(APITestCase):

    def setUp(self):
        self.owner_user = User.objects.create_user(username="owner1", password="pass@1234", role="OWNER")
        self.normal_user = User.objects.create_user(username="user1", password="pass@1234", role="OTHER")
        self.admin_user = User.objects.create_user(username="admin1", password="pass@1234", role="ADMIN")

        self.task1 = TaskModel.objects.create(title="Test Task 1", description="Desc 1")
        self.task2 = TaskModel.objects.create(title="Test Task 2", description="Desc 2")

        self.client = APIClient()

    #authorization
    def auth(self, user):
        token = get_token_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    #test case for get request
    def test_get_all_tasks_authenticated(self):
        self.auth(self.normal_user)
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    #test case for get request for single id
    def test_get_single_task(self):
        self.auth(self.normal_user)
        response = self.client.get(f'/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task1.title)

    #test case for get request if id doesn't exists
    def test_get_nonexistent_task_returns_204(self):
        self.auth(self.normal_user)
        response = self.client.get('/tasks/124/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #test case for post request
    def test_create_task(self):
        self.auth(self.normal_user)
        data = {"title": "New Task", "description": "Testing"}
        response = self.client.post('/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TaskModel.objects.count(), 3)

    #test case for put request
    def test_update_task(self):
        self.auth(self.normal_user)
        data = {"title": "New updated Title"}
        response = self.client.put(f'/tasks/{self.task1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, "New updated Title")

    #test case for delete id request
    def test_delete_task_as_owner(self):
        self.auth(self.owner_user)
        response = self.client.delete(f'/tasks/{self.task2.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TaskModel.objects.count(), 1)

    #test case for delete id request for other user(show forbidden for other user)
    def test_delete_task_as_non_owner_denied(self):
        self.auth(self.normal_user)
        response = self.client.delete(f'/tasks/{self.task2.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #test case for get request but unauthorized
    def test_unauthenticated_user_cannot_access(self):
        self.client.credentials() 
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
