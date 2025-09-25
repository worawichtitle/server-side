from django import forms
from condo.models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError

import hashlib
# -----------USER-----------------------------------
class UserForm(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    class Meta:
        model = User
        fields = ['username', 'password_hash', 'first_name', 'last_name',
                  'email', 'phone', 'main_contact', 'address']
        widgets = {
            'password_hash': forms.PasswordInput(),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    def clean_username(self):
        data = self.cleaned_data["username"]
        if User.objects.filter(username=data).exists():
            raise ValidationError("This username is already in use")
        return data
    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already in use")
        return data
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        # confirm = cleaned_data.get("confirm_password")
        confirm = self.cleaned_data.get("confirm_password")
        if not password or not confirm:
            raise ValidationError("Both password and confirm password are required.")
        if password != confirm:
            raise ValidationError("Passwords do not match")

        # Hash the password before saving
        cleaned_data["password_hash"] = hashlib.sha256(password.encode()).hexdigest()
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="Username or Email")
    password_hash = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password_hash'}),
        label="Password"
    )
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

# -----------Staff----------------------------
class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['username', 'password_hash', 'first_name', 'last_name',
                  'email', 'phone', 'role']
        widgets = {
            'password_hash': forms.PasswordInput(),
            # 'role': forms.Select(),
        }
    def clean_username(self):
        data = self.cleaned_data["username"]
        if User.objects.filter(username=data).exists():
            raise ValidationError("This username is already in use")
        return data
    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already in use")
        return data
    
class StaffLoginForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['username', 'password_hash']
        widgets = {
            'password_hash': forms.PasswordInput(),
        }
    def clean(self):
        cleaned_data = super().clean()
        staffinput = cleaned_data.get("username")
        password = cleaned_data.get("password_hash")
        staff = Staff.objects.filter(username=staffinput).first()
        if not staff:
            staff = Staff.objects.filter(email=staffinput).first()
        if not staff:
            raise ValidationError("User not found.")
        password_input_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_input_hash != staff.password_hash:
            raise ValidationError("Incorrect username or password.")
        self.staff = staff
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