from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class CookAdminTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="adminpassword"
        )
        self.client.force_login(self.admin_user)

        self.cook = get_user_model().objects.create_user(
            username="testcook",
            password="testpassword",
            first_name="John",
            last_name="Doe",
            years_of_experience="1"
        )

    def test_years_of_experience_listed(self):
        url = reverse("admin:kitchen_cook_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

    def test_years_of_experience_in_detail_view(self):
        url = reverse("admin:kitchen_cook_change", args=[self.cook.id])
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)
        self.assertContains(response, self.cook.first_name)
        self.assertContains(response, self.cook.last_name)

    def test_add_cook_page_contains_years_of_experience(self):
        url = reverse("admin:kitchen_cook_add")
        response = self.client.get(url)

        self.assertContains(response, "years_of_experience")

    def test_regular_user_cannot_access_admin(self):
        self.client.logout()
        self.client.force_login(self.cook)
        url = reverse("admin:kitchen_cook_changelist")
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)
