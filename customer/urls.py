from django.urls import path, include
from .views import (
    CustomerListApiView,
    CustomerDetailApiView
)

urlpatterns = [
    path('', CustomerListApiView.as_view()),
    path('<int:customer_id>', CustomerDetailApiView.as_view()),
]