from rest_framework.test import APITestCase
from authentication.models import User

class TestModel(APITestCase):
    
    def test_create_user(self):
        user = User.objects.create_user('elijah','popoolakejiah@gmail.com','kejiah12345')
        self.assertIsInstance(user,User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email, 'popoolakejiah@gmail.com')
    
    def test_create_super_user(self):
        user = User.objects.create_superuser('elijah','popoolakejiah@gmail.com','kejiah12345')
        self.assertIsInstance(user,User)
        self.assertEqual(user.email, 'popoolakejiah@gmail.com')
        self.assertTrue(user.is_staff)

    def test_without_username(self):
        self.assertRaises(ValueError, User.objects.create_user, username="",email='popoolakejiah@gmail.com',password='kejiah12345')

    def test_without_email(self):
        self.assertRaises(ValueError,User.objects.create_user,
        username="elijah",email='',password='kejiah12345'
        )

    def test_superuser_isStaff_false(self):
        self.assertRaises(ValueError,User.objects.create_superuser,username="elijah",email='popoolakejiah@gmail.com',password='kejiah12345',is_staff = False)

    def test_superuser_isSuperUser_false_withMessage(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_superuser=True."):
            User.objects.create_superuser(username="elijah",email='popoolakejiah@gmail.com',password='kejiah12345',is_superuser=False)