from rest_framework import serializers
from .models import (
    Category,
    Attribute,
    Value,
    Condition,
    Answer
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = '__all__'


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

    def to_representation(self, instance):
        category = instance.category
        conditions = instance.conditions.all()
        conditions_list = []
        for condition in conditions:
            attribute = Condition.objects.get(id=condition.pk).attribute
            value = Condition.objects.get(id=condition.pk).value
            conditions_list.append({
                "attribute": attribute.name,
                "value": value.name,
                "category": category.name
            })
        return {'answer': conditions_list}



        # return super().to_representation(instance)

# Path: app\urls.py