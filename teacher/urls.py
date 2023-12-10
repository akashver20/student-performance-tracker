from django.urls import path
from . import views
# from teacher.views import user_home, signup, signin,  our_class, teachers,teacher_home
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'tracker'

urlpatterns = [
    path('', views.signin, name='signin'), 

    path('teacher_home',views.teacher_home, name="teacher_home"),
    path('signin/',views.signin, name='signin'),
    path('logout/', LogoutView.as_view(next_page='teacher:signin'), name='logout'),
    path('add_teacher',views.add_teacher, name="add_teacher"),
    path('delete_teacher',views.delete_teacher, name="delete_teacher"),
    path('teacher_students/<int:class_id>/', views.teacher_students, name='teacher_students'),
    path('teacher_students/<int:class_id>/', views.teacher_students, name='teacher_students'),
    # path('view_student_details/<int:class_id>/<str:student_name>/', views.view_student_details, name='view_student_details'),
    path('teacher_view_student_details/<int:class_id>/<str:student_name>/', views.teacher_prediction, name='teacher_view_student_details'),
    path('teacher_report_generation/<int:class_id>/', views.teacher_report_generation, name='teacher_report_generation'),


]