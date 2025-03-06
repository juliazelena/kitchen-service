from django.contrib.auth.models import AbstractUser
from django.db import models

from kitchen_service import settings


class DishType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        related_name="dishes",
    )
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dishes"
    )


    def __str__(self):
        return f"{self.dish_type.name} {self.name}, price: {self.price}"


class Cook(AbstractUser):
    years_of_experience = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["years_of_experience"]
        unique_together = ("username", "years_of_experience")
        verbose_name = "cook"
        verbose_name_plural = "cooks"
