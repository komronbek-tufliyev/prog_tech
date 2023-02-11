from django.urls import path, include
from rest_framework import routers
from .views import (
    CategoryViewSet,
    AttributeViewSet,
    ValueViewSet,
    CheckAnswerView,
    SearchView
)

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'attributes', AttributeViewSet, basename='attribute')
router.register(r'values', ValueViewSet, basename='value')

urlpatterns = [
    path('', include(router.urls)),
    path('check-answer/', CheckAnswerView.as_view(), name='check-answer'),
    path('search/', SearchView.as_view(), name='search'),
]

