from django.urls import path
from . import views
from .views import login_view,bookdelete,bookedite,bookdetails

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),

    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('students/profile/', views.student_profile, name='student'),
    path('books/', views.view_books, name='view_books'),
    path('create/', views.create_book, name='create_book'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('borrowed/', views.borrowed_books, name='borrowed_books'),
    path('return/<int:borrowed_book_id>/', views.return_book, name='return_book'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', login_view, name='login'),
    path('books/<int:pk>/delete/', bookdelete.as_view(), name='book_delete'),
    path('books/<int:pk>/edit/', bookedite.as_view(), name='book_edit'),
    path('books/<int:pk>/', bookdetails.as_view(), name='book_details'),





    path('get_all_users/', views.get_all_users, name='get_all_users'),

]
