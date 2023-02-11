from django.contrib import admin
from .models import (
    Category,
    Attribute,
    Value,
    Answer
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
    


admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Value, ValueAdmin)

