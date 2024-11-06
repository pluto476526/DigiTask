from django.forms import ModelForm
from dash.models import Category


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'