from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Quiz, Question, QuizAttempt, StudentAnswer


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'phone', 'roll_number', 'branch']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'phone', 'roll_number']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'roll_number', 'branch')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'roll_number', 'branch')}),
    )


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'time_limit', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_text', 'correct_answer', 'marks', 'order']
    list_filter = ['quiz', 'correct_answer']
    search_fields = ['question_text']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'score', 'total_marks', 'is_completed', 'started_at']
    list_filter = ['is_completed', 'quiz', 'started_at']
    search_fields = ['student__username', 'quiz__title']
    date_hierarchy = 'started_at'


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selected_answer', 'is_correct']
    list_filter = ['is_correct', 'selected_answer']
    search_fields = ['attempt__student__username', 'question__question_text']
