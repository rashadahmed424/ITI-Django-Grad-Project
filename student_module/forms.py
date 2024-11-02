from django import forms
from django.contrib.auth.forms import UserCreationForm
from admin_module.models import Student, BorrowedBook,Book


class StudentSignupForm(UserCreationForm):
    student_id = forms.CharField(max_length=10, required=True, help_text='Required. Your unique student ID.')
    email = forms.EmailField(max_length=200, help_text='Required. Provide a valid email address.')

    class Meta:
        model = Student
        fields = ('username', 'student_id', 'email', 'password1', 'password2')


class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = ['book']  # The student selects the book to borrow

class ReturnDateForm(forms.Form):
    return_date = forms.DateField(widget=forms.SelectDateWidget(), label="Return Date")

class Bookform(forms.ModelForm):
    class Meta:
        model =Book
        fields= '__all__'