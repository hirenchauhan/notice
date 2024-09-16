from django.shortcuts import render,redirect
from myadmin.models import *
from user.models import *
from django.contrib.auth.models import User
from django.contrib import auth,messages
from datetime import date
import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import FileResponse
import os
from django.utils.dateparse import parse_date
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

#PDF genrate

from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch 
from reportlab.lib.pagesizes import letter

def layout(request):
    context = {}
    return render(request,'user/layout.html',context)

# Login Crud
def login(request):
    context = {}
    return render(request,'user/login.html',context)

def login_check(request):
    if request.method == 'POST':
        myusername = request.POST.get('username')
        mypassword = request.POST.get('password')

        if not myusername or not mypassword:
            messages.error(request, "Username and password are required.")
            return redirect('/user/login')

        result = auth.authenticate(username=myusername, password=mypassword)
        if result is None:
            messages.error(request, "Invalid Username or Password 🤭")
            return redirect('/user/login')
        else:
            # Check user's status
            try:
                user_register = Register.objects.get(user=result)
                user_status = user_register.status  # Assuming user profile has a status field
                if user_status == 'Pending':
                    messages.error(request, "Your account is still pending approval.")
                    return redirect('/user/login')
                else:
                    auth.login(request, result)
                    return redirect('/user/layout')
            except Register.DoesNotExist:
                messages.error(request, "User profile does not exist.")
                return redirect('/user/login')
    else:
        return render(request, 'user/login.html') 
     
# Logout
def logout(request):
	auth.logout(request)
	return redirect('/user/login')

# User Registration Crud
def register(request):
    state = State.objects.all()
    city = City.objects.all()
    area = Area.objects.all()

    context = {'state':state,'city':city,'area':area}
    return render(request,'user/register.html',context)

def check_username(request,uname):
    if User.objects.filter(username=uname).exists():
        return False 
    else:
        return True    

def check_email(request,email):
    if User.objects.filter(email=email).exists():
        return False
    else:
        return True

def check_contact(request,contact):
    if Register.objects.filter(contact=contact).exists():
        return False
    else:
        return True
    
def store_register(request):
    myfirst_name = request.POST['fname']
    mylast_name = request.POST['lname']
    myemail = request.POST['email']
    myusername = request.POST['username']
    mypassword = request.POST['password']
    mycpassword = request.POST['cpassword']

    mycontact = request.POST['contact']
    mydob = request.POST['dob']
    mygender = request.POST['gender']
    myaddress = request.POST['address']
    mystate= request.POST['state']
    mycity= request.POST['city']
    myarea= request.POST['area']


    if mypassword == mycpassword and check_username(request,myusername) and check_email(request,myemail) and check_contact(request,mycontact):
        user = User.objects.create_user(first_name=myfirst_name,last_name=mylast_name,email=myemail,username=myusername,password=mypassword)
        Register.objects.create(contact=mycontact,dob=mydob,gender=mygender,address=myaddress,state_id=mystate,city_id=mycity,area_id=myarea,user_id=user.id)

        return redirect('/user/layout')
    else:
        if check_username(request,myusername) is False:
            messages.error(request,'UserName Already Exists...') 
            return redirect('/user/register')
        elif check_email(request,myemail) is False:
            messages.error(request,'Email Already Exists...') 
            return redirect('/user/register')
        elif check_contact(request,mycontact) is False:
            messages.error(request,'Contact Already Exists...') 
            return redirect('/user/register')
        
def notice(request):
    notice = Notice.objects.all()
    context = {'notice':notice}
    return render(request,'user/notice.html',context)

def search_view(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    result = []
    
    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        if start_date and end_date:
            notice = Notice.objects.filter(date__range=[start_date, end_date])
        else:
            notice = Notice.objects.none()  # or handle invalid dates differently
    else:
        notice = Notice.objects.all()
    print(f"Start Date: {start_date}, End Date: {end_date}, notice: {notice}")

    return render(request, 'user/notice.html', {'notice': notice, 'start_date': start_date, 'end_date': end_date})

    context = {}
def gen_pdf(request):
    # Get the start and end dates from the request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    result = []
    
    if start_date and end_date:
        try:
            # Convert strings to datetime objects
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            
            # Ensure the end_date includes the entire day by adding one day
            end_date += datetime.timedelta(days=1)

            # Filter Notice objects based on the 'date' field
            result = Notice.objects.filter(date__range=[start_date, end_date])
        except ValueError as e:
            print(f"Date conversion error: {e}")
    else:
        print("Start date or end date not provided")

    # Generate the PDF
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    
    # Table data with headers
    data = [['Title', 'Date', 'Description']]
    for notice in result:
        data.append([
            notice.title,
            notice.date.strftime('%Y-%m-%d'),  # Format date as needed
            notice.description
        ])
    
    # Create the table
    table = Table(data, colWidths=[doc.width/3.0]*3)

    # Apply style to the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 2, colors.black),
    ])
    table.setStyle(style)
    
    # Build the PDF
    elements = [table]
    doc.build(elements)
    
    # Save the PDF to a file
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='notice.pdf')

# Conatct Crud
def contact(request):
    return render(request,'user/contact.html',context)

def insert_contact(request):
     myname = request.POST['name']
     myemail = request.POST['email']
     mycontact = request.POST['contact']
     mymessage = request.POST['message']
     mydate = date.today()

     Contact.objects.create(name=myname,email=myemail,contact=mycontact,message=mymessage,date=mydate)
     return redirect('/user/contact')