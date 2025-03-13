from django.urls import path


from kitchen.views import index, DishTypesListView

urlpatterns = [
    path("", index, name="index"),
    path("dish-types/", DishTypesListView.as_view(), name="dish-type-list")
]

app_name = "kitchen"
