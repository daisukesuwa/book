"""book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views

app_name = "isbn"

urlpatterns = [
               path('list/', views.BookListView.as_view(), name='book_list'),
               path('create/', views.SearchWordCreateView.as_view(), name='create'),
               path('create_done/', views.create_done, name='create_done'),
               path('word_list/', views.WordListView.as_view(), name='word_list'),
               path('update/<int:pk>/', views.WordUpdateView.as_view(), name='update'),
               path('update_done/', views.update_done, name='update_done'),
               path('delete/<int:pk>/', views.WordDeleteView.as_view(), name='delete'),
               path('delete_done/', views.delete_done, name='delete_done'),
               path('isbn_update/', views.update_isbn_info, name='isbn_update'),
]
