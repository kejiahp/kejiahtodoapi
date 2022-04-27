from turtle import update
from urllib import response
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from todos.models import Todo

class TestAPI(APITestCase):
    def authenticate(self):
        login_sample = {"username":"testUser","email":"testemial@gmail.com","password":"testPassword"}
        self.client.post(reverse('register'),login_sample)

        response = self.client.post(reverse('login'),{"email":"testemial@gmail.com","password":"testPassword"})

        self.client.credentials(HTTP_AUTHORIZATION = f"Bearer {response.data['token']}",)

    def test_to_not_create_todo_with_no_user(self):
        sample_data = {"title":"Testing Title","desc":"Testing description"}
        response = self.client.post(reverse("todosCR"),sample_data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_create_todo_with_authenticated_user(self):
        self.authenticate()
        sample_data = {"title":"Testing Title","desc":"Testing description"}
        response = self.client.post(reverse("todosCR"),sample_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieves_all_todos(self):
        self.authenticate()
        response = self.client.get(reverse('todosCR'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

class TestRUDAPIView(TestAPI):

    def test_retrieve_todo(self):
        self.authenticate()
        sample_data = {"title":"Testing Title","desc":"Testing description"}
        response = self.client.post(reverse("todosCR"),sample_data)

        res = self.client.get(
            reverse('todoRUD', kwargs={"id":response.data["id"]})
            )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        todo_object = Todo.objects.get(id = response.data["id"])

        self.assertEqual(todo_object.title,res.data["title"])
        

    def test_update_todo(self):
        self.authenticate()
        sample_data = {"title":"Testing Title","desc":"Testing description"}
        response = self.client.post(reverse("todosCR"),sample_data)

        res = self.client.patch(
        reverse('todoRUD', kwargs={"id":response.data["id"]}),{
            "title":"UpdatedTitle","is_complete":True
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        todo = Todo.objects.get(id=response.data["id"])

        self.assertEqual(todo.is_complete, True)

        self.assertEqual(todo.title, "UpdatedTitle")

    def test_delete_todo(self):
        self.authenticate()
        sample_data = {"title":"Testing Title","desc":"Testing description"}
        response = self.client.post(reverse("todosCR"),sample_data)
        prev_db_count = Todo.objects.all().count()

        self.assertGreater(prev_db_count,0)
        self.assertEqual(prev_db_count,1)

        res = self.client.delete(
            reverse('todoRUD', kwargs={"id":response.data["id"]})
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        new_db_count = Todo.objects.all().count()

        self.assertEqual(new_db_count,0)


