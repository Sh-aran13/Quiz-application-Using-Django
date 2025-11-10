from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Count, Avg, Q
from .models import User, Quiz, Question, QuizAttempt, StudentAnswer
from .forms import StudentRegistrationForm, AdminRegistrationForm, LoginForm, QuizForm, QuestionForm
import random
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO


def generate_captcha(request):
    """Generate a random 6-digit captcha"""
    captcha = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    request.session['captcha'] = captcha
    return captcha


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        role = request.POST.get('role')
        
        # Only allow admin registration for superusers
        if role == 'admin':
            messages.error(request, 'Admin registration is restricted. Please contact the system administrator.')
            return render(request, 'quiz/auth.html', {'show_register': True})
        
        if role == 'student':
            form = StudentRegistrationForm(request.POST)
        else:
            messages.error(request, 'Invalid role selected. Please choose Student or Admin.')
            return render(request, 'quiz/auth.html', {'show_register': True})
        
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Registration successful! Welcome {user.username}. Please login to continue.')
            return render(request, 'quiz/auth.html', {'show_register': False})
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f'{field}: {error}')
            messages.error(request, 'Registration failed. ' + ' '.join(error_messages))
            return render(request, 'quiz/auth.html', {'show_register': True})
    else:
        form = None
    
    return render(request, 'quiz/auth.html', {'show_register': True})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}! Login successful.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Login failed. Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Login failed. Please fill in all required fields.')
    else:
        form = LoginForm()
    
    return render(request, 'quiz/auth.html', {'show_register': False})


@login_required
def logout_view(request):
    username = request.user.username
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('student_dashboard')


@login_required
def admin_dashboard(request):
    # Only allow superusers to access admin dashboard
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin dashboard is only accessible to superusers.')
        return redirect('student_dashboard')
    
    if request.user.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('student_dashboard')
    
    # Show all quizzes for admin users, not just their own
    quizzes = Quiz.objects.all().annotate(
        attempt_count=Count('attempts')
    )
    
    active_quizzes_count = quizzes.filter(is_active=True).count()
    
    context = {
        'quizzes': quizzes,
        'total_quizzes': quizzes.count(),
        'total_attempts': QuizAttempt.objects.count(),
        'active_quizzes_count': active_quizzes_count,
    }
    
    return render(request, 'quiz/admin_dashboard.html', context)


@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        messages.error(request, 'Access denied')
        return redirect('admin_dashboard')
    
    # Get all active quizzes
    all_quizzes = Quiz.objects.filter(is_active=True)
    
    # Get quizzes already attempted by the student
    attempted_quiz_ids = QuizAttempt.objects.filter(
        student=request.user, 
        is_completed=True
    ).values_list('quiz_id', flat=True)
    
    # Available quizzes (not attempted)
    available_quizzes = all_quizzes.exclude(id__in=attempted_quiz_ids)
    
    # Attempted quizzes with scores
    attempted_quizzes = QuizAttempt.objects.filter(
        student=request.user,
        is_completed=True
    ).select_related('quiz')
    
    context = {
        'available_quizzes': available_quizzes,
        'attempted_quizzes': attempted_quizzes,
    }
    
    return render(request, 'quiz/student_dashboard.html', context)


@login_required
def add_quiz(request):
    # Only allow superusers to access admin features
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin features are only accessible to superusers.')
        return redirect('student_dashboard')
    
    if request.user.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            messages.success(request, 'Quiz created successfully!')
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        form = QuizForm()
    
    return render(request, 'quiz/add_quiz.html', {'form': form})


@login_required
def add_questions(request, quiz_id):
    # Only allow superusers to access admin features
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin features are only accessible to superusers.')
        return redirect('student_dashboard')
    
    if request.user.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('student_dashboard')
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'Question added successfully!')
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        form = QuestionForm()
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'form': form,
    }
    
    return render(request, 'quiz/add_questions.html', context)


@login_required
def delete_question(request, question_id):
    # Only allow superusers to access admin features
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin features are only accessible to superusers.')
        return redirect('student_dashboard')
    
    if request.user.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('student_dashboard')
    
    question = get_object_or_404(Question, id=question_id)
    quiz_id = question.quiz.id
    question.delete()
    messages.success(request, 'Question deleted successfully!')
    return redirect('add_questions', quiz_id=quiz_id)


