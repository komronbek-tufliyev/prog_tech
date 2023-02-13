from django.contrib import admin
from .models import (
    Category,
    Attribute,
    Value,
    Condition,
    Answer,
)
# Register your models here.

    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created')
    list_filter = ('date_created',)

class AttributeAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
    list_filter = ('category',)

class ValueAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
    list_filter = ('category',)
    
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('category', 'attribute', 'value')
    list_filter = ('category',)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', )
    list_filter = ('category',)

admin.site.register(Condition, ConditionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Value, ValueAdmin)

