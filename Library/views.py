from django.shortcuts import render , redirect ,get_object_or_404
from Library.models import *
from django.contrib import messages
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login , logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

# Creating the register and Login page for students ...

def RegisterStudent(request):
    if request.method == "POST":
        name = request.POST.get('name')
        roll_no = request.POST.get('roll_no')
        department = request.POST.get('department')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        profile_img = request.FILES.get('profile_img')
        
        if User.objects.filter(username = roll_no).exists():
            messages.error(request,"Username already Exists ... ")
            return redirect('RegisterStudent')
        
        else:
            user = User.objects.create_user(username=roll_no , password=password)
            user.is_staff = False
            user.save()
            
            
            Student.objects.create(
                user=user,
                roll_no=roll_no,
                name=name,
                department = department,
                age = age,
                profile_img = profile_img,
                gender = gender
            )
            messages.success(request , "Student details added successfully ... ")
            return redirect('student_login')
        
    return render(request,'RegisterStudent.html')

def LoginStudent(request):
    
    if request.method == "POST":
        roll_no = request.POST.get('roll_no')
        password = request.POST.get('password')
        
        user = authenticate(username = roll_no , password = password)
        
        if user:
            login(request,user)
            messages.success(request,"Logined Successfull ..")
            return redirect('Index')
        else:
            messages.error(request,"Invalid Crendential ..")
            return redirect('student_login')
    
    return render(request,"LoginStudent.html")

# Logout of the students ...

@ login_required
def StudentLogout(request):
    logout(request)
    return redirect('RegisterStudent')


# Admin Registration process ...

def AdminRegister(request):
    if request.method == "POST":
        name = request.POST.get('name')
        id_card_number = request.POST.get('id_card_number')
        password = request.POST.get('password')
        profile_img = request.FILES.get('profile_img')
        
        if User.objects.filter(username=id_card_number).exists():
            messages.error(request,"Admin Already exists")
            return redirect('admin_register')
        
        user = User.objects.create_user(
            username=id_card_number,
            password=password
        )
        
        user.is_staff = False
        user.save()
        
        AdminRequest.objects.create(
            user =user,
            name = name,
            id_card_number = id_card_number,
            profile_img = profile_img
        )
        
        messages.success(request,"Registration submitted . Waiting for approval ..")
        return redirect('AdminLogin')
    
    return render(request,"AdminRegister.html")
        
# Admin login process .....

def AdminLogin(request):
    
    if request.method == "POST":
        id_card_number = request.POST.get('id_card_number')
        password = request.POST.get('password')
        
        user = authenticate(username = id_card_number , password = password)
        
        if not user:
            messages.error(request,"Invalid Credential .. ")
            return redirect("admin_register")
        
        try:
            admin_request = AdminRequest.objects.get(user = user)
            
        except AdminRequest.DoesNotExist:
            messages.error(request,"Not an adminstrator account")
            return redirect('AdminLogin')
        
        if not admin_request.approved:
            messages.error(request,"Admin Approval pending .")
            return redirect('AdminLogin')
        
        user.is_staff = True
        user.save()
        login(request,user)
        return redirect("Dashboard")
    
    return render(request,"AdminLogin.html")

# Admin logout Scene ...

def AdminLogout(request):
    
    if not request.user.is_staff:
        messages.error(request,"Not an admin ..")
        return redirect('AdminLogin')
    logout(request)
    return redirect('Home')

# Home page for all :

def Home(request):
    return render(request,"Home.html")

@ login_required
def Dashboard(request):
    return render(request,"Dashboard.html")

