
app_name = 'classes'
from classes import views
from django.urls import path

urlpatterns = [
    # path("our_class",views.our_class, name='our_class'),
    path("next_class",views.next_class, name='next_class'),
    path('current_classes/', views.current_classes, name='current_classes'),
    path('archive_class/<int:class_id>/', views.archive_class, name='archive_class'),
    path('view_Archived_class/', views.view_Archived_class, name='view_Archived_class'),
    path('delete_class/<int:class_id>/', views.delete_class, name='delete_class'),
    path('students/<int:class_id>/', views.students, name='students'),
    # path('view_student_details/<int:class_id>/<str:student_name>/', views.view_student_details, name='view_student_details'),
    path('view_student_details/<int:class_id>/<str:student_name>/', views.prediction, name='view_student_details'),
    path('report_generation/<int:class_id>/', views.report_generation, name='report_generation'),

# path('line-graph/', plot_line_graph, name='plot_line_graph'),
    # path('line-graph/<str:selected_student>/', plot_line_graph, name='plot_line_graph_with_student'),
  

]