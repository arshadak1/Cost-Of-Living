

from django import forms

from django.forms import ModelForm

from .models import Data, Review


class DateInput(forms.DateInput):
    input_type = 'date'




class DataForm(ModelForm):
    class Meta:
        model = Data
        fields = ['title', 'is_expense', 'value', 'per', 'Date']

        widgets = {
            'Date': DateInput(),
        }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['review_text_box']