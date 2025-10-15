from django.urls import path

from . import views
from condo.views import *

urlpatterns = [
    # ex: /  or  {% url 'user-login' %}
    path("", views.user_login.as_view(), name="user-login"),
    # ex: /regis/  or  {% url 'user-regis' %}
    path("regis/", views.user_regis.as_view(), name="user-regis"),
    # ex: /changepw/1/  or  {% url 'user-changepw' user_id %}
    path("changepw/<int:user_id>/", views.user_changepw.as_view(), name="user-changepw"),
    # ex: /home/  or  {% url 'user-home' %}
    path("home/", views.user_home.as_view(), name="user-home"),
     # ex: /profile_user/1/  or  {% url 'user-profile' user_id %}
    path("profile_user/<int:user_id>/", views.user_profile.as_view(), name="user-profile"),
    # ex: /update_user/1/  or  {% url 'user-update' user_id %}
    path("update_user/<int:user_id>/", views.user_update.as_view(), name="user-update"),
    # ex: /create_condo/  or  {% url 'condo-create' %}
    path("create_condo/", views.condo_create.as_view(), name="condo-create"),
    # ex: /condo_update/  or  {% url 'condo-update' deed_number %}
    path("update_condo/<deed_number>/", views.condo_update.as_view(), name="condo-update"),
    # ex: /detail_condo/1/  or  {% url 'condo-detail' deed_number %}
    path("detail_condo/<deed_number>/", views.condo_detail.as_view(), name="condo-detail"),
    # ex: /update_list/1/  or  {% url 'list-update' list_id %}
    path("update_list/<list_id>/", views.condolist_edit.as_view(), name="list-update"),

    # ex: /logout/  or  {% url 'logout' %}
    path("logout/", views.logout.as_view(), name="logout"),
    path("condolist/", views.condo_list.as_view(), name="condo-list"),
    # ex: /status_edit/1/  or  {% url 'status-edit' deed_number %}
    path("status_edit/<deed_number>/", status_edit.as_view(), name="status-edit"),
    path("status_edit/<deed_number>/cancel/", status_edit.as_view(), name="status-cancel"),

    # ------STAFF----------------
    # ex: /login_staff/  or  {% url 'staff-login' %}
    path("login_staff/", views.staff_login.as_view(), name="staff-login"),
    # ex: /home_staff/  or  {% url 'staff-home' %}
    path("home_staff/", views.staff_home.as_view(), name="staff-home"),
    # ex: /regis_staff/  or  {% url 'staff-regis' %}
    path("regis_staff/", views.staff_regis.as_view(), name="staff-regis"),
    # ex: /changepw_staff/1/  or  {% url 'staff-changepw' staff_id %}
    path("changepw_staff/<int:staff_id>/", views.staff_changepw.as_view(), name="staff-changepw"),
    # ex: /profile_staff/1/  or  {% url 'staff-profile' staff_id %}
    path("profile_staff/<int:staff_id>/", views.staff_profile.as_view(), name="staff-profile"),
    # ex: /update_staff/1/  or  {% url 'staff-update' staff_id %}
    path("update_staff/<int:staff_id>/", views.staff_update.as_view(), name="staff-update"),
    # ex: /detail_condo_staff/1/  or  {% url 'staff-cdetail' deed_number %}
    path("detail_condo_staff/<deed_number>/", views.staff_cdetail.as_view(), name="staff-cdetail"),
    # ex: /update_condo_staff/1/  or  {% url 'staff-cupdate' deed_number %}
    path("update_condo_staff/<deed_number>/", views.status_edit.as_view(), name="staff-cupdate"),
    # ex: /report_staff/1/  or  {% url 'staff-report' deed_number %}
    path("report_staff/<deed_number>/", views.staff_report.as_view(), name="staff-report"),
]