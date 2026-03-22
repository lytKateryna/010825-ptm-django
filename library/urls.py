"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path

from my_app.views import (
    get_all_books,
    get_book_by_id,
    create_new_book,
    update_book,
    delete_book
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', get_all_books),
    path('books/create/', create_new_book),
    path('books/<int:pk>', get_book_by_id),
    path('books/<int:pk>/update/', update_book),
    path('books/<int:pk>/delete/', delete_book),
]