@login_required
def Index(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None

    return render(request, 'index.html', {'student': student})

# Creating All the books details ...

def AddBook(request):
    
    if not request.user.is_staff:
        return redirect('AdminLogin')
    
    if request.method == "POST":
        
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn_no = request.POST.get('isbn_no')
        quantity = request.POST.get('quantity')
        book_img = request.FILES.get('book_img')
        
        Book.objects.create(
            title = title,
            author = author,
            isbn_no = isbn_no,
            quantity = quantity,
            book_img=book_img
            )
        messages.success(request,"Book added successfully ..")
        return redirect('view_book')
    
    return render(request,'AddBook.html')

# Editing the book ...

def EditBook(request , book_id):
    
    if not request.user.is_staff:
        messages.error(request,"Not an adminstractor accounts ..")
        return redirect("AdminLogin")
    
    book = get_object_or_404(Book,id = book_id)
    
    if request.method == "POST":
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.isbn_no = request.POST.get('isbn_no')
        book.quantity = request.POST.get('quantity')
        book.book_img = request.FILES.get('book_img')

        
        book.save()
        messages.success(request,"Book edited successfully ..")
        return redirect('view_book')
    
    return render(request,'EditBook.html', {'book':book})

# Viewing the book ....

@ login_required
def ViewBook(request):
    Books = Book.objects.all()
     
    search = request.GET.get('search')
        
    if search:
        Books = Book.objects.filter(
            Q(title__icontains =search) |
            Q(author__icontains =search)
        )
    
    return render(request,'ViewBook.html', {'Books':Books})

# Deleting the book ..

def DeleteBook(request,book_id):
    
    if not request.user.is_staff:
        messages.error(request,"Not an adminstrator accounts ..")
        return redirect("AdminLogin")
    
    book = get_object_or_404(Book,id = book_id)
    
    book.delete()
    messages.success(request,"Book deleted successfully ...")
    return redirect('view_book')
        
# Book Part completed ...

# Adding Student Details ..

def AddStudent(request):
    if not request.user.is_staff:
        messages.error(request, "Not an administrator account.")
        return redirect("AdminLogin")

    if request.method == "POST":
        name = request.POST.get('name')
        roll_no = request.POST.get('roll_no')
        department = request.POST.get('department')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        profile_img = request.FILES.get('profile_img')

        # 🔒 Prevent duplicate roll numbers
        if User.objects.filter(username=roll_no).exists():
            messages.error(request, "Student with this roll number already exists.")
            return redirect('AddStudent')

        # 🔑 Create User (default password)
        user = User.objects.create_user(
            username=roll_no,
            password="student@123"   # admin can tell student to change later
        )

        # 👤 Create Student profile
        Student.objects.create(
            user=user,
            roll_no=roll_no,
            name=name,
            department=department,
            age=age,
            gender=gender,
            profile_img=profile_img
        )

        messages.success(request, "Student added successfully.")
        return redirect('view_students')

    return render(request, 'AddStudent.html')


def EditStudent(request,student_id):
    
    if not request.user.is_staff:
        messages.error(request,"Not an adminstrator accounts ..")
        return redirect("AdminLogin")
    
    student = get_object_or_404(Student,id = student_id)
    
    if request.method == "POST":
        student.name = request.POST.get('name')
        student.roll_no = request.POST.get('roll_no')
        student.department = request.POST.get('department')
        student.age = request.POST.get('age')
        student.gender = request.POST.get('gender')
        student.profile_img = request.FILES.get('profile_img')
        
        
        student.save()
        messages.success(request,"Student edited successfully ...")
        return redirect('view_students')
    
    return render(request,'EditStudent.html',{'student':student})

# viewing all students ...

def ViewStudent(request):
    
    students = Student.objects.all()
    
    
    search = request.GET.get('search')
        
    if search:
        students = Student.objects.filter(
            Q(name__icontains = search) |
            Q(roll_no__icontains = search) |
            Q(department__icontains = search)  |
            Q(age__icontains = search)
        )
    
    return render(request,'ViewStudent.html',{'students':students})

# Deleting the students ....

def DeleteStudent(request,student_id):
    if not request.user.is_staff:
        messages.error(request,"Not an adminstrator accounts ..")
        return redirect("AdminLogin")
    
    student = get_object_or_404(Student,id = student_id)
    
    book_returned = IssueBook.objects.filter(
        student=student,
        is_returned = False
    ).exists()
    
    if book_returned:
        messages.error(request,"This Student has not return the book yet ...")
        return redirect('view_students')
    
    student.delete()
    return redirect('view_students')

# Here the students details has completed ....


# Adding issue book ..

def AddIssueBook(request):
    if not request.user.is_staff:
        messages.error(request,"Not an adminstrator accounts ..")
        return redirect("AdminLogin")
    
    books = Book.objects.all()
    students = Student.objects.all()
    
    if request.method == "POST":
        book_id = request.POST.get('book')
        student_id = request.POST.get('student')
        fine_start_after = int(request.POST.get('fine_start_after'))
        fine_amount = int(request.POST.get('fine_amount'))
        
        book = Book.objects.get(id=book_id)
        student = Student.objects.get(id=student_id)
        
        if book.quantity <= 0:
            messages.error(request,"Book Not Available")
        
        else:
            IssueBook.objects.create(
                book=book,
                student = student,
                fine_start_after = fine_start_after,
                fine_amount = fine_amount
            )
            book.quantity = book.quantity-1
            book.save()
            return redirect('View_IssueBook')
        
        return redirect('View_IssueBook')
    
    context = {
        'books':books,
        'students':students
    }
        
    return render(request,'AddIssueBook.html',context)

# Returning the issue books ...

def ReturnBook(request,issue_id):
    if not request.user.is_staff:
        messages.error(request,"Not an adminstrator accounts ..")
        return redirect("AdminLogin")
    
    issue = get_object_or_404(IssueBook,id = issue_id)
    
    if not issue.is_returned:
        
        total_days = (date.today() - issue.issue_date).days
        
        if total_days > issue.fine_start_after:
            issue.fine = (total_days - issue.fine_start_after) * (issue.fine_amount)
            
        else:
            issue.fine =0
            
        issue.is_returned = True
        issue.return_date = date.today()
        issue.save()
            
        book = issue.book
        book.quantity = book.quantity +1 
        book.save()
            
    return redirect('View_IssueBook')
    
# Viewing the issue books ..

def ViewIssueBook(request):
    
    if not request.user.is_staff:
        messages.error(request,"Not an administrator account.")
        return redirect('AdminLogin')
    
    issue = IssueBook.objects.all()
    
    return render (request,"ViewIssueBook.html" , {'issue':issue})

# Editing the issue books .. 

def EditIssueBook(request,issue_id):
    if not request.user.is_staff:
        messages.error(request,"Not an adminstrator accounts ..")
        return redirect("AdminLogin")
    
    
    issue_book = get_object_or_404(IssueBook,id=issue_id)
    
    if request.method == "POST":
        issue_book.book_id = request.POST.get('book')
        issue_book.student_id = request.POST.get('student')
        issue_book.fine_start_after = int(request.POST.get('fine_start_after'))
        issue_book.fine_amount = int(request.POST.get('fine_amount'))
        
        issue_book.save()
        return redirect('View_IssueBook')
    
    return render(request,"EditIssueBook.html",{'issue_book':issue_book})

# Deleting the IssueBook ....

def DeleteIssueBook(request,issue_id):
    if not request.user.is_staff:
        messages.error(request,"Not an adminstrator accounts ..")
        return redirect("AdminLogin")
    
    
    issue = get_object_or_404(IssueBook,id = issue_id)
    
    if issue.is_returned == False:
        messages.error(request,"First Return The Book Then Delete")
        return redirect('View_IssueBook')
    else:
        issue.delete()
        messages.success(request,"Successfully deleted the issue record .")
        return redirect('View_IssueBook')
    
# Student viewing their issue book history and status ...

def StudentIssueBookStatus(request):
    
    if not request.user.is_authenticated:
        return redirect('student_login')
    
    try:
            student = Student.objects.get(user = request.user)

    except Student.DoesNotExist:
        messages.error(request,"Student profile not found . ")
        return redirect('student_login')
    
    issue_book = IssueBook.objects.filter(student=student)
    
    if request.method == "POST":
        search = request.POST.get('search')
        
        if search:
            if search == "Pending":
                issue_book = issue_book.filter(
                    is_returned = False
                )
            elif search == "Returned":
                issue_book = issue_book.filter(
                    is_returned = True
                )            
    
    return render(request,"StudentIssueBookStatus.html", {'issue_book':issue_book})
        

# Profile Page of student and admin ...

# sudent Profile Page ..

def StudentProfile(request):
    
    if not request.user.is_authenticated:
        return redirect('student_login')
    try:
        student = Student.objects.get(user = request.user)
    
    except Student.DoesNotExist:
        messages.error(request,"Student Details Doesnot exists .")
        return redirect('student_login')
    
    return render(request,"StudentProfile.html",{'student':student})