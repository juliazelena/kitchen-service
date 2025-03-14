from django.urls import path


from kitchen.views import index, DishTypeListView, DessertTypeCreateView

urlpatterns = [
    path("", index, name="index"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish-types/create/", DessertTypeCreateView.as_view(),
        name="dessert-type-create",
    ),
]

app_name = "kitchen"
