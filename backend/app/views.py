from django.shortcuts import render
from rest_framework import viewsets
from .models import (
    Category,
    Attribute,
    Value,
    Answer,
    Condition
)
from .serializers import (
    CategorySerializer,
    AttributeSerializer,
    ValueSerializer,
    AnswerSerializer,
    ConditionSerializer
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

    # @action(detail=True, methods=['get'])
    # def attributes(self, request, pk=None):
    #     category = self.get_object()
    #     attributes = Attribute.objects.filter(category=category)
    #     serializer = AttributeSerializer(attributes, many=True)
    #     return Response(serializer.data)
    
    # @action(detail=True, methods=['get'])
    # def values(self, request, pk=None):
    #     category = self.get_object()
    #     values = Value.objects.filter(category=category)
    #     serializer = ValueSerializer(values, many=True)
    #     return Response(serializer.data)
    
    # @action(detail=True, methods=['get'])
    # def answers(self, request, pk=None):
    #     category = self.get_object()
    #     attributes = Attribute.objects.filter(category=category)
    #     values = Value.objects.filter(category=category)
    #     answers = []
    #     for attribute in attributes:
    #         for value in values:
    #             answers.append({
    #                 "attribute_id": attribute.id,
    #                 "value_id": value.id
    #             })
    #     return Response(answers)
    
    # @action(detail=True, methods=['get'])
    # def search(self, request, pk=None):
    #     category = self.get_object()
    #     attributes = Attribute.objects.filter(category=category)
    #     values = Value.objects.filter(category=category)
    #     answers = []
    #     for attribute in attributes:
    #         for value in values:
    #             answers.append({
    #                 "attribute_id": attribute.id,
    #                 "value_id": value.id
    #             })
    #     return Response(answers)
    
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


    def create(self, request, *args, **kwargs):
        try:
            try:
                print("request.data: ", request.data)
                category_name = request.data.get('category', None)
                if category_name is None:
                    print("category_name is None")
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "category_name is None"})
                category = Category.objects.filter(name=category_name).first()
                if category is None:
                    print("category is None")
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "category is None"})
                print("category obj: ", category)
                print("category: ", category)
                attribute = Attribute.objects.create(name=request.data.get('name'), category=category)
                # serializer = self.get_serializer(data=request.data)
                # if serializer.is_valid(raise_exception=True):
                #     print("serializer is valid")
                # else:
                #     print("serializer is not valid")
                # serializer.save(category=category)
                # headers = self.get_success_headers(serializer.data)
                content = {
                    'message': 'Attribute created successfully',
                    'attribute': attribute.name,
                }
                print("content: ", content)
                return Response(status=status.HTTP_201_CREATED, data=content)
            except Exception as e:
                print("Exception1: ", e)
                return super().create(request, *args, **kwargs)
        except Exception as e:
            print("Exception2: ", e)
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "category_name is None"})
    
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

    def create(self, request, *args, **kwargs):
        try:
            try:
                category_name = request.data.get('category', None)
                if category_name is None:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                category = Category.objects.get(name=category_name)

                value_obj = Value.objects.create(name=request.data.get('name'), category=category)
                content = {
                    'message': 'Value created successfully',
                    'value': value_obj.name,
                }
                return Response(status=status.HTTP_201_CREATED, data=content)
                # serializer = self.get_serializer(data=request.data)
                # serializer.is_valid(raise_exception=True)
                # serializer.save(category=category)
                # headers = self.get_success_headers(serializer.data)
                # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except Exception as e:
                print("Exception: ", e)
                return super().create(request, *args, **kwargs)
        except Exception as e:
            print("Exception: ", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Condition.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            conditions = request.data
            print("data: ", conditions)
            condition_ids = []
            category = conditions[0].get('category', Category.objects.first().name)
            category = Category.objects.get(name=category)
            print("category: ", category)
            if category is None:
                category = Category.objects.first()
                print("category is None")
            for condition in conditions:
                print("condition: ", condition)
                attribute_name = condition.get('attribute', None)
                value_name = condition.get('value', None)
                if attribute_name is None or value_name is None or category is None:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "attribute_name or value_name is None"})
                attribute = Attribute.objects.get(name=attribute_name)
                value = Value.objects.get(name=value_name)
                
                condition_ids.append(Condition.objects.create(attribute=attribute, value=value, category=category).pk)
            answer = Answer.objects.filter(category=category)
            if answer.exists():
                answer = answer.first()
            else:
                answer = Answer.objects.create(category=category)
            answer.conditions.set(condition_ids)
            content = {
                'message': 'Condition created successfully',
            }
            return Response(status=status.HTTP_201_CREATED, data=content)
        except Exception as e:
            print("Exception: ", e)
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "attribute_name or value_name is None"})



class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Answer.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
       
    def create(self, request, *args, **kwargs):
        try:
            try:
                category_name = request.data.get('category', None)
                if category_name is None:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                category = Category.objects.get(name=category_name)

                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(category=category)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except Exception as e:
                print("Exception: ", e)
                return super().create(request, *args, **kwargs)
        except Exception as e:
            print("Exception: ", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CheckAnswerView(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get(self, request, format=None):
        category_id = request.query_params.get('category_id', None)
        if category_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "category_id is required"})
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "category not found"})
        conditions = request.query_params.getlist('conditions', None)
        if conditions is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "conditions is required"})
        condition_objs = Condition.objects.filter(id__in=conditions)
        if condition_objs.count() != len(conditions):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "condition not found"})

        answers = Answer.objects.filter(conditions__in=condition_objs).distinct()
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        category = self.request.query_params.get('category', None)

        if category is not None:
            category = Category.objects.filter(name=category).first()
            if category is not None:
                answers = Answer.objects.filter(category=category)



class CheckAnswerAPIView(APIView):

    def post(self, request, format=None):
        category = request.data.get('category', None)
        condition_ids = []
        if category is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "category is required"})
        try:
            category = Category.objects.get(name=category)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "category not found"})
        conditions = request.data.get('conditions', None)
        if conditions is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "conditions is required"})
        for condition in conditions:
            attribute = condition.get('attribute', None)
            value = condition.get('value', None)
            if attribute is None or value is None:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "attribute or value is required"})
            try:
                attribute = Attribute.objects.get(name=attribute)
            except Attribute.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "attribute not found"})
            try:
                value = Value.objects.get(name=value)
            except Value.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "value not found"})
            condition_object = Condition.objects.filter(attribute=attribute, value=value, category=category).first()
            if condition_object is None:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "condition not found"})
            condition_ids.append(condition_object.id)
        answers = Answer.objects.filter(conditions__in=condition_ids).distinct()
        serializer = AnswerSerializer(answers, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


        # answers = Answer.objects.filter(conditions__in=condition_objs).distinct()
        # serializer = AnswerSerializer(answers, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)





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

