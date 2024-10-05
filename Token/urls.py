
from django.urls import path
from .views import BookAppointmentView

urlpatterns = [
    path('get-token/', BookAppointmentView.as_view(), name='get-token'),

]