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
            request.session.flush()
            user = form.user
            request.session.set_expiry(21600)  # 6 hours in seconds
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            return redirect("user-home")
        else:
            print("Form error:", form.errors)
            return self.get(request, error=form.errors)

class user_home(View):
    def get(self, request):
        if not request.session.get("user_id"):
            return redirect("user-login")
        context = {
            'username': request.session.get("username"),
            'user_id': request.session.get("user_id")
        }
        return render(request, 'home_user.html', context)
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
        
class user_profile(View):
    def get(self, request, user_id):
        if request.session.get("staff_id"):
            pass
        elif request.session.get("user_id") != user_id:
            if  not request.session.get("user_id"):
                return redirect("user-login")
            return redirect("user-home")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return redirect("user-login")
        context = {
            'user_id': user_id,
            'user': user
        }
        return render(request, 'profile_user.html', context)
    
class user_update(View):
    def get(self, request, user_id, **thisiserror):
        if not request.session.get("user_id"):
            return redirect("user-login")
        if request.session.get("user_id") != user_id:
            return redirect("user-home")
        user = User.objects.get(pk=user_id)
        print(user.id)
        form = UserUpdateForm(instance=user)
        context = {
            'form': form,
            'user_id': user_id,
            'user': user,
        }
        context.update(thisiserror)
        return render(request, 'update_user.html', context)
    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = UserUpdateForm(request.POST, instance=user)
        try:
            with transaction.atomic():
                if form.is_valid():
                    user = form.save()
                    return redirect('user-profile', user_id)
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                print("try error:", e)
                context = {
                    'form': form,
                    'user_id': user_id,
                    'user': user,
                }
                return render(request, 'update_user.html', context)

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
            request.session.flush()
            staff = form.staff
            request.session.set_expiry(21600)  # 6 hours in seconds
            request.session["staff_id"] = staff.id
            request.session["username"] = staff.username
            return redirect("staff-home")
        else:
            print("Form error:", form.errors)
            return self.get(request, error=form.errors)

class staff_home(View):
    def get(self, request):
        if not request.session.get("staff_id"):
            return redirect("staff-login")
        context = {
            'username': request.session.get("username"),
            'staff_id': request.session.get("staff_id")
        }
        return render(request, 'home_staff.html', context)
    
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
        
class staff_profile(View):
    def get(self, request, staff_id):
        if not request.session.get("staff_id"):
            return redirect("staff-login")
        if request.session.get("staff_id") != staff_id:
            return redirect("staff-home")
        try:
            staff = Staff.objects.get(pk=staff_id)
        except Staff.DoesNotExist:
            return redirect("staff-login")
        context = {
            'staff_id': staff_id,
            'staff': staff
        }
        return render(request, 'profile_staff.html', context)

class staff_update(View):
    def get(self, request, staff_id, **thisiserror):
        if not request.session.get("staff_id"):
            return redirect("staff-login")
        if request.session.get("staff_id") != staff_id:
            return redirect("staff-home")
        staff = Staff.objects.get(pk=staff_id)
        print(staff.id)
        form = StaffUpdateForm(instance=staff)
        context = {
            'form': form,
            'staff_id': staff_id,
            'staff': staff,
        }
        context.update(thisiserror)
        return render(request, 'update_staff.html', context)
    def post(self, request, staff_id):
        staff = Staff.objects.get(pk=staff_id)
        form = StaffUpdateForm(request.POST, instance=staff)
        try:
            with transaction.atomic():
                if form.is_valid():
                    staff = form.save()
                    return redirect('staff-profile', staff_id)
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                print("try error:", e)
                context = {
                    'form': form,
                    'staff_id': staff_id,
                    'staff': staff,
                }
                return render(request, 'update_staff.html', context)
        
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
