from admin_module.models import Book, BorrowedBook, Student
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from admin_module.views import admin_check
from student_module.forms import StudentSignupForm, ReturnDateForm, Bookform
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.views.generic import DetailView
from django.utils.decorators import method_decorator






@user_passes_test(admin_check)
def admin_dashboard(request):
    borrowed_books = BorrowedBook.objects.all()
    all_books = Book.objects.all()
    all_users = Student.objects.all()
    context = {
        'borrowed_books': borrowed_books,
        'all_books': all_books,
        'all_users': all_users,
    }
    return render(request, 'dashboard.html', context)





@login_required
def student_dashboard(request):
    borrowed_books = BorrowedBook.objects.filter(student=request.user)
    context = {'borrowed_books': borrowed_books}
    return render(request, 'student_module/dashboard.html', context)



@login_required
def view_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'books/books_index.html', context)

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.copies_available > 0:
        BorrowedBook.objects.create(student=request.user, book=book)
        book.copies_available -= 1
        book.save()
        return redirect('student_dashboard')

@user_passes_test(admin_check)
def create_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        copies_available = request.POST.get('copies_available')
        Book.objects.create(title=title, author=author, copies_available=copies_available)
        return redirect('admin_dashboard')
    return render(request, 'books/create_book.html')



@login_required
def return_book(request, borrowed_book_id):
    borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_book_id)
    borrowed_book.return_date = timezone.now()
    borrowed_book.book.copies_available += 1
    borrowed_book.book.save()
    borrowed_book.save()
    return redirect('student_dashboard')


def signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Specify the backend
            messages.success(request, 'Your account has been created successfully!')
            return redirect('student_dashboard')  # Redirect to student dashboard after signup
        else:
            messages.error(request, 'Please correct the error below.')  # Error message for invalid form
    else:
        form = StudentSignupForm()

    return render(request, 'student_module/signup.html', {'form': form})

from .forms import CustomLoginForm


def login_view(request):
    # If the user is already logged in, redirect to the respective dashboard
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('student_dashboard')

    # Handle the login form submission
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user type
                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('student_dashboard')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = CustomLoginForm()

    # Render the login page if the user is not authenticated
    return render(request, 'registration/login.html', {'form': form})


@login_required
def book_list(request):
    books = Book.objects.filter(is_borrowed=False)  # Only show books that are not borrowed
    return render(request, 'books/book_list.html', {'books': books})


@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.copies_available <= 0:
        messages.error(request, "This book is not available for borrowing.")
        return redirect('book_list')

    if request.method == 'POST':
        form = ReturnDateForm(request.POST)
        if form.is_valid():
            return_date = form.cleaned_data['return_date']

            # Create a new BorrowedBook record
            borrowed_book = BorrowedBook.objects.create(
                student=request.user,
                book=book,
                borrowed_date=timezone.now(),
                return_date=return_date  # Assuming you have a return_date field
            )
            book.copies_available -= 1
            book.save()

            messages.success(request, f"You have borrowed {book.title} until {return_date}.")
            return redirect('view_books')
    else:
        form = ReturnDateForm()

    return render(request, 'books/borrow_book.html', {'form': form, 'book': book})

@user_passes_test(admin_check)
def borrowed_books(request):
    books = BorrowedBook.objects.all()
    return render(request, 'books/borrowed_books.html', {'borrowed_books': books})


@user_passes_test(admin_check)
def get_all_users(request):
    users = Student.objects.all()
    return render(request, 'users.html', {'users': users})

@user_passes_test(admin_check)
def delete_user(request, user_id):
    user = get_object_or_404(Student, id=user_id)
    user.delete()
    return redirect('get_all_users')


@user_passes_test(admin_check)
def add_user(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User added successfully.")
            return redirect('get_all_users')
    else:
        form = StudentSignupForm()

    return render(request, 'student_module/add_user.html', {'form': form})


@user_passes_test(admin_check)
def update_user(request, user_id):
    user = get_object_or_404(Student, id=user_id)
    if request.method == 'POST':
        form = StudentSignupForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('get_all_users')
    else:
        form = StudentSignupForm(instance=user)

    return render(request, 'student_module/update_user.html', {'form': form})

@method_decorator(user_passes_test(admin_check), name='dispatch')
class bookdelete(DeleteView):
    model=Book
    template_name='books/book_delete.html'
    success_url='view_books'

@method_decorator(user_passes_test(admin_check), name='dispatch')
class bookedite(UpdateView):
    model=Book
    template_name='books/book_edite.html'
    form_class= Bookform

@method_decorator(login_required, name='dispatch')
class bookdetails(DetailView):
    model=Book
    template_name='books/book_detail.html'
    context_object_name='book'