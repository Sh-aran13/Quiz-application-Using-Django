from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-quiz/', views.add_quiz, name='add_quiz'),
    path('add-questions/<int:quiz_id>/', views.add_questions, name='add_questions'),
    path('edit-question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete-question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('toggle-quiz-status/<int:quiz_id>/', views.toggle_quiz_status, name='toggle_quiz_status'),
    path('delete-quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('view-results/', views.view_results, name='view_results'),
    path('export-results-excel/<int:quiz_id>/', views.export_results_excel, name='export_results_excel'),
    path('export-results-pdf/<int:quiz_id>/', views.export_results_pdf, name='export_results_pdf'),
    
    # Student URLs
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('take-quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('submit-quiz/<int:attempt_id>/', views.submit_quiz, name='submit_quiz'),
    path('quiz-result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
]
