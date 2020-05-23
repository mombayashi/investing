from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('usage', views.index, name='index'),
    path('prediction', views.prediction, name='prediction'),
    path('historical', views.historical, name='historical'),
    path('contact', views.contact, name='contact'),
    # path('bstest', views.bstest, name='bstest'),
]
