from django.conf.urls import url
from django.contrib.auth import views as v
from accounts.forms import LoginForm
from accounts import views as account_views


urlpatterns = [
    url(r'^login/$', v.login, {'template_name': 'accounts/login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', v.logout, {'next_page': '/accounts/login'},  name='logout'),
    url(r'^change_password$', account_views.change_password, name='change_password'),
    url(r'^edit_profile/$', account_views.user_profile, name='edit_profile'),
]