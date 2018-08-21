from django.shortcuts import render,redirect,HttpResponse
from . models import *
from django.contrib import messages
import bcrypt
import calendar
from datetime import datetime
from django.conf import settings
from django.conf.urls.static import static
from django.core.files.storage import FileSystemStorage


def index(request):
    # print("BASE DIR", BASE_DIR)
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=int(request.session['ID']))
        }
        return render(request,'ChiesCakesApp/index.html',context)
    else:
        return render(request,'ChiesCakesApp/index.html')

def flavors(request):
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=int(request.session['ID'])),
            'flavors':Flavors.objects.all().order_by('flavor')
        }
        print(Flavors.objects.count())
        return render(request,'ChiesCakesApp/flavors.html', context)
    else:
        context={
            'flavors':Flavors.objects.all().order_by('flavor')
        }
        print(Flavors.objects.count())
        return render(request,'ChiesCakesApp/flavors.html', context)
    
def gallery(request):
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=int(request.session['ID']))
        }
        return render(request,'ChiesCakesApp/gallery.html', context)
    else:
        return render(request,'ChiesCakesApp/gallery.html')
    
def book(request):
    months={}
    month=datetime.now().month
    year=datetime.now().year
    # allReservations=Reservations.objects.filter(event_date)
    if request.method == 'POST':
        month=int(request.POST['hdnMonth'])
        # print(month)
        for i in range(datetime.now().month,13):
            months[str(i)]=datetime(datetime.now().year,i,1).strftime('%B')
    else:
        for i in range(datetime.now().month,13):
            months[str(i)]=datetime(datetime.now().year,i,1).strftime('%B')
    # print(month)
    # print(months)
    # print(calendar.monthcalendar(datetime.now().year,month))
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=int(request.session['ID'])),
            'calMonth':calendar.monthcalendar(datetime.now().year,month),
            'months':months,
            'selectedMonth':month,
            'thisDay':datetime.now().day,
            'thisMonth':datetime.now().month,
            'monthName':datetime(datetime.now().year,month,1).strftime('%B'),
            'year':datetime.now().year
        }
    else:
        context={
            'calMonth':calendar.monthcalendar(datetime.now().year,month),
            'months':months,
            'selectedMonth':month,
            'thisDay':datetime.now().day,
            'thisMonth':datetime.now().month,
            'monthName':datetime(datetime.now().year,month,1).strftime('%B'),
            'year':year
        }
    return render(request,'ChiesCakesApp/book.html',context)
    
def reserve(request,day,month):
    if 'ID' in request.session:
        user=Users.objects.get(id=int(request.session['ID']))
        edit=False
        context={}
        if user.reserves.count() > 0:
            # print("you have reservations")
            for reserved in user.reserves.all():
                # print(reserved.event_date.day==int(day))
                # print(day)
                if reserved.event_date.day == int(day) and reserved.event_date.month == int(month) and reserved.event_date.year == datetime.now().year:
                    reservation=reserved
                    order=reserved.orders.get(order_by=user)
                    edit=True
                    
                    context={
                        'user':user,
                        'monthName':datetime(datetime.now().year,int(month),int(day)).strftime('%B'),
                        'month':month,
                        'day':day,
                        'year':str(datetime.now().year),
                        'edit':edit,
                        'reservation':reservation,
                        'order':order
                    }
                    # print("ready for edit")
                    return render(request,'ChiesCakesApp/editReservation.html',context)

        if not edit:
            context={
                'user':user,
                'monthName':datetime(datetime.now().year,int(month),int(day)).strftime('%B'),
                'month':month,
                'day':day,
                'year':str(datetime.now().year),
                'edit':edit
            }

        return render(request,'ChiesCakesApp/reservation.html',context)
    else:
        return redirect('/register')

def process(request):
    if 'ID' in request.session:
        if request.method == 'POST':
            date=datetime.strptime(request.POST['hdnDate'],'%m/%d/%Y')
            user=Users.objects.get(id=int(request.session['ID']))
            reservation=Reservations.objects.create(eventType=request.POST['txtEvent'],location=request.POST['txtLoc'],event_date=date,event_by=user)
            order=Orders.objects.create(orderType=request.POST['drpOrder'],description=request.POST['txtDesc'],celebrant=request.POST['txtCeleb'],order_by=user,event=reservation)
            print(reservation)
            print(order)
        else:
            print(request.method)
        return redirect('/book')
    else:
        return redirect('/register')

