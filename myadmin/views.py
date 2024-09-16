from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from myadmin.models import *
from user.models import *
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from datetime import date
from django.contrib.auth.models import User
from django.contrib import auth,messages
import pdfplumber
import PyPDF2

def layout(request):
    context = {}
    return render(request,'myadmin/common/layout.html',context)

def dashboard(request):
    context = {}
    return render(request,'myadmin/dashboard.html',context)

# Login Crud
def login(request):
    context = {}
    return render(request,'myadmin/login.html',context)

def login_check(request):
	myusername  = request.POST['username']
	mypassword  = request.POST['password']

	result = auth.authenticate(username=myusername,password=mypassword)
	if result is None:
		messages.success(request,"Invaild username and password😅")
		return redirect('/myadmin/login')	
	else:
		auth.login(request,result)
		return redirect('/myadmin/dashboard')

# Logout
def logout(request):
	auth.logout(request)
	return redirect('/myadmin/login')

# State Crud
def add_state(request):
    context = {}
    return render(request,'myadmin/add_state.html',context)

def insert_state(request):
    mystatename =  request.POST['state_name']

    State.objects.create(state_name = mystatename)
    return(redirect('/myadmin/add_state'))

def all_state(request):
    result = State.objects.all()
    context = {'result' : result}
    return render(request,'myadmin/all_state.html',context)

def del_state(request,id):
    result = State.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/all_state')

def edit_state(request,id):
    result = State.objects.get(pk=id)
    context = {'result' : result}
    return render(request,'myadmin/edit_state.html',context)

def update_state(request,id):
    mystatename =  request.POST['state_name']

    data = {
        'state_name' : mystatename
    }
    State.objects.update_or_create(pk=id,defaults=data)
    return redirect('/myadmin/all_state')


# City Crud
def add_city(request):
    result = State.objects.all()
    context = {'result' : result}
    return render(request,'myadmin/add_city.html',context)

def all_city(request):
    result = City.objects.all()
    context = {'result' :result}
    return render(request,'myadmin/all_city.html',context)

def insert_city(request):
	result=State.objects.all()

	mycity=request.POST['city_name']
	mysid=request.POST['state']

	City.objects.create(city_name=mycity,state_id=mysid)
	return redirect('/myadmin/add_city')

def del_city(request,id):
    result = City.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/all_city')

def edit_city(request,id):
	result = City.objects.get(pk=id)
	result1 = State.objects.all()
	context={'result':result,'result1':result1}
	return render(request,'myadmin/edit_city.html',context)

def update_city(request,id):
	result=State.objects.all()
	mycity=request.POST['city_name']
	mystate=request.POST['state']

	data={
			'city_name':mycity,
			'state_id':mystate,
	    }
	City.objects.update_or_create(pk=id,defaults=data)
	return redirect('/myadmin/all_city')


# Area Crud
def add_area(request):
    city = City.objects.all()
    state = State.objects.all()
    context = {'city' : city,'state':state}
    return render(request,'myadmin/add_area.html',context)

def insert_area(request):
     myarea = request.POST['area_name']
     mycity = request.POST['city']
     mystate = request.POST['state']

     Area.objects.create(area_name=myarea,city_id=mycity,state_id=mystate)
     return redirect('/myadmin/add_area')

def all_area(request):
    result = Area.objects.all()
    context = {'result' : result}
    return render(request,'myadmin/all_area.html',context)

def del_area(request,id):
     result= Area.objects.get(pk=id)
     result.delete()
     return redirect('/myadmin/all_area')

def edit_area(request,id):
     result = Area.objects.get(pk=id)
     result1 = City.objects.all()
     result2 = State.objects.all()

     context = {'result':result,'result1':result1,'result2':result2}
     return render(request,'myadmin/edit_area.html',context)

def update_area(request,id):
    result=City.objects.all()
    myarea = request.POST['area_name']
    mycid = request.POST['city']
    mysid = request.POST['state']

    data={
            'area_name':myarea,
            'city_id':mycid,
            'state_id':mysid

    }
    Area.objects.update_or_create(pk=id,defaults=data)
    return redirect('/myadmin/all_area')

#User Crud
def user(request):
    result = Register.objects.all()
    context = {'result':result}
    return render(request,'myadmin/user.html',context)

def view_user(request,id):
    result = Register.objects.get(pk=id)
    context = {'result':result}
    return render(request,'myadmin/view_user.html',context)

def verify(request,id):
    #  id = request.session['id']
    #  mystatus = request.POST['status']
     data = {
          'status':'Verify'
     }
     Register.objects.update_or_create(pk=id, defaults=data)
     context = {}
     return redirect('/myadmin/user')

#Notic Crud
def add_notice(request):
    context = {}
    return render(request,'myadmin/add_notice.html',context)

def insert_notice(request):
    mytitle = request.POST['title']
    mydescription = request.POST['description']
    mydate = date.today()
    mypdf = request.FILES['pdf']

    #folder store
    mylocation = os.path.join(settings.MEDIA_ROOT, 'upload')
    obj = FileSystemStorage(location=mylocation)
    obj.save(mypdf.name, mypdf)

    Notice.objects.create(title=mytitle,description=mydescription,date=mydate,pdf=mypdf.name)
    return redirect('/myadmin/add_notice')

# def view_pdf(request, id):
#     document = get_object_or_404(Notice, pk=id)
#     pdf_file = document.pdf

#     # Open the PDF file
#     try:
#         with open(pdf_file) as file:
#             reader = PyPDF2.PdfFileReader(file)
#             number_of_pages = reader.numPages
#             text = ''

#             # Extract text from each page
#             with pdfplumber.open(pdf_file) as pdf:
#                 for page in pdf.pages:
#                     text += page.extract_text()

#         return HttpResponse(text, content_type='text/plain')
#     except FileNotFoundError:
#         return HttpResponse('File not found', status=404)
#     except Exception as e:
#         return HttpResponse(f'An error occurred: {str(e)}', status=500)
    
    
def all_notice(request):
    result = Notice.objects.all()
    context = {'result' : result}
    return render(request,'myadmin/all_notice.html',context)

def del_notice(request,id):
     result= Notice.objects.get(pk=id)
     result.delete()
     return redirect('/myadmin/all_notice')

def edit_notice(request,id):
     result = Notice.objects.get(pk=id)

     context = {'result':result}
     return render(request,'myadmin/edit_notice.html',context)

def update_notice(request,id):
    mytitle =  request.POST['title']
    mydescription =  request.POST['description']
    mydate =  date.today()
    mypdf =  request.FILES['pdf']

    #folder store
    mylocation = os.path.join(settings.MEDIA_ROOT, 'upload')
    obj = FileSystemStorage(location=mylocation)
    obj.save(mypdf.name, mypdf)


    data = {
            'title':mytitle,
            'description':mydescription,
            'date':mydate,
            'pdf':mypdf

    }

    Notice.objects.update_or_create(pk=id,defaults=data)
    return redirect('/myadmin/all_notice')

#Contact Crud
def all_contact(request):
    result = Contact.objects.all()
    context = {'result':result}
    return render(request,'myadmin/all_contact.html',context)

def del_contact(request,id):
    result = Contact.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/all_contact')
