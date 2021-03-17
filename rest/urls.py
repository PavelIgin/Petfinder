"""petfinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from rest.views import AnimalAdvertisementView, AnimalNewsView, \
    AnimalAdvertisementTypeView, AnimalAdvertisementColorView, \
    FavoritAnimal, CommentAnimal, CommentObjectView, CommentEditView

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router = DefaultRouter()
router.register('advertisement', AnimalAdvertisementView, basename='advertisement')
router.register('comment_object', CommentObjectView, basename='comment_object')

urlpatterns = [
    path('news/', AnimalNewsView.as_view(), name='news'),
    path('advertisement/type/', AnimalAdvertisementTypeView.as_view(), name='advertisement_type'),
    path('advertisement/color/', AnimalAdvertisementColorView.as_view(), name='advertisement_color'),
    path('favorit/', FavoritAnimal.as_view(), name='advertisement_favorit'),
    path('token/', views.obtain_auth_token, name='token'),
    path('comment/<pk>', CommentAnimal.as_view(), name='comment'),
    path('comment_edit/', CommentEditView.as_view({'patch': 'partial_update', 'delete': 'destroy'}), name='comment_edit')]+router.urls
