from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Book, Student, BorrowedBook



# Custom authorization check for admin users
def admin_check(user):
    return user.is_superuser


def main(request):
    return render(request, 'main.html')


def admin_dashboard(request):
    borrowed_books = BorrowedBook.objects.all()
    all_books = Book.objects.all()
    all_users = Student.objects.all()
    context = {
        'borrowed_books': borrowed_books,
        'all_books': all_books,
        'all_users': all_users,
    }
    return render(request, './main.html', context)


@user_passes_test(admin_check)
def search_student(request):
    results = []
    student_id = request.GET.get('student_id', '').strip()  # Get the student ID from the request

    if student_id:  # If there's an ID provided, filter by ID
        try:
            student_id = int(student_id)  # Convert ID to integer
            results = Student.objects.filter(id=student_id)  # Filter by ID
        except ValueError:
            # Handle the case where the ID is not a valid integer
            results = []

    return render(request, 'search_results.html', {'results': results, 'student_id': student_id})


@user_passes_test(admin_check)
def find_student(request):
    return render(request, 'search_student.html')


def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')