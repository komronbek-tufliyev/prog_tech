from django.urls import path, include
from rest_framework import routers
from .views import (
    CategoryViewSet,
    AttributeViewSet,
    ValueViewSet,
    AnswerViewSet,
    CheckAnswerView,
    ConditionViewSet,
    SearchView,
    CheckAnswerAPIView
)

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'conditions', ConditionViewSet, basename='condition')
router.register(r'attributes', AttributeViewSet, basename='attribute')
router.register(r'values', ValueViewSet, basename='value')
router.register(r'answers', AnswerViewSet, basename='answer')

urlpatterns = [
    path('', include(router.urls)),
    # path('check-answer/', CheckAnswerView.as_view(), name='check-answer'),
    path('check-answer/', CheckAnswerAPIView.as_view(), name='check-answer'),
    path('search/', SearchView.as_view(), name='search'),
]