@login_required
def edit_question(request, question_id):
    # Only allow superusers to access admin features
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin features are only accessible to superusers.')
        return redirect('student_dashboard')
    
    if request.user.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('student_dashboard')
    
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated successfully!')
            return redirect('add_questions', quiz_id=question.quiz.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuestionForm(instance=question)
    
    return render(request, 'quiz/edit_question.html', {
        'form': form,
        'question': question
    })


@login_required
def toggle_quiz_status(request, quiz_id):
    # Only allow superusers to access admin features
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin features are only accessible to superusers.')
        return redirect('student_dashboard')
    
    if request.user.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('student_dashboard')
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.is_active = not quiz.is_active
    quiz.save()
    
    status = 'activated' if quiz.is_active else 'deactivated'
    messages.success(request, f'Quiz "{quiz.title}" has been {status} successfully!')
    return redirect('admin_dashboard')


@login_required
def delete_quiz(request, quiz_id):
    # Only allow superusers to access admin features
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin features are only accessible to superusers.')
        return redirect('student_dashboard')
    
    if request.user.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('student_dashboard')
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        quiz_title = quiz.title
        quiz.delete()
        messages.success(request, f'Quiz "{quiz_title}" has been deleted successfully!')
        return JsonResponse({'status': 'success', 'message': f'Quiz "{quiz_title}" has been deleted successfully!'})
    
    # For GET requests, return JSON response for AJAX modal
    return JsonResponse({'status': 'confirm', 'quiz_id': quiz_id, 'quiz_title': quiz.title})


@login_required
def view_results(request):
    # Only allow superusers to access admin features
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin features are only accessible to superusers.')
        return redirect('student_dashboard')
    
    if request.user.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('student_dashboard')
    
    quizzes = Quiz.objects.all()
    selected_quiz_id = request.GET.get('quiz_id')
    
    attempts = None
    selected_quiz = None
    
    if selected_quiz_id:
        selected_quiz = get_object_or_404(Quiz, id=selected_quiz_id)
        attempts = QuizAttempt.objects.filter(
            quiz=selected_quiz,
            is_completed=True
        ).select_related('student').order_by('student__roll_number')
    
    context = {
        'quizzes': quizzes,
        'selected_quiz': selected_quiz,
        'attempts': attempts,
    }
    
    return render(request, 'quiz/view_results.html', context)


@login_required
def export_results_excel(request, quiz_id):
    # Only allow superusers to access admin features
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin features are only accessible to superusers.')
        return redirect('student_dashboard')
    
    if request.user.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('student_dashboard')
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempts = QuizAttempt.objects.filter(
        quiz=quiz,
        is_completed=True
    ).select_related('student').order_by('-score')
    
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Quiz Results"
    
    # Header style
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    
    # Add title
    ws.merge_cells('A1:F1')
    ws['A1'] = f'Quiz Results: {quiz.title}'
    ws['A1'].font = Font(bold=True, size=14)
    ws['A1'].alignment = Alignment(horizontal='center')
    
    # Add headers
    headers = ['S.No', 'Student Name', 'Roll Number', 'Score', 'Total Marks', 'Percentage']
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_num)
        cell.value = header
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')
    
    # Add data
    for idx, attempt in enumerate(attempts, 1):
        ws.cell(row=idx+3, column=1, value=idx)
        ws.cell(row=idx+3, column=2, value=attempt.student.username)
        ws.cell(row=idx+3, column=3, value=attempt.student.roll_number or 'N/A')
        ws.cell(row=idx+3, column=4, value=attempt.score)
        ws.cell(row=idx+3, column=5, value=attempt.total_marks)
        ws.cell(row=idx+3, column=6, value=f"{attempt.percentage()}%")
    
    # Adjust column widths
    for col_idx in range(1, 7):  # 6 columns (A to F)
        max_length = 0
        column_letter = openpyxl.utils.get_column_letter(col_idx)
        for row in ws.iter_rows(min_col=col_idx, max_col=col_idx):
            for cell in row:
                try:
                    if cell.value and len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{quiz.title}_results.xlsx"'
    wb.save(response)
    
    return response


