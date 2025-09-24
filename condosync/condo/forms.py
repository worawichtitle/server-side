from django import forms
from condo.models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError

import hashlib

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password_hash']
        widgets = {
            'password_hash': forms.PasswordInput(),
        }
    def clean(self):
        cleaned_data = super().clean()
        userinput = cleaned_data.get("username")
        password = cleaned_data.get("password_hash")
        user = User.objects.filter(username=userinput).first()
        if not user:
            user = User.objects.filter(email=userinput).first()
        if not user:
            raise ValidationError("User not found.")
        password_input_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_input_hash != user.password_hash:
            raise ValidationError("Incorrect username or password.")
        self.user = user
        return cleaned_data


# class StudentForm(ModelForm):
#     class Meta:
#         model = Student
#         fields = ['student_id', 'first_name', 'last_name', 'faculty', 'enrolled_sections']
#         widgets = {
            # 'faculty': forms.RadioSelect(),
#             # 'enrolled_sections': forms.CheckboxSelectMultiple(),
#             'address': forms.Textarea(attrs={'rows': 3}),
#         }
#     def clean_student_id(self):
#         data = self.cleaned_data["student_id"]
#         if StudentProfile.objects.filter(student_id=data).exists():
#             raise ValidationError("This student_id is already in use")
#         return data
# class StudentProfileForm(ModelForm):
#     class Meta:
#         model = StudentProfile
#         fields = ['email', 'phone_number', 'address']
#         widgets = {
#             'address': forms.Textarea(attrs={'rows': 3}),
#         }

#     def clean_email(self):
#         data = self.cleaned_data["email"]
#         if "@kmitl.ac.th" not in data:
#             raise ValidationError("Email must end with @kmitl.ac.th")
#         elif StudentProfile.objects.filter(email=data).exists():
#             raise ValidationError("This email is already in use")
#         return data
    
# class CourseForm(ModelForm):
#     class Meta:
#         model = Course
#         fields = ['course_code', 'course_name', 'credits']

# class SectionForm(ModelForm):
#     class Meta:
#         model = Section
#         fields = ['section_number', 'semester', 'professor', 'day_of_week', 'start_time', 'end_time', 'capacity']
#         widgets = {
#             'start_time': forms.TimeInput(attrs={'type': 'time'}),
#             'end_time': forms.TimeInput(attrs={'type': 'time'}),
#             'day_of_week': forms.Select(),
#             'professor': forms.Select(),
#         }
#     def clean(self):
#         cleaned_data = super().clean()
#         start_time = cleaned_data.get("start_time")
#         end_time = cleaned_data.get("end_time")
#         if start_time and end_time and end_time < start_time:
#             raise ValidationError(
#                     "End time cannot be before start time"
#                 )
#         return cleaned_data
#     def clean_capacity(self):
#         data = self.cleaned_data["capacity"]
#         print(data)
#         if data < 20:
#             raise ValidationError("Capacity must be more than 20")
#         return data