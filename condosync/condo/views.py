from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
# from django.contrib.auth import authenticate, login

from condo.forms import *
from condo.models import *
from django.db.models import Q
from django.db import transaction

# Create your views here.
# -----------USER--------------------------------
class user_login(View):
    def get(self, request, **thisiserror):
        form = LoginForm(request.POST)
        context = {
            'form': form
        }
        context.update(thisiserror)
        return render(request, 'login_user.html', context)
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            return redirect("user-home")
        else:
            print("Form error:", form.errors)
            return self.get(request, error=form.errors)

class user_home(View):
    def get(self, request):
        username = request.session.get("username", "Guest")
        return render(request, 'home_user.html', {"username": username})
        # return render(request, 'home_user.html')

class user_regis(View):
    def get(self, request, **thisiserror):
        form = UserForm(request.POST)
        context = {
            'form': form,
        }
        context.update(thisiserror)
        return render(request, 'regis_user.html', context)
    def post(self, request):
        form = UserForm(request.POST)
        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()
                    return redirect('user-login')
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                context = {
                    'form': form,
                }
                return render(request, 'regis_user.html', context)
        
class user_forgetpw(View):
    def get(self, request, **thisiserror):
        form = ForgetPWForm(request.POST)
        context = {
            'form': form,
        }
        context.update(thisiserror)
        return render(request, 'forgetpw_user.html', context)
    def post(self, request):
        form = ForgetPWForm(request.POST)
        try:
            with transaction.atomic():
                if form.is_valid():
                    user = form.user
                    user.password_hash = form.cleaned_data["password_hash"]
                    user.save()
                    # print("form User:", user.id, user.username)
                    return redirect('user-login')
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                context = {
                    'form': form,
                }
                return render(request, 'forgetpw_user.html', context)

# -----------STAFF------------------------------------------------
class staff_login(View):
    def get(self, request, **thisiserror):
        form = StaffLoginForm(request.POST)
        context = {
            'form': form
        }
        context.update(thisiserror)
        return render(request, 'login_staff.html', context)
    def post(self, request):
        form = StaffLoginForm(request.POST)
        if form.is_valid():
            staff = form.staff
            request.session["staff_id"] = staff.id
            request.session["username"] = staff.username
            return redirect("staff-home")
        else:
            print("Form error:", form.errors)
            return self.get(request, error=form.errors)

class staff_home(View):
    def get(self, request):
        username = request.session.get("username", "Guest")
        return render(request, 'home_staff.html', {"username": username})
    
class staff_regis(View):
    def get(self, request, **thisiserror):
        form = StaffForm(request.POST)
        context = {
            'form': form,
        }
        context.update(thisiserror)
        return render(request, 'regis_staff.html', context)
    def post(self, request):
        form = StaffForm(request.POST)
        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()
                    return redirect('staff-login')
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                print("try error:", e)
                context = {
                    'form': form,
                }
                return render(request, 'regis_staff.html', context)

class staff_forgetpw(View):
    def get(self, request, **thisiserror):
        form = StaffForgetPWForm(request.POST)
        context = {
            'form': form,
        }
        context.update(thisiserror)
        return render(request, 'forgetpw_staff.html', context)
    def post(self, request):
        form = StaffForgetPWForm(request.POST)
        try:
            with transaction.atomic():
                if form.is_valid():
                    user = form.user
                    user.password_hash = form.cleaned_data["password_hash"]
                    user.save()
                    # print("form User:", user.id, user.username)
                    return redirect('staff-login')
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                context = {
                    'form': form,
                }
                return render(request, 'forgetpw_staff.html', context)

# class create_course(View):
#     def get(self, request, **thisiserror):
#         cform = CourseForm(request.POST)
#         sform = SectionForm(request.POST)
#         context = {
#             'cform': cform,
#             'sform': sform,
#         }
#         context.update(thisiserror)
#         return render(request, 'create_course.html', context)
#     def post(self, request):
#         cform = CourseForm(request.POST)
#         sform = SectionForm(request.POST)
#         if cform.is_valid() and sform.is_valid():
#             try:
#                 course = cform.save()
#                 section = sform.save(commit=False)
#                 section.course = course
#                 section.save()
#                 return redirect('course-list')
#             except Exception as e:
#                 context = {
#                     'cform': cform,
#                     'sform': sform
#                 }
#                 print("cform", cform.errors)
#                 print("sform", sform.errors)
#                 return render(request, 'create_course.html', context, error=e)
#         else:
#             print("cform", cform.errors)
#             print("sform", sform.errors)
#             return self.get(request, error=cform.errors)
        
# class update_course(View):
#     def get(self, request, course_code, **thisiserror):
#         print(course_code)
#         course = Course.objects.get(course_code=course_code)
#         print(course)
#         section = Section.objects.filter(course_id=course.id).first()
#         cform = CourseForm(request.POST, instance=course)
#         sform = SectionForm(request.POST, instance=section)
#         context = {
#             'cform': cform,
#             'sform': sform,
#             'course_code': course_code,
#         }
#         context.update(thisiserror)
#         return render(request, 'update_course.html', context)

#     def post(self, request, course_code):
#         course = Course.objects.get(course_code=course_code)
#         section = Section.objects.filter(course_id=course.id).first()
#         cform = CourseForm(request.POST, instance=course)
#         sform = SectionForm(request.POST, instance=section)
#         if cform.is_valid() and sform.is_valid():
#             try:
#                 course = cform.save()
#                 section = sform.save(commit=False)
#                 section.course = course
#                 section.save()
#                 return redirect('course-list')
#             except Exception as e:
#                 context = {
#                     'cform': cform,
#                     'sform': sform,
#                 }
#                 return render(request, 'update_course.html', context)
#         else:
#             context = {
#                 'cform': cform,
#                 'sform': sform,
#             }
#             return render(request, 'update_course.html', context)
