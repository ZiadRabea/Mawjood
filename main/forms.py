from django import forms
from.models import Grade, Classroom, Student, Report

class AddGrade(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['title']

class AddClassroom(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['title']

class AddStudent(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'code', 'grade', 'classroom', 'phone']
        
    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)

        if school is None and self.instance.pk:
            school = self.instance

        if school is not None:
            self.fields['classroom'].queryset = Classroom.objects.filter(grade__school=school)
            self.fields['grade'].queryset = Grade.objects.filter(school=school)
        else:
            self.fields['classroom'].queryset = Classroom.objects.none()
            self.fields['grade'].queryset = Grade.objects.none()

class AddGrade(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['title']