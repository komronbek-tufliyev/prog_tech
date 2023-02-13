from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"), unique=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Created"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Value(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"))
    name = models.CharField(max_length=255, verbose_name=_("Value"), unique=True)
    date_created = models.DateTimeField(verbose_name=_("Date Created"), default=timezone.now)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Value")
        verbose_name_plural = _("Values")

class Attribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"))
    name = models.CharField(max_length=255, verbose_name=_("Name"), unique=True)
    date_created = models.DateTimeField(verbose_name=_("Date Created"), default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Attribute")
        verbose_name_plural = _("Attributes")

class Condition(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"), default=1)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name=_("Attribute"))
    value = models.ForeignKey(Value, on_delete=models.CASCADE, verbose_name=_("Value"))
    date_created = models.DateTimeField(verbose_name=_("Date Created"), default=timezone.now)

    def __str__(self):
        return f"{self.attribute.name} - {self.value.name}"

    class Meta:
        verbose_name = _("Condition")
        verbose_name_plural = _("Conditions")
    
    def get_condition(self):
        return {
            "attribute_id": self.attribute.id,
            "value_id": self.value.id
        }

class Answer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"), default=1)
    conditions = models.ManyToManyField(Condition, verbose_name=_("Conditions"))
    name = models.CharField(max_length=255, verbose_name=_("Name"), default="Answer")
    date_created = models.DateTimeField(verbose_name=_("Date Created"), default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def get_conditions(self):
        return [condition.get_condition() for condition in self.conditions.all()]

    def get_answer(self):
        return {
            "id": self.id,
            "name": self.name,
            "conditions": self.get_conditions()
        }