@login_required
def export_results_pdf(request, quiz_id):
    # Only allow superusers to access admin features
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin features are only accessible to superusers.')
        return redirect('student_dashboard')
    
    if request.user.role != 'admin':
        messages.error(request, 'Access denied')
        return redirect('student_dashboard')
    
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempts = QuizAttempt.objects.filter(
        quiz=quiz,
        is_completed=True
    ).select_related('student').order_by('-score')
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#366092'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    # Add title
    title = Paragraph(f"Quiz Results: {quiz.title}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Create table data
    data = [['S.No', 'Student Name', 'Roll Number', 'Score', 'Total', 'Percentage']]
    
    for idx, attempt in enumerate(attempts, 1):
        data.append([
            str(idx),
            attempt.student.username,
            attempt.student.roll_number or 'N/A',
            str(attempt.score),
            str(attempt.total_marks),
            f"{attempt.percentage()}%"
        ])
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    
    # Return response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{quiz.title}_results.pdf"'
    
    return response


@login_required
def take_quiz(request, quiz_id):
    if request.user.role != 'student':
        messages.error(request, 'Access denied')
        return redirect('admin_dashboard')
    
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    # Check if student has already attempted this quiz
    existing_attempt = QuizAttempt.objects.filter(student=request.user, quiz=quiz).first()
    if existing_attempt and existing_attempt.is_completed:
        messages.error(request, 'You have already attempted this quiz')
        return redirect('student_dashboard')
    
    # Create or get attempt
    if not existing_attempt:
        questions = Question.objects.filter(quiz=quiz)
        total_marks = sum([q.marks for q in questions])
        
        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            total_marks=total_marks
        )
    else:
        attempt = existing_attempt
    
    questions = Question.objects.filter(quiz=quiz).order_by('order', 'id')
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'attempt': attempt,
    }
    
    return render(request, 'quiz/take_quiz.html', context)


@login_required
def submit_quiz(request, attempt_id):
    if request.user.role != 'student':
        messages.error(request, 'Access denied')
        return redirect('admin_dashboard')
    
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    
    if attempt.is_completed:
        messages.error(request, 'This quiz has already been submitted')
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        questions = Question.objects.filter(quiz=attempt.quiz)
        score = 0
        
        for question in questions:
            answer_key = f'question_{question.id}'
            selected_answer = request.POST.get(answer_key)
            
            # Handle unanswered questions (when selected_answer is None or empty)
            if not selected_answer:
                selected_answer = None
            
            is_correct = False
            if selected_answer and selected_answer == question.correct_answer:
                is_correct = True
                score += question.marks
            
            StudentAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_answer=selected_answer,
                is_correct=is_correct
            )
        
        attempt.score = score
        attempt.is_completed = True
        attempt.completed_at = timezone.now()
        attempt.save()
        
        messages.success(request, f'Quiz submitted successfully! Your score: {score}/{attempt.total_marks}')
        return redirect('quiz_result', attempt_id=attempt.id)
    
    return redirect('take_quiz', quiz_id=attempt.quiz.id)


@login_required
def quiz_result(request, attempt_id):
    if request.user.role != 'student':
        messages.error(request, 'Access denied')
        return redirect('admin_dashboard')
    
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    
    if not attempt.is_completed:
        messages.error(request, 'Quiz not yet completed')
        return redirect('take_quiz', quiz_id=attempt.quiz.id)
    
    answers = StudentAnswer.objects.filter(attempt=attempt).select_related('question')
    
    # Calculate correct, wrong, and unanswered answers
    correct_count = answers.filter(is_correct=True).count()
    wrong_count = answers.filter(is_correct=False, selected_answer__isnull=False).count()
    unanswered_count = answers.filter(selected_answer__isnull=True).count()
    total_questions = answers.count()
    
    context = {
        'attempt': attempt,
        'answers': answers,
        'correct_count': correct_count,
        'wrong_count': wrong_count,
        'unanswered_count': unanswered_count,
        'total_questions': total_questions,
    }
    
    return render(request, 'quiz/quiz_result.html', context)


@login_required
def profile_view(request):
    return render(request, 'quiz/profile.html', {'user': request.user})
