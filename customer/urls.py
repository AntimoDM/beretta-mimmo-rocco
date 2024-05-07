from django.urls import path, include
from .views import (
    CustomerListApiView,
    CustomerDetailApiView,
    ClienteDettaglioApiView,
    ClienteListApiView,
    InterventoListApiView,
    InterventoDettaglioApiView,
    TecnicoCaldaiaListApiView,
    NumeroDiTelefonoAggiuntivoListApiView
)

urlpatterns = [
    path('', CustomerListApiView.as_view()),
    path('<int:customer_id>', CustomerDetailApiView.as_view()),
    path('cliente', ClienteListApiView.as_view()),
    path('cliente/<str:numero_di_telefono>', ClienteDettaglioApiView.as_view()),
    path('intervento', InterventoListApiView.as_view()),
    path('intervento/<int:_id>', InterventoDettaglioApiView.as_view()),
    path('tecnico', TecnicoCaldaiaListApiView.as_view()),
    path('numeroAggiuntivo', NumeroDiTelefonoAggiuntivoListApiView.as_view()),
]