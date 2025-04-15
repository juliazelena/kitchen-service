from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from kitchen_service import settings


class DishType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(
        default="https://kitchen-media.s3.eu-central-1.amazonaws.com/images/default_dish.png",
        upload_to="https://kitchen-media.s3.eu-central-1.amazonaws.com/images/",
        null=True,
        blank=True
    )
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        related_name="dishes",
    )
    cooks = models.ManyToManyField(
        settings.base.AUTH_USER_MODEL,
        related_name="dishes"
    )
    ingredients = models.ManyToManyField("Ingredient", related_name="dishes")

    def get_absolute_url(self):
        return reverse("kitchen:dish-detail", kwargs={"pk": self.pk})


    def __str__(self):
        return f"{self.dish_type.name} {self.name}, price: {self.price}"


class Cook(AbstractUser):
    years_of_experience = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(
        default="https://kitchen-media.s3.eu-central-1.amazonaws.com/images/cook.png",
        upload_to="https://kitchen-media.s3.eu-central-1.amazonaws.com/images/",
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["years_of_experience"]
        unique_together = ("username", "years_of_experience")
        verbose_name = "cook"
        verbose_name_plural = "cooks"

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
