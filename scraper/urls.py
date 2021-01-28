from django.urls import path
from .views import index, ResultsList, success

urlpatterns = [
    path('',index, name='index'),
    path('results/', ResultsList.as_view(), name='results'),
    path('success/', success, name='success')
]