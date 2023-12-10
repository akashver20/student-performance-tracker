from django.shortcuts import render,redirect
from . import forms
from .forms import SignInForm
from classes.models import Class
from django.contrib.auth import login, authenticate
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib import messages
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render,redirect,get_object_or_404
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from sklearn.linear_model import LinearRegression
import os
from sklearn.impute import SimpleImputer
import numpy as np
import io

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Gradewise:user_home')  # Redirect to user home page after login
            else:
                pass
    else:
        form = SignInForm()
    return render(request,'index.html')

@login_required(login_url='teacher:signin') 
@never_cache
def teacher_home(request):
    current_classes = Class.objects.filter(session='current')
    # current_classes1 = Class.objects.filter(session='previous')
    user = request.user
    return render(request, 'teacher_home.html', {'current_classes': current_classes,'user':user})

@login_required(login_url='teacher:signin') 
def teacherbase(request):
    user = request.user
    return render(request,'teacher_base.html',{'user':user})



@login_required(login_url='teacher:signin')
def add_teacher(request):
    teacherForm=forms.addTeacherForm()
    
    mydict={'teacherForm': teacherForm}
    if request.method=='POST':
        teacherForm=forms.addTeacherForm(request.POST)
        if teacherForm.is_valid():
            user=teacherForm.save()
            user.set_password(user.password)
            user.save()

            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()

            teacher_group = Group.objects.get_or_create(name='TEACHER')
            teacher_group[0].user_set.add(user)
            return HttpResponseRedirect(reverse('Gradewise:teachers'))
        else:
            error=teacherForm.errors
    return render(request,'add_teacher.html',context=mydict)   

@login_required(login_url='teacher:signin')
def delete_teacher(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        if teacher_id:
            User.objects.filter(id=teacher_id).delete()
            return redirect('Gradewise:teachers')
    # Retrieve the updated list of teachers after deletion
    # teachers = User.objects.all()
    
    return render(request, 'teachers.html')

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Gradewise:user_home')  # Redirect to user home page after login
            else:
                pass
    else:
        form = SignInForm()
    
    return render(request, 'signin.html', {'form': form})



@login_required(login_url='teacher:signin')
def teacher_students(request, class_id):
    class_instance = get_object_or_404(Class, pk=class_id)

    excel_data = pd.read_excel(class_instance.excel_file.path)
    student_names = excel_data['Student Name'].tolist()

    return render(request, 'teacher_students.html', {'class_instance': class_instance, 'student_names': student_names})

@login_required(login_url='teacher:signin')
def teacher_report_generation(request, class_id):
    class_instance = get_object_or_404(Class, pk=class_id)
    current_students = pd.read_excel(class_instance.excel_file.path)
    student_names = current_students['Student Name'].tolist()
    actual_ete =    current_students['original_ETE'].tolist()

    try:
        previous_classes = Class.objects.filter(session='previous')

        merged_wb = Workbook()
        merged_ws = merged_wb.active

        skip_header = False

        for class_instance in previous_classes:
            excel_file_path = class_instance.excel_file.path

            if os.path.exists(excel_file_path):
                df = pd.read_excel(excel_file_path)

                for i, row in enumerate(dataframe_to_rows(df, index=False, header=True)):
                    if skip_header and i == 0:
                        continue
                    merged_ws.append(row)

                skip_header = True

        merged_file_path = 'static/merged_data.xlsx'
        merged_wb.save(merged_file_path)

        messages.success(request, 'Data merged successfully.')

        ie1_columns = [col for col in current_students.columns if 'ie1' in col]
        ie2_columns = [col for col in current_students.columns if 'ie2' in col]
        current_students['IE1'] = current_students[ie1_columns].mean(axis=1)*5
        current_students['IE2'] = current_students[ie2_columns].mean(axis=1)*3.33
        merged_data = pd.read_excel('static\merged_data.xlsx')

        X_current_students = current_students[['IE1', 'IE2']]
        y = merged_data['ETE']

        # Initialize the Linear Regression model
        model = LinearRegression()

       
        model.fit(merged_data[['IE1', 'IE2']], y)

        # Predict the total marks for current students
        current_students['predicted_ete'] = model.predict(X_current_students)
        predicted_ete1=current_students['predicted_ete'].values
        student_data=[]
        for i in range(len(current_students['predicted_ete'].values)):
            x=[student_names[i],actual_ete[i],round(predicted_ete1[i],2) ]
            student_data.append(x)

        roll_no=[]
        for i in range(1,len(predicted_ete1)+1):
            roll_no.append(i)
        

        plt.switch_backend('Agg')
        fig, ax3= plt.subplots(nrows=1, ncols=1, figsize=(15, 5), sharex=True)

        ax3.plot(roll_no, actual_ete, marker='o', linestyle='-', label='actual marks')
        ax3.plot(roll_no, predicted_ete1, marker='o', linestyle='-', label='predicted marks')

        ax3.set_ylabel('Marks')
        ax3.set_title("actual vs predicted")
        ax3.legend()
        for x, y in zip(roll_no, actual_ete):
            ax3.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 5), ha='center')
        ax3.axhline(y=34, color='red', linestyle='--', label='passing mark')

        ax3.set_ylim(0, 100)
        ax3.set_xticks(roll_no)
        ax3.set_xticklabels(roll_no)
        image_stream = io.BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)
        image3_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
        plt.close()

        student_data=[]
        for i in range(len(current_students['predicted_ete'].values)):
            x=[student_names[i],actual_ete[i],round(current_students['predicted_ete'].values[i],2)]
            student_data.append(x)

        return render(request, 'teacher_report_generation.html', {'student_details': student_data,'image3_base64':image3_base64})

    except Exception as e:

        messages.error(request, f'Error processing data: {str(e)}')

    
    return render(request, 'teacher_report_generation.html', {'student_details': None,'image3_base64':image3_base64})



