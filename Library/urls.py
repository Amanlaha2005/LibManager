from django.urls import path
from Library.views import *

urlpatterns = [
    
    # Registration and login urls ....
    
    path('RegisterStudent/', RegisterStudent , name = "RegisterStudent"),
    path('Login_student/', LoginStudent , name = "student_login"),
    path('admin-register/', AdminRegister, name='admin_register'),
    path('AdminLogin/',AdminLogin,name="AdminLogin"),
    path('StudentLogout/', StudentLogout , name = "StudentLogout"),
    path('adminlogout/',AdminLogout,name = "AdminLogout"),
    
    # Home and dashboard page urls ...
    
    path('Dashboard',Dashboard,name="Dashboard"),
    path('',Home,name ="Home"),
    path('Index/',Index,name ="Index"),
    
    # Book Details urls ....
    
    path('AddBook/',AddBook,name="AddBook"),
    path('ViewBook/',ViewBook,name="view_book"),
    path('EditBook/<int:book_id>/',EditBook,name="EditBook"),
    path('DeleteBook/<int:book_id>/',DeleteBook,name="DeleteBook"),
    
    # Students details urls ...
    
    path('AddStudent/',AddStudent,name="AddStudent"),
    path('EditStudent/<int:student_id>/',EditStudent,name="EditStudent"),
    path('ViewStudent/',ViewStudent,name="view_students"),
    path('DeleteStudent/<int:student_id>/',DeleteStudent,name="DeleteStudent"),
    
    # issue Book details urls ...
    
    path('AddIssueBook/',AddIssueBook,name="AddIssueBook"),
    path('ReturnBook/<int:issue_id>/',ReturnBook,name="ReturnBook"),
    path('ViewIssueBook/',ViewIssueBook,name="View_IssueBook"),
    path('EditIssueBook/<int:issue_id>/',EditIssueBook,name="EditIssueBook"),
    path('DeleteIssueBook/<int:issue_id>/',DeleteIssueBook,name="DeleteIssueBook"),
    
    # student views urls ...
    
    path('StudentIssueBookStatus/',StudentIssueBookStatus,name="student_status"),
    path('StudentProfile/',StudentProfile,name="StudentProfile"),

]