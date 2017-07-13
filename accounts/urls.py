from django.conf.urls import url
from accounts import views
from django.contrib.auth.views import logout
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
	url(r'^favicon.ico$', 
		RedirectView.as_view(
			url=staticfiles_storage.url('favicon.ico'), 
			permanent=False), 
		name="favicon"),
	url(r'^send_login_email$', views.send_login_email, name='send_login_email'),
	url(r'^login$', views.login, name='login'),
	url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
]