def editProcess(request,day,month):
    if 'ID' in request.session:
        if request.method == 'POST':
            user=Users.objects.get(id=int(request.session['ID']))
            date=datetime.strptime(request.POST['hdnDate'],'%m/%d/%Y')
            for reserved in user.reserves.all():
                if reserved.event_date.day == int(day) and reserved.event_date.month == int(month) and reserved.event_date.year == datetime.now().year:
                    print("saving edits")
                    reservation=reserved
                    order=reserved.orders.get(order_by=user)
                    reservation.eventType=request.POST['txtEvent']
                    reservation.location=request.POST['txtLoc']
                    reservation.event_date=date
                    order.orderType=request.POST['drpOrder']
                    order.description=request.POST['txtDesc']
                    order.celebrant=request.POST['txtCeleb']
                    reservation.save()
                    order.save()
    
    return redirect('/book')

def contacts(request):
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=int(request.session['ID']))
        }
        return render(request,'ChiesCakesApp/contacts.html', context)
    else:
        return render(request,'ChiesCakesApp/contacts.html')

def reviews(request):
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=int(request.session['ID'])),
            'reviews':Reviews.objects.all().order_by('-created_at'),
            'rates':[1,2,3,4,5],
            'uploaded_file_url':'media/locate.jpg'
        }
        return render(request,'ChiesCakesApp/reviews.html',context)
    else:
        context={
            'reviews':Reviews.objects.all().order_by('-created_at'),
            'rates':[1,2,3,4,5],
            'uploaded_file_url':'media/locate.jpg'
        }
        return render(request,'ChiesCakesApp/reviews.html',context)
    
def post_review(request):
    if 'ID' in request.session:
        errors = {}
        if request.method == 'POST':
            filepath = request.FILES.get('myCake', False)

            if filepath:
                errors=Reviews.objects.review_validator(request.POST)
                if len(errors)==0:
                    myCake = request.FILES['myCake']
                    fs = FileSystemStorage()
                    filename = fs.save(myCake.name, myCake)
                    uploaded_file_url = fs.url(filename)
            
                    user=Users.objects.get(id=int(request.session['ID']))
                    review = Reviews.objects.create(img_url=uploaded_file_url,review=request.POST['txtReview'],rating=request.POST['hdnRating'],review_by=user)
                else:
                    for key,value in errors.items():
                        messages.error(request,value,key)
            else:
                errors['noFile']="Please select a picture of your cake."
                for key,value in errors.items():
                    messages.error(request,value,key)

            return redirect('/reviews', )
    else:
        return redirect('/register')

def register(request):
    if 'ID' in request.session:
        return redirect('/')
    else:
        return render(request,'ChiesCakesApp/register.html')
    
def newuser(request):
    if request.method=='POST':
        errors=Users.objects.registration_validator(request.POST)
        if len(Users.objects.filter(email_address=request.POST['txtEmail']))>0:
            errors['dupEmail']="duplicate email detected."
        
        if len(errors):
            for key,value in errors.items():
                messages.error(request,value,key)
                # print(key)
            return redirect('/register')
        else:
            password=request.POST['txtPWord']
            pwHash=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
            print(pwHash)
            Users.objects.create(first_name=request.POST['txtFirst'],last_name=request.POST['txtLast'],email_address=request.POST['txtEmail'],password=pwHash)

            user=Users.objects.get(email_address=request.POST['txtEmail'])
            request.session['ID']=user.id

    return redirect('/')

def login(request):
    validator=Users.objects.login_validator(request.POST)
    if 'ID' not in validator:
        for key,value in validator.items():
            messages.error(request,value,key)
            print(key)
        return redirect('/register')
    else:    
        request.session['ID']=validator['ID']
        return redirect('/')

def logout(request):
    if 'ID' in request.session:
        del request.session['ID']
    
    return redirect('/')
