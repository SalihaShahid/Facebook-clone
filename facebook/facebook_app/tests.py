from django.test import TestCase
from django.test import SimpleTestCase
from .models import *
from datetime import date, datetime
from django.utils import timezone


# Create your tests here.
class UserModelTests(TestCase):
    def setUp(self):
        User.objects.create(
            email="f200147@cfd.nu.edu.pk",
            password="dora1234",
            date_of_birth=date(2002, 2, 24),
            gender="M",
            verification_code="WRteGc",
            verification_status=True,
            name="Doraemon",
        )

    def test_user_correct_name(self):
        user = User.objects.get(email="f200147@cfd.nu.edu.pk")
        self.assertEqual(user.name, "Doraemon")

    def test_user_correct_password(self):
        user = User.objects.get(email="f200147@cfd.nu.edu.pk")
        self.assertEqual(user.password, "dora1234")

    def test_user_correct_password(self):
        user = User.objects.get(email="f200147@cfd.nu.edu.pk")
        self.assertEqual(user.date_of_birth, date(2002, 2, 24))

    def test_user_correct_gender(self):
        user = User.objects.get(email="f200147@cfd.nu.edu.pk")
        self.assertEqual(user.gender, "M")

    def test_user_correct_verification_code(self):
        user = User.objects.get(email="f200147@cfd.nu.edu.pk")
        self.assertEqual(user.verification_code, "WRteGc")

    def test_user_correct_verification_status(self):
        user = User.objects.get(email="f200147@cfd.nu.edu.pk")
        self.assertEqual(user.verification_status, True)

    def test_user_incorrect_name(self):
        user = User.objects.get(email="f200147@cfd.nu.edu.pk")
        self.assertNotEqual(user.name, "Nobita")

    def test_user_incorrect_password(self):
        user = User.objects.get(email="f200147@cfd.nu.edu.pk")
        self.assertNotEqual(user.password, "do34")

    def test_user_incorrect_date_of_birth(self):
        user = User.objects.get(email="f200147@cfd.nu.edu.pk")
        self.assertNotEqual(user.date_of_birth, date(2004, 2, 24))

    def test_user_correct_gender(self):
        user = User.objects.get(email="f200147@cfd.nu.edu.pk")
        self.assertNotEqual(user.gender, "F")

    def test_user_incorrect_verification_code(self):
        user = User.objects.get(email="f200147@cfd.nu.edu.pk")
        self.assertNotEqual(user.verification_code, "RteGc")

    def test_user_incorrect_verification_status(self):
        user = User.objects.get(email="f200147@cfd.nu.edu.pk")
        self.assertNotEqual(user.verification_status, False)


class FriendRequestModelTest(TestCase):
    def setUp(self):
        FriendRequests.objects.create(
            user_email="f200147@cfd.nu.edu.pk",
            friend_email="salihashahid1102@gmail.com",
            approval_status=True,
        )

    def test_user_email(self):
        user = FriendRequests.objects.get(user_email="f200147@cfd.nu.edu.pk")
        self.assertEqual(user.user_email, "f200147@cfd.nu.edu.pk")

    def test_friend_email(self):
        user = FriendRequests.objects.get(user_email="f200147@cfd.nu.edu.pk")
        self.assertEqual(user.friend_email, "salihashahid1102@gmail.com")

    def test_approval_status(self):
        user = FriendRequests.objects.get(user_email="f200147@cfd.nu.edu.pk")
        self.assertEqual(user.approval_status, True)


class MessageModelTest(TestCase):
    def setUp(self):
        message = Message.objects.create(
            sender="f200147@cfd.nu.edu.pk",
            receiver="salihashahid1102@gmail.com",
            message="hello",
            time=timezone.datetime(2023, 7, 26, 9, 37, 48, 879083, tzinfo=timezone.utc),
        )

    def test_sender_email(self):
        message = Message.objects.get(sender="f200147@cfd.nu.edu.pk")
        self.assertEqual(message.sender, "f200147@cfd.nu.edu.pk")

    def test_receiver_email(self):
        message = Message.objects.get(sender="f200147@cfd.nu.edu.pk")
        self.assertEqual(message.receiver, "salihashahid1102@gmail.com")

    def test_message(self):
        message = Message.objects.get(sender="f200147@cfd.nu.edu.pk")
        self.assertEqual(message.message, "hello")

    def test_time(self):
        message = Message.objects.get(sender="f200147@cfd.nu.edu.pk")
        self.assertEqual(
            message.time,
            timezone.datetime(2023, 7, 26, 9, 37, 48, 879083, tzinfo=timezone.utc),
        )


class TestStausCodes(SimpleTestCase):
    def test_sign_up(self):
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, 200)

    def test_authenticate(self):
        response = self.client.get("/authenticatef200147@cfd.nu.edu.pk")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get("/search")
        self.assertEqual(response.status_code, 200)
