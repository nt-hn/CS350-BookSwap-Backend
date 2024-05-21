"""
URL configuration for BookSwap_Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from account_api import urls
from book import urls
from chat import urls
from book_request import urls
from landing_page import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('account_api/', include('account_api.urls')),
    path('book/', include('book.urls')),
    path('chat/', include('chat.urls')),
    path('book_request/', include('book_request.urls')),
    path('', include('landing_page.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
