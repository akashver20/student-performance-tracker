# from django.shortcuts import render

# Create your views here.
# yourapp/views.py

# from django.shortcuts import render, redirect
from django.shortcuts import render,redirect
from . import forms,models
from teacher import models as tmodel
from teacher.models import Teacher
from django.contrib.auth import login, authenticate
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.contrib import messages
# from .forms import CreateClassForm, UploadStudentsForm
# from .models import Class, Department
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def index(request):
    return render(request,'index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def afteradminlogin(request):
    if is_teacher(request.user):
        return redirect(request, 'teacher/teacher_home')

    return render(request, 'user_home.html')


@login_required(login_url='teacher:signin') #login_url='home'
@never_cache
def user_home(request):
    if is_teacher(request.user):
        return redirect('teacher:teacher_home')
    else:
        return render(request,'user_home.html')



@login_required(login_url='teacher:signin')
def teachers(request):
    fname=tmodel.User.objects.values_list('first_name',flat=True)
    lname=tmodel.User.objects.values_list('last_name',flat=True)
    # mail=tmodel.User.objects.values_list('email')
    # mail_list=[f"{m}" for  m in zip(mail[1:])]
    name = [f"{f} {l}" for f, l in zip(fname[1:], lname[1:])]
    name1=[]
    for i in range(len(name)):
        name1.append(str(name[i]).capitalize())
    
    teacher1=tmodel.User.objects.all()
    return render(request, 'teachers.html', {'teachers': teacher1[1:]})
    





@login_required(login_url='teacher:signin')
def our_class(request):
    return render(request, 'our_class.html')

# def create_class(request):
#     if request.method == 'POST':
#         form = CreateClassForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('Gradewise:class_list')
#     else:
#         form = CreateClassForm()
#     return render(request, 'create_class.html', {'form': form})

# def add_students_from_excel(request, class_id):
#     if request.method == 'POST':
#         form = UploadStudentsForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Assuming the uploaded file has a 'students_data' sheet
#             excel_file = form.cleaned_data['excel_file']
#             df = pd.read_excel(excel_file, sheet_name='students_data')

#             # Assuming 'class' field in the DataFrame corresponds to the Class model
#             class_instance = Class.objects.get(pk=class_id)

#             # Fetch columns needed for prediction
#             X = df[['ie1_scores', 'ie2_scores', 'attendance', 'practical_marks']]

#             # Fetch columns for visualization
#             subjects = ['IE1', 'IE2']
#             students_data = df[['ie1_scores', 'ie2_scores']].values.T

#             # Assuming 'ete_marks' is the column we want to predict
#             # For simplicity, using Linear Regression, you might want to use a more sophisticated model
#             y = df['ete_marks']

#             # Split the data into training and testing sets
#             X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#             # Create a linear regression model and fit it
#             model = LinearRegression()
#             model.fit(X_train, y_train)

#             # Predict ete_marks for the test set
#             y_pred = model.predict(X_test)

#             # Use the trained model to predict ete_marks for students
#             df['predicted_ete'] = model.predict(X)

#             # Visualize data
#             fig, ax = plt.subplots()
#             for i, scores in enumerate(students_data):
#                 ax.plot(subjects, scores, label=f'Student {i + 1}')

#             ax.set_xlabel('Subjects')
#             ax.set_ylabel('Scores')
#             ax.set_title('IE1 and IE2 Scores')
#             ax.legend()

#             # Save the plot to a BytesIO buffer
#             buffer = BytesIO()
#             plt.savefig(buffer, format='png')
#             buffer.seek(0)

#             # Convert the buffer to a base64-encoded string
#             image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

#             # Display the plot along with other details
#             return render(request, 'analyze_data.html', {'image_base64': image_base64})

#     else:
#         form = UploadStudentsForm()

#     return render(request, '.add_students_from_excel.html', {'class_id': class_id, 'form': form})
