from django import forms
from django.forms import inlineformset_factory
from django.forms import BaseModelFormSet
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget

from .models import Question, Answer, Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["name", "text"]
        widgets = {
            "name": forms.Textarea(),
            "text": CKEditorWidget()
        }

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

class BaseAnswerFormSet(BaseModelFormSet):
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