from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Dish, Cook, Ingredient

User = get_user_model()


class DishTypeModelTest(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(name="Pizza")
        self.assertEqual(str(dish_type), "Pizza")


class IngredientModelTest(TestCase):
    def test_ingredient_str(self):
        ingredient = Ingredient.objects.create(name="Tomato")
        self.assertEqual(str(ingredient), "Tomato")


class DishModelTest(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Pasta")
        self.ingredient1 = Ingredient.objects.create(name="Tomato")
        self.ingredient2 = Ingredient.objects.create(name="Cheese")

        self.dish = Dish.objects.create(
            name="Carbonara",
            description="Delicious Italian pasta",
            price=12.99,
            dish_type=self.dish_type
        )
        self.dish.ingredients.add(self.ingredient1, self.ingredient2)

    def test_dish_str(self):
        self.assertEqual(str(self.dish), "Pasta Carbonara, price: 12.99")

    def test_dish_has_ingredients(self):
        self.assertEqual(self.dish.ingredients.count(), 2)

    def test_dish_get_absolute_url(self):
        expected_url = reverse(
            "kitchen:dish-detail",
            kwargs={"pk": self.dish.pk}
        )
        self.assertEqual(self.dish.get_absolute_url(), expected_url)


class CookModelTest(TestCase):
    def setUp(self):
        self.cook = User.objects.create_user(
            username="chef_john",
            password="testpassword",
            years_of_experience=5
        )

    def test_cook_str(self):
        self.assertEqual(str(self.cook), "chef_john")

    def test_cook_has_years_of_experience(self):
        self.assertEqual(self.cook.years_of_experience, 5)

    def test_get_absolute_url(self):
        expected_url = reverse(
            "kitchen:cook-detail",
            kwargs={"pk": self.cook.pk}
        )
        self.assertEqual(self.cook.get_absolute_url(), expected_url)

    def test_cook_ordering(self):
        Cook.objects.create(username="cook1", years_of_experience=3)
        Cook.objects.create(username="cook2", years_of_experience=1)
        Cook.objects.create(username="cook3", years_of_experience=5)

        expected_order = ["cook2", "cook1", "chef_john", "cook3"]
        actual_order = list(Cook.objects.values_list("username", flat=True))
        self.assertEqual(actual_order, expected_order)
