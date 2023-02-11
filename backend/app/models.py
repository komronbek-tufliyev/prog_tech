from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Created"))


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Value(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"))
    name = models.CharField(max_length=255, verbose_name=_("Value"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Value")
        verbose_name_plural = _("Values")

class Attribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"))
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Attribute")
        verbose_name_plural = _("Attributes")

class Answer(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name=_("Attribute"))
    value = models.ForeignKey(Value, on_delete=models.CASCADE, verbose_name=_("Value"))

    def __str__(self):
        return f"{self.attribute.name} - {self.value.name}"

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def check_answer(self, attribute_id, value_id):
        if self.attribute.id == attribute_id and self.value.id == value_id:
            return True
        return False
    
    def get_answer(self):
        return {
            "attribute_id": self.attribute.id,
            "value_id": self.value.id
        }
