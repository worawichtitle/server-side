from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
# from django.contrib.auth import authenticate, login

from condo.forms import *
from condo.models import *
from django.db.models import Q

# Create your views here.
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
        return redirect("user-home")




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
