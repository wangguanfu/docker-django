# from django.conf.urls import patterns, url
import views as user
from django.conf.urls import url

urlpatterns = [
    # urls for device
    url(r'^login/', user.login),
    url(r'^get/', user.get_users),
    url(r'^add/', user.add_user),
    url(r'^delete/', user.delete_user),
    url(r'^update/', user.update_user),
    url(r'^logout/', user.log_out),
    url(r'^get_roles/', user.get_roles),
    url(r'^add_roles/', user.add_roles),
    url(r'^update_roles/', user.update_roles),
    url(r'^message/', user.get_audit_log),
    url(r'^profile/', user.get_groups),
    url(r'^edit_profile/', user.get_groups),
    url(r'^get_groups/', user.get_groups),
    # url(r'^update_group/', user.update_group),

]


























