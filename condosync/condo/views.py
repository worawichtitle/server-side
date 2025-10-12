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
        return render(request, 'user/login_user.html', context)
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
        try:
            user_id = request.session.get("user_id")
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return redirect("user-login")
        context = {
            'user_id': user_id,
            'user': user
        }
        return render(request, 'user/home_user.html', context)

class user_regis(View):
    def get(self, request, **thisiserror):
        form = UserForm(request.POST)
        pwform = PWForm(request.POST)
        context = {
            'form': form,
            'pwform': pwform,
        }
        context.update(thisiserror)
        return render(request, 'user/regis_user.html', context)
    def post(self, request):
        form = UserForm(request.POST)
        pwform = PWForm(request.POST)
        try:
            with transaction.atomic():
                if form.is_valid() and pwform.is_valid():
                    print('form pass')
                    form_instance = form.save(commit=False)
                    print('PWform pass', pwform.cleaned_data["password_hash"])
                    form_instance.password_hash = pwform.cleaned_data["password_hash"]
                    form_instance.save()
                    return redirect('user-login')
                else:
                    print('Transaction ERROR')
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                print("other error:", e)
                context = {
                    'form': form,
                    'pwform': pwform,
                }
                return render(request, 'user/regis_user.html', context)

class user_changepw(View):
    def get(self, request, user_id, **thisiserror):
        if not request.session.get("user_id"):
            return redirect("user-login")
        if request.session.get("user_id") != user_id:
            return redirect("user-home")
        user = User.objects.get(pk=user_id)
        form = ChangePWForm(request.POST, instance=user)
        context = {
            'form': form,
            'user_id': user_id,
            'user': user,
        }
        context.update(thisiserror)
        return render(request, 'user/changepw_user.html', context)
    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = ChangePWForm(request.POST, instance=user)
        try:
            with transaction.atomic():
                if form.is_valid():
                    user.password_hash = form.cleaned_data["password_hash"]
                    user.save()
                    # print("form User:", user.id, user.username)
                    return redirect('user-profile', user_id)
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                context = {
                    'form': form,
                    'user_id': user_id,
                    'user': user
                }
                return render(request, 'user/changepw_user.html', context)
        
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
            if request.session.get("staff_id"):
                return redirect("staff-home")
            return redirect("user-login")
        context = {
            'user_id': user_id,
            'user': user
        }
        return render(request, 'user/profile_user.html', context)
    
class user_update(View):
    def get(self, request, user_id, **thisiserror):
        if not request.session.get("user_id"):
            return redirect("user-login")
        if request.session.get("user_id") != user_id:
            return redirect("user-home")
        user = User.objects.get(pk=user_id)
        print(user.id)
        form = UserForm(instance=user)
        context = {
            'form': form,
            'user_id': user_id,
            'user': user,
        }
        context.update(thisiserror)
        return render(request, 'user/update_user.html', context)
    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = UserForm(request.POST, instance=user)
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
                return render(request, 'user/update_user.html', context)
        

class logout(View):
    def get(self, request):
        # Clear session keys
        staff = False
        if request.session.get('staff_id'):
            staff = True
        request.session.flush()  # Clears all session data
        if staff:
            return redirect('staff-login') 
        return redirect('user-login') 

# -----------STAFF------------------------------------------------
class staff_login(View):
    def get(self, request, **thisiserror):
        form = StaffLoginForm(request.POST)
        context = {
            'form': form
        }
        context.update(thisiserror)
        return render(request, 'staff/login_staff.html', context)
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
        try:
            staff_id = request.session.get("staff_id")
            staff = Staff.objects.get(pk=staff_id)
        except Staff.DoesNotExist:
            return redirect("staff-login")
        context = {
            'staff_id': staff_id,
            'staff': staff
        }
        return render(request, 'staff/home_staff.html', context)
    
class staff_regis(View):
    def get(self, request, **thisiserror):
        form = StaffForm(request.POST)
        pwform = StaffPWForm(request.POST)
        context = {
            'form': form,
            'pwform': pwform,
        }
        context.update(thisiserror)
        return render(request, 'staff/regis_staff.html', context)
    def post(self, request):
        form = StaffForm(request.POST)
        pwform = StaffPWForm(request.POST)
        try:
            with transaction.atomic():
                if form.is_valid() and pwform.is_valid():
                    form_instance = form.save(commit=False)
                    print('PWform pass', pwform.cleaned_data["password_hash"])
                    form_instance.password_hash = pwform.cleaned_data["password_hash"]
                    form_instance.save()
                    return redirect('staff-login')
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                print("try error:", e)
                context = {
                    'form': form,
                    'pwform': pwform,
                }
                return render(request, 'staff/regis_staff.html', context)
        
class staff_changepw(View):
    def get(self, request, staff_id, **thisiserror):
        if not request.session.get("staff_id"):
            return redirect("staff-login")
        if request.session.get("staff_id") != staff_id:
            return redirect("staff-home")
        staff = Staff.objects.get(pk=staff_id)
        form = StaffChangePWForm(request.POST, instance=staff)
        context = {
            'form': form,
            'staff_id': staff_id,
            'staff': staff,
        }
        context.update(thisiserror)
        return render(request, 'staff/changepw_staff.html', context)
    def post(self, request, staff_id):
        staff = Staff.objects.get(pk=staff_id)
        form = StaffChangePWForm(request.POST, instance=staff)
        try:
            with transaction.atomic():
                if form.is_valid():
                    staff.password_hash = form.cleaned_data["password_hash"]
                    staff.save()
                    # print("form User:", staff.id, staff.staffname)
                    return redirect('staff-profile', staff_id)
                else:
                    raise transaction.TransactionManagementError("Error")
        except Exception as e:
                context = {
                    'form': form,
                    'staff_id': staff_id,
                    'staff': staff
                }
                return render(request, 'staff/changepw_staff.html', context)
        
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
        return render(request, 'staff/profile_staff.html', context)

class staff_update(View):
    def get(self, request, staff_id, **thisiserror):
        if not request.session.get("staff_id"):
            return redirect("staff-login")
        if request.session.get("staff_id") != staff_id:
            return redirect("staff-home")
        staff = Staff.objects.get(pk=staff_id)
        print(staff.id)
        form = StaffForm(instance=staff)
        context = {
            'form': form,
            'staff_id': staff_id,
            'staff': staff,
        }
        context.update(thisiserror)
        return render(request, 'staff/update_staff.html', context)
    def post(self, request, staff_id):
        staff = Staff.objects.get(pk=staff_id)
        form = StaffForm(request.POST, instance=staff)
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
                return render(request, 'staff/update_staff.html', context)

