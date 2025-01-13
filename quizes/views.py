from django.shortcuts import render, redirect
from .forms import QuestionForm, AnswerFormSet
from .models import Quiz

def create_question(request, quiz_id):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        answer_formset = AnswerFormSet(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = Quiz.objects.get(id=quiz_id)
            question.save()
            answer_formset.clean()
            for form in answer_formset:
                if form.cleaned_data:
                    print(form.cleaned_data)
                    answer = form.save(commit=False)
                    answer.question = question
                    answer.save()
            return redirect('/', quiz_id=quiz_id)
    else:
        question_form = QuestionForm()
        answer_formset = AnswerFormSet()
    return render(request, 'create_question.html', {
        'question_form': question_form,
        'answer_formset': answer_formset,
    })