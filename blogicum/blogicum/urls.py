from django.conf import settings
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView

handler404 = 'pages.views.page_not_found'
handler403 = 'pages.views.csrf_failure'
handler500 = 'pages.views.internal_server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('blog.urls', namespace='blog')),
    path('auth/registration/', CreateView.as_view(
        template_name='registration/registration_form.html', 
        form_class=UserCreationForm, success_url=reverse_lazy('blog:index'),),
        name='registration',),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('debug/', include(debug_toolbar.urls))]
