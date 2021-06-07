from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('register', views.register),
    path('login', views.login),
    path('home',views.home),
    path('logout',views.logout),
    path('newBook',views.newBook),
    path('createBook',views.createBook),
    path('user/<int:user_id>',views.viewUser),
    path('book/<int:book_id>',views.viewBook),
    path('newReview/<int:book_id>',views.newReview),
    path('review/<int:review_id>',views.deleteReview)
]