@login_required(login_url='teacher:signin')
def teacher_prediction(request, class_id, student_name):
    class_instance = get_object_or_404(Class, pk=class_id)
    current_students = pd.read_excel(class_instance.excel_file.path)
    student_details = current_students[current_students['Student Name'] == student_name]

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    try:
        previous_classes = Class.objects.filter(session='previous')

        merged_wb = Workbook()
        merged_ws = merged_wb.active

        skip_header = False

        for class_instance in previous_classes:
            excel_file_path = class_instance.excel_file.path

            if os.path.exists(excel_file_path):
                df = pd.read_excel(excel_file_path)

                for i, row in enumerate(dataframe_to_rows(df, index=False, header=True)):
                    if skip_header and i == 0:
                        continue
                    merged_ws.append(row)

                skip_header = True

        merged_file_path = 'static/merged_data.xlsx'
        merged_wb.save(merged_file_path)

        messages.success(request, 'Data merged successfully.')
    except Exception as e:
        messages.error(request, f'Error merging data: {str(e)}')



    
    ie1_columns = [col for col in student_details.columns if 'ie1' in col]
    ie2_columns = [col for col in student_details.columns if 'ie2' in col]
    ie1_average = student_details[ie1_columns].mean(axis=1)*5
    ie2_average = student_details[ie2_columns].mean(axis=1)*3.33
    
    ie1=ie1_average.values[0]
    ie2=ie2_average.values[0]

    merged=pd.read_excel('static\merged_data.xlsx')
    X_train = merged[['IE1','IE2']]
    Y_train=merged[['ETE']]
    imputer = SimpleImputer(strategy='mean')
    X_train_imputed = imputer.fit_transform(X_train)


    student_details_dict = student_details.to_dict(orient='records')

    # Check for NaN values in the imputed data
    if np.isnan(X_train_imputed).any():
        messages.error(request, 'Imputed data contains NaN values.')
        return render(request, 'teacher_view_student_details.html', {'class_instance': class_instance, 'student_details': student_details_dict, 'prediction': None})

    model = LinearRegression()
    try:
        model.fit(X_train_imputed, Y_train)
    except ValueError as e:
        messages.error(request, f'Error fitting the model: {str(e)}')
        return render(request, 'teacher_view_student_details.html', {'class_instance': class_instance, 'student_details': student_details_dict, 'prediction': None})

    # Handle NaN values in the prediction step
    X_pred = imputer.transform([[ie1, ie2]])
    if np.isnan(X_pred).any():
        messages.error(request, 'Input for prediction contains NaN values.')
        return render(request, 'teacher_view_student_details.html', {'class_instance': class_instance, 'student_details': student_details_dict, 'prediction': None})

    predict = model.predict(X_pred)[0]
    prediction=round(predict[0],2)

    
    
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ graphs+++++++++++++++++++++++++++++++++++++++++++++++++++++++

    subjects = [col.replace('_ie1', '') for col in student_details.columns if '_ie1' in col]
    
    plt.switch_backend('Agg')
    x_axis=['ie1','ie2','predicted']
    y_axis=[ie1,ie2,prediction]
    # ''''''''''''''''''''''''''''''''''line graph'''''''''''''''''''
    fig, ax1= plt.subplots(nrows=1, ncols=1, figsize=(8, 5), sharex=True)

    ax1.plot(x_axis, y_axis, marker='o', linestyle='-', label='marks graph')
    ax1.set_ylabel('Marks')
    ax1.set_title(f'Marks for {student_name}')
    ax1.legend()
    for x, y in zip(x_axis, y_axis):
        ax1.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 5), ha='center')
    ax1.axhline(y=34, color='red', linestyle='--', label='passing mark')

    ax1.set_ylim(0, 100)

    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()

#   ==============================bar graph===============================

    x_axis2=np.arange(len(subjects))
    
    ie1_scores=student_details[ie1_columns].values[0]*5
    ie2_scores=student_details[ie2_columns].values[0]*3.33

    plt.bar(x_axis2 - 0.2,ie1_scores , 0.4, label = 'IE1') 
    plt.bar(x_axis2 + 0.2, ie2_scores, 0.4, label = 'IE2')
    plt.xticks(x_axis2, subjects) 
    plt.xlabel("Subjects") 
    plt.ylabel("Marks") 
    plt.title("% Marks in each Subjects") 
    plt.legend()
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

            # Encode the image to base64
    image2_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()

# ++++++++++++++++++++++++++++++  multiple line graph+++++++++++++++++++++++++++++++++++++++
    
    fig, ax3= plt.subplots(nrows=1, ncols=1, figsize=(8, 5), sharex=True)

    ax3.plot(subjects, ie1_scores, marker='o', linestyle='-', label='IE1 marks')
    ax3.plot(subjects, ie2_scores, marker='o', linestyle='-', label='IE2 marks')

    ax3.set_ylabel('Marks')
    ax3.set_title(f' % Marks for {student_name}')
    ax3.legend()
    for x, y in zip(subjects, ie1_scores):
        ax3.annotate(f'{y}', (x, y), textcoords="offset points", xytext=(0, 5), ha='center')
    ax3.axhline(y=34, color='red', linestyle='--', label='passing mark')

    ax3.set_ylim(0, 100)

    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    image3_base64 = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()
    subjects = [col.replace('_ie1', '') for col in student_details.columns if '_ie1' in col]

    
    return render(request, 'teacher_view_student_details.html', {'image_base64': image_base64,'image2_base64':image2_base64,'image3_base64':image3_base64,'class_instance': class_instance, 'student_details': student_details_dict,'prediction': prediction})
    
    