# yourapp/urls.py

from django.urls import path
from . import views
from .views import user_home,our_class, teachers
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'tracker'

urlpatterns = [

    path('admin_login', LoginView.as_view(template_name='admin_login.html'),name='admin_login'),
    path('afteradminlogin', views.afteradminlogin,name='afteradminlogin'),
    
  

    path('user_home/', views.user_home, name='user_home'),
    path('logout/', LogoutView.as_view(next_page='teacher:signin'), name='logout'),
    path('our_class/', our_class, name='our_class'),

    path('teachers/', teachers, name='teachers'),
    # path('add_students_from_excel/<int:class_id>/', views.add_students_from_excel, name='add_students_from_excel'),


    # path('class_list/', views.class_list, name='class_list'),

    # Add more URLs for other views
]
