from django.urls import path
from .views import my_cargos, mark_as_delivered

urlpatterns = [
    path('my-cargos/', my_cargos),
    path('deliver/', mark_as_delivered),
]