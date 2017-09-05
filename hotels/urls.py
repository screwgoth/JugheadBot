from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^api/v1/hotels/$',
        views.get_hotel_info,
        name='get_hotel_info'
    ),
]
