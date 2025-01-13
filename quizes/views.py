from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

def index(request):
    return render(request, "quizes/index.html")

def preview_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'quizes/preview_quiz.html', {
        'quiz': quiz,
        'questions': questions
    })

@login_required(login_url="users:login")
def quiz_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = get_object_or_404(Question, pk=question_id, quiz=quiz)

    if request.method == 'POST':
        answer_id = request.POST.get('answer')
        selected_answer = get_object_or_404(Answer, pk=answer_id)
        results, created = Results.objects.get_or_create(user=request.user, quiz=quiz)
        if 'answers' not in results.data:
            results.data['answers'] = []

        results.data['answers'].append({
            'question': question.text,
            'answer': selected_answer.text,
            'is_correct': selected_answer.isCorrect
        })
        results.save()
        next_question = quiz.questions.filter(id__gt=question.id).first()

        if next_question:
            return redirect('quiz_question', quiz_id=quiz.id, question_id=next_question.id)
        else:
            return redirect('quiz_results', quiz_id=quiz.id)

    answers = question.answers.all()
    return render(request, 'quizes/quiz_question.html', {
        'quiz': quiz,
        'question': question,
        'answers': answers
    })

@login_required(login_url="users:login")
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    results = get_object_or_404(Results, user=request.user, quiz=quiz)
    answers_data = results.data.get('answers', [])

    return render(request, 'quizes/quiz_results.html', {
        'quiz': quiz,
        'answers_data': answers_data
    })

@login_required(login_url="users:login")
def create_question(request, quiz_id):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        answer_formset = AnswerFormSet(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = Quiz.objects.get(visibleId=quiz_id)
            question.save()
            answer_formset.clean()
            for form in answer_formset:
                if form.cleaned_data:
                    print(form.cleaned_data)
                    answer = form.save(commit=False)
                    answer.question = question
                    answer.save()
            return redirect('/preview', quiz_id=quiz_id)
    else:
        quiz = get_object_or_404(Quiz, visibleId=quiz_id)
        question_form = QuestionForm()
        answer_formset = AnswerFormSet()
    return render(request, 'quizes/create_question.html', {
        'question_form': question_form,
        'answer_formset': answer_formset,
    })

@login_required(login_url="users:login")
def edit_question(request, quiz_id, question_id):
    question = get_object_or_404(Question, visibleId=question_id, quiz__visibleId=quiz_id)
    answers = Answer.objects.filter(question=question)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question)
        answer_formset = AnswerFormSet(request.POST)
        
        if question_form.is_valid() and answer_formset.is_valid():
            question = question_form.save()
            
            for form in answer_formset:
                if form.cleaned_data.get('DELETE'):
                    form.instance.delete()
            
            for form in answer_formset:
                if form.cleaned_data:
                    answer = form.save(commit=False)
                    answer.question = question
                    answer.save()
            
            return redirect('/preview', quiz_id=quiz_id)
    
    else:
        question_form = QuestionForm(instance=question)
        answer_formset = AnswerFormSet(queryset=Answer.objects.filter(question=question))
    
    return render(request, 'quizes/edit_question.html', {
        'question_form': question_form,
        'answer_formset': answer_formset,
        'quiz_id': quiz_id,
        'question_id': question_id,
    })

@login_required(login_url="users:login")
def delete_question(request, quiz_id, question_id):
    question = get_object_or_404(Question, visibleId=question_id)
    if request.method == 'POST':
        if request.user == question.quiz.author:
            question.delete()
            return redirect('/')
    return render(request, 'materials/delete_material.html', {'question_form': question})

@login_required(login_url="users:login")
def create_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('material_list')
    else:
        form = MaterialForm()
    return render(request, 'materials/create_material.html', {'form': form})

@login_required(login_url="users:login")
def edit_material(request, mat_id):
    material = get_object_or_404(Material, visibleId=mat_id)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('material_list')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'materials/edit_material.html', {'form': form, 'material': material})

@login_required(login_url="users:login")
def delete_material(request, mat_id):
    material = get_object_or_404(Material, visibleId=mat_id)
    if request.method == 'POST':
        if request.user == material.quiz.author:
            material.delete()
            return redirect('/')
    return render(request, 'materials/delete_material.html', {'material': material})

def topic_search(request, topic_id):
    if request.method == "POST":
        topic = Topic.objects.get(visibleId=topic_id)
        if topic:
            quizes = Quiz.objects.filter(topic=topic)
        else:
            quizes = Quiz.objects.all()
    else:
        quizes = Quiz.objects.all()
    return render(request, "quizes/search.html", {"quizes": quizes})

def materials_list(request, topic_id):
    if request.method == "POST":
        topic = Topic.objects.filter(visibleId=topic_id)
        if topic:
            quizes = Quiz.objects
            materials = Material.objects.filter(quiz__topic=topic)
        else:
            materials = Material.objects.all()
    else:
        quizes = Quiz.objects.all()
    return render(request, "quizes/search.html", {"materials": materials})