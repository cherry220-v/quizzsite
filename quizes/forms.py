from django import forms
from django.forms import inlineformset_factory
from django.forms import BaseFormSet
from django.core.exceptions import ValidationError

from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz', 'text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'isCorrect', 'image']

class BaseAnswerFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

AnswerFormSet = inlineformset_factory(
    Question,
    Answer,
    form=AnswerForm,
    formset=BaseAnswerFormSet,
    extra=2,
    can_delete=False,
)