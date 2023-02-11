from django.shortcuts import render
from rest_framework import viewsets
from .models import (
    Category,
    Attribute,
    Value,
    Answer
)
from .serializers import (
    CategorySerializer,
    AttributeSerializer,
    ValueSerializer
)
from rest_framework import permissions
from rest_framework import generics
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
#  for searching
from django.db.models import Q, F
from django.db.models.functions import Concat

from rest_framework.views import APIView

# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def attributes(self, request, pk=None):
        category = self.get_object()
        attributes = Attribute.objects.filter(category=category)
        serializer = AttributeSerializer(attributes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def values(self, request, pk=None):
        category = self.get_object()
        values = Value.objects.filter(category=category)
        serializer = ValueSerializer(values, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def answers(self, request, pk=None):
        category = self.get_object()
        attributes = Attribute.objects.filter(category=category)
        values = Value.objects.filter(category=category)
        answers = []
        for attribute in attributes:
            for value in values:
                answers.append({
                    "attribute_id": attribute.id,
                    "value_id": value.id
                })
        return Response(answers)
    
    @action(detail=True, methods=['get'])
    def search(self, request, pk=None):
        category = self.get_object()
        attributes = Attribute.objects.filter(category=category)
        values = Value.objects.filter(category=category)
        answers = []
        for attribute in attributes:
            for value in values:
                answers.append({
                    "attribute_id": attribute.id,
                    "value_id": value.id
                })
        return Response(answers)
    
    def get_queryset(self):
        queryset = Category.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
    
class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Attribute.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
    
class ValueViewSet(viewsets.ModelViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Value.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class CheckAnswerView(APIView):
    def post(self, request, format=None):
        attribute_id = request.data.get('attribute_id', None)
        value_id = request.data.get('value_id', None)
        if attribute_id is None or value_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "attribute_id and value_id are required"})
        try:
            answer = Answer.objects.get(attribute_id=attribute_id, value_id=value_id)
            return Response(status=status.HTTP_200_OK, data={"answer": answer.answer})
        except Answer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "answer not found"})
        
class SearchView(APIView):
    def post(self, request, format=None):
        category_id = request.data.get('category_id', None)
        if category_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "category_id is required"})
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "category not found"})
        attributes = Attribute.objects.filter(category=category)
        values = Value.objects.filter(category=category)
        answers = []
        for attribute in attributes:
            for value in values:
                answers.append({
                    "attribute_id": attribute.id,
                    "value_id": value.id
                })
        return Response(answers)