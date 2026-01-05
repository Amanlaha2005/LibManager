from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    isbn_no = models.CharField(max_length=13,unique=True)
    quantity = models.IntegerField()
    book_img = models.FileField(upload_to="book_img/" ,default="book_img/default.png", null=True,blank=True)
    
    def __str__(self):
        return self.title
    
class Student(models.Model):
    gender_choice = (('male' , 'male') , ('female' , 'female'))
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=20)
    department = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True,blank=True)
    profile_img = models.ImageField(upload_to="profile_img/" , default="profile_img/default_student.png", null=True,blank=True)
    gender = models.CharField(max_length=10  , choices=gender_choice , null=True , blank=True)
    
    def __str__(self):
        return f"{self.name} --> {self.roll_no}"
    
class IssueBook(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    fine_start_after = models.IntegerField(default=7)
    fine = models.IntegerField(default=0)
    fine_amount = models.IntegerField(default=5)
    return_date = models.DateField(blank=True,null=True)
    is_returned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.student} borrowed {self.book} on {self.issue_date}"
    
    
class AdminRequest(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)
    id_card_number = models.CharField(max_length=30,unique=True)
    profile_img = models.ImageField(upload_to="admin_img",default="admin_img/default_admin.png" , blank=True,null=True)
    
    def __str__(self):
        return self.user.username