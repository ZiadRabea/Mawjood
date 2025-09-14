from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AddGrade, AddClassroom, AddStudent
from django.http import JsonResponse
from .models import *
# Create your views here.

@login_required
def home(request):
    return redirect("/grades")

def error(request):
    return render(request, "error.html")
@login_required
def create_grades(request):
    user = request.user.profile 
    if not user.type == "School" :
        return redirect("/error")
    else:
        grades = Grade.objects.filter(school=user)
        if request.method == "POST":
            form = AddGrade(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.school = user
                myform.save()
        else:
            form = AddGrade()
        
        context = {
            "form":form,
            "grades": grades
            }
    
        return render(request, "manage_grades.html", context)

@login_required
def show_grades(request):
    user = request.user.profile
    grades = Grade.objects.filter(school=user) if user.type=="School" else Grade.objects.filter(school = user.school)
    
    context = {
        "grades":grades
    }

    return render(request, "grades.html", context)

@login_required
def delete_grade(request, id): 
    grade = Grade.objects.get(id=id)
    user = request.user.profile
    if user.type == "School" and grade.school == user:
        grade.delete()
        return redirect("/")
    else:
        return redirect("/error")

@login_required
def create_classrooms(request, id):
    user = request.user.profile 
    grade = Grade.objects.get(id=id)
    classrooms = Classroom.objects.filter(grade=grade)
    if not (user.type == "School" and grade.school == user):
        return redirect("/error")
    else: 
        if request.method == "POST":
            form = AddClassroom(request.POST, request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.grade = grade
                myform.save()
        else:
            form = AddClassroom()
        
        context = {
            "form":form,
            "classrooms": classrooms
            }
    
        return render(request, "manage_classrooms.html", context)

@login_required
def show_classrooms(request, id):
    user = request.user.profile 
    grade = Grade.objects.get(id=id)

    if (user.type == "School" and grade.school == user) or (user.type == "Teacher" and grade.school == user.school):
        classrooms = Classroom.objects.filter(grade=grade)
        context = {
            "classrooms" : classrooms,
            "grade": grade
        }
        return render(request, "classrooms.html", context)
    else:
        return redirect("/error")

@login_required
def delete_classroom(request, id, cid):
    user = request.user.profile
    grade = Grade.objects.get(id=id)
    classroom = Classroom.objects.get(id=cid)
    if classroom.grade != grade:
        return redirect("/error")
    if user.type == "School" and classroom.grade.school == user:
        classroom.delete()
        return redirect(f"/grades/{grade.id}/classrooms")
    else:
        return redirect("/error")
    

@login_required
def add_student(request, id=None):
    user = request.user.profile 
    if user.type == 'School':
        if request.method == "POST":
            if id:
                student = Student.objects.get(id=id)
                form = AddStudent(request.POST, request.FILES, instance=student, school=user)
            else:
                form = AddStudent(request.POST, request.FILES, school=user)
            if form.is_valid():
                student = form.save()
                return redirect(f"/grades/{student.classroom.grade.id}/classrooms/{student.classroom.id}/students")
        else:
            if id:
                student = Student.objects.get(id=id)
                form = AddStudent(instance=student, school=user)
            else:
                form = AddStudent(school=user)
        
        context = {
            "form":form
        }

        return render(request, "addstudent.html", context)
    else:
        return redirect("/error")

@login_required
def students(request, id, cid):
    user = request.user.profile
    classroom = Classroom.objects.get(id=cid)

    if (user.type == "School" and classroom.grade.school == user) or (user.type == "Teacher" and classroom.grade.school == user.school):
        st = Student.objects.filter(classroom = classroom)

        context = {
            "students": st,
            "classroom": classroom,
            "grade": classroom.grade
        }

        return render(request, "students.html", context)
    else:
        return redirect("/error")

@login_required
def delete_sutudent(request, id):
    user = request.user.profile
    student = Student.objects.get(id=id)
    if student.grade.school == user and user.type == "School":
        student.delete()
        return redirect(f"/grades/{student.classroom.grade.id}/classrooms/{student.classroom.id}/students")
    else:
        return redirect("/error")

@login_required
def register_absence(request, id):
    student = Student.objects.get(id=id)
    user = request.user.profile
    if student.grade.school == user.school and user.type == "Teacher":
        student.registered = True
        student.attending = False
        student.monthly_absence +=1
        student.total_absence +=1
        student.save()
        return redirect(f"/grades/{student.classroom.grade.id}/classrooms/{student.classroom.id}/students")
    else:
        return redirect("/error")
    
@login_required
def register_presence(request, id):
    student = Student.objects.get(id=id)
    user = request.user.profile
    if student.grade.school == user.school and user.type == "Teacher":
        student.registered = True
        student.attending = True
        student.save()
        return redirect(f"/grades/{student.classroom.grade.id}/classrooms/{student.classroom.id}/students")
    else:
        return redirect("/error")   
    
@login_required
def register_attendance(request, cid):
    user = request.user.profile
    classroom = Classroom.objects.get(id=cid)
    if user.type =="Teacher" and user.school == classroom.grade.school: 
        Student.objects.filter(classroom=classroom, registered=False).update(attending=True, registered=True)
        return redirect(f'/grades/{classroom.grade.id}/classrooms/{classroom.id}/students')
    else:
        return redirect("/error")  

@login_required
def auto_reports(request, id):
    user = request.user.profile
    classroom = Classroom.objects.get(id=id)

    if user.type == "School" and classroom.grade.school == user:
        students = Student.objects.filter(classroom = classroom)
        reports = [Report(student=s, monthly_absences=s.monthly_absence) for s in students]
        students.update(monthly_absence=0)
        Report.objects.bulk_create(reports)
        messages.success(request, "Reports generated successfully!")
        return redirect(f"/grades/{classroom.grade.id}/classrooms/{classroom.id}/students")
@login_required
def reports(request, id):
    user = request.user.profile
    student = Student.objects.get(id=id)

    if student.classroom.grade.school == user and user.type == "School":
        r = Report.objects.filter(student=student)
        context = {
            "student": student,
            "reports": r
        }
        return render(request, "reports.html", context)
    
@login_required
def add_options(request):
    if request.user.profile.type == "School":
        return render(request, "add.html")
    else:
        return redirect("/error")
    
def reset(request):
    if request.GET.get("token") == "secret123":
        Student.objects.all().update(registered=False, attending=True)
        return JsonResponse({"status": "success", "message": "Absences reset"})
    return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
