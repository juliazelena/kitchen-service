from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType

DishType_URL = reverse("kitchen:dish-type-list")


class PublicDishTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DishType_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTypeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.DishType = DishType.objects.create(
            name="salad test",
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_types(self):
        DishType.objects.create(name="soup test2",)
        response = self.client.get(DishType_URL)
        self.assertEqual(response.status_code, 200)
        dish_types = DishType.objects.all()
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_types),
        )
        self.assertTemplateUsed(
            response,
            "kitchen/dish_type_list.html"
        )

    def test_create_dish_type(self):
        form_data = {
            "name": "dessert test1",
        }
        self.client.post(reverse("kitchen:dish-type-create"), data=form_data)
        new_dish_type = DishType.objects.get(name=form_data["name"])
        self.assertEqual(new_dish_type.name, form_data["name"])

    def test_update_dish_type(self):
        update_url = reverse(
            "kitchen:dish-type-update",
            args=[self.DishType.id]
        )
        updated_data = {"name": "Italian food"}
        response = self.client.post(update_url, data=updated_data)
        self.assertRedirects(response, reverse("kitchen:dish-type-list"))
        self.DishType.refresh_from_db()
        self.assertEqual(self.DishType.name, updated_data["name"])

    def test_delete_DishType(self):
        delete_url = reverse(
            "kitchen:dish-type-delete",
            args=[self.DishType.id]
        )
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse("kitchen:dish-type-list"))
        self.assertFalse(
            DishType.objects.filter(id=self.DishType.id).exists()
        )
