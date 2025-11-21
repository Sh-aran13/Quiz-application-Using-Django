from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)
    
    # Student-specific fields
    roll_number = models.CharField(max_length=20, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"


# Quiz Model
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_limit = models.IntegerField(help_text="Time limit in minutes", default=30)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


# Question Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    marks = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"


# Quiz Attempt Model
class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    question_order = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('student', 'quiz')
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"
    
    def percentage(self):
        if self.total_marks > 0:
            return round((self.score / self.total_marks) * 100, 2)
        return 0


# Student Answer Model
class StudentAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ], null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('attempt', 'question')
    
    def __str__(self):
        return f"{self.attempt.student.username} - {self.question.question_text[:50]}"

