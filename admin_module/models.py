from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.shortcuts import reverse 
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError



class Student(AbstractUser):
    student_id = models.IntegerField(unique=True,null=True)
    email = models.EmailField(unique=True)

    # Override the groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='student_groups',  # Use a unique related_name
        blank=True,
        help_text='The groups this student belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='student_user_permissions',  # Use a unique related_name
        blank=True,
        help_text='Specific permissions for this student.',
        verbose_name='user permissions',
    )

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    copies_available = models.PositiveIntegerField()


    def __str__(self):
        return self.title
    
    # def clean(self):
    #     super().clean()
    #     # Convert ISBN to an integer for comparison
    #     try:
    #         isbn_value = int(self.isbn)  # Convert the ISBN to an integer
    #     except ValueError:
    #         raise ValidationError('ISBN must be a valid number.')

    #     if self.copies_available > isbn_value:
    #         raise ValidationError('Copies available must be Less than the ISBN number.')

    def save(self, *args, **kwargs):
        self.clean()  # Call the clean method before saving
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        url = reverse("book_details", args=[self.id])
        return url

class BorrowedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def is_overdue(self):
        return self.return_date < timezone.now() if self.return_date else False
