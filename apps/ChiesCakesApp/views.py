from django.shortcuts import render,redirect,HttpResponse
from . models import *
from django.contrib import messages
import bcrypt
import calendar
import os
from datetime import datetime
from django.conf import settings
from django.conf.urls.static import static
from django.core.files.storage import FileSystemStorage



def index(request):
    # print("BASE DIR", BASE_DIR)
    if 'ID' in request.session:
        user = Users.objects.get(id=int(request.session['ID']))
        details = Carousel.objects.all()

        if user.access_type == 'admin':
            return redirect('/admin')

        context={
            'user':user,
            'details':details
        }

    else:
        details = Carousel.objects.all()
        context={
            'details':details
        }

    return render(request,'ChiesCakesApp/index.html',context)

def flavors(request):
    if 'ID' in request.session:
        user = Users.objects.get(id=int(request.session['ID']))

        if user.access_type == 'admin':
            return redirect('/adminFlavors')

        context={
            'user':user,
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
        user = Users.objects.get(id=int(request.session['ID']))
        details = Gallery.objects.all()
        
        if user.access_type == 'admin':
            return redirect('/adminGallery')

        context={
            'user':Users.objects.get(id=int(request.session['ID'])),
            'details':details
        }
        return render(request,'ChiesCakesApp/gallery.html', context)
    else:
        details = Gallery.objects.all()
        
        context={
            'details':details
        }
        return render(request,'ChiesCakesApp/gallery.html', context)
    
def book(request):
    months={}
    month=datetime.now().month
    year=datetime.now().year
    isAdmin = False

    if request.method == 'POST':
        month=int(request.POST['hdnMonth'])
        
        for i in range(datetime.now().month,13):
            months[str(i)]=datetime(datetime.now().year,i,1).strftime('%B')
    else:
        for i in range(datetime.now().month,13):
            months[str(i)]=datetime(datetime.now().year,i,1).strftime('%B')
            
    if 'ID' in request.session:
        user = Users.objects.get(id=int(request.session['ID']))
        reservations=user.reserves.all()

        if user.access_type == 'admin':
            isAdmin=True
            reservations=Reservations.objects.all()
            print('Reservations:', len(reservations))
            
        context={
            'user':user,
            'calMonth':calendar.monthcalendar(datetime.now().year,month),
            'months':months,
            'selectedMonth':month,
            'thisDay':datetime.now().day,
            'thisMonth':datetime.now().month,
            'monthName':datetime(datetime.now().year,month,1).strftime('%B'),
            'year':datetime.now().year,
            'isAdmin':isAdmin,
            'reservations':reservations
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

        if user.access_type == 'admin':
            return redirect('/admin/manage/reservations/' + day + '/' + month)

        if user.reserves.count() > 0:
            for reserved in user.reserves.all():
                if reserved.event_date.day == int(day) and reserved.event_date.month == int(month) and reserved.event_date.year == datetime.now().year:
                    reservation=reserved
                    order=reservation.orders.get(order_by=user)
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
            order=Orders.objects.create(orderType=request.POST['drpOrder'],description=request.POST['txtDesc'],celebrant=request.POST['txtCeleb'],contact_number=request.POST['txtNumber'],order_by=user,event=reservation)
            print(reservation)
            print(order)
        else:
            print(request.method)
        return redirect('/reservations')
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
    
    return redirect('/reservations')

def contacts(request):
    if 'ID' in request.session:
        user = Users.objects.get(id=int(request.session['ID']))

        # if user.access_type == 'admin':
        #     return redirect('/admin/contactus')

        context={
            'user':Users.objects.get(id=int(request.session['ID']))
        }
        return render(request,'ChiesCakesApp/contacts.html', context)
    else:
        return render(request,'ChiesCakesApp/contacts.html')

def reviews(request):
    if 'ID' in request.session:
        reviews = Reviews.objects.all().order_by('-created_at')
        context={
            'user':Users.objects.get(id=int(request.session['ID'])),
            'rates':[1,2,3,4,5],
            'reviews':reviews,
            'comments':Comments.objects.all().order_by('created_at'),
            'uploaded_file_url':'media/locate.jpg'
        }

        return render(request,'ChiesCakesApp/reviews.html',context)
    else:
        context={
            'reviews':Reviews.objects.all().order_by('-created_at'),
            'comments':Comments.objects.all(),
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
            return redirect('/reviews')

    else:
        return redirect('/register')

def post_comment(request):
    if 'ID' in request.session:
        errors=Comments.objects.comment_validator(request.POST)
        if len(errors)==0:
            user=Users.objects.get(id=int(request.session['ID']))
            review=Reviews.objects.get(id=int(request.POST['hdnReviewID']))
            comment=Comments.objects.create(comment=request.POST['txtComment'],comment_by=user,comment_in=review)
        else:
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

# Admin pages starts here

def adminHome(request):
    if "ID" in request.session:
        user = Users.objects.get(id=int(request.session['ID']))
        details = Carousel.objects.all()
        if user.access_type == 'admin':    
            context={
                'user':user,
                'details':details
            }
            return render(request,'ChiesCakesApp/adminHome.html',context)
        else:
            return redirect('/')
    else:
        return redirect('/')

def addCarouselItem(request):
    if "ID" in request.session:
        errors={}
        user = Users.objects.get(id=int(request.session['ID']))
        if request.method == 'POST':
            filepath = request.FILES.get('carouselItem', False)
            if filepath:
                errors = Carousel.objects.carousel_validator(request.POST)
                if len(errors)==0:
                    item_img = request.FILES['carouselItem']
                    print("item_img:", item_img)
                    fs = FileSystemStorage()
                    filename = fs.save(item_img.name,item_img)
                    uploaded_file_url = fs.url(filename)
                    carousel_item = Carousel.objects.create(img_url=uploaded_file_url,filename=filename,caption=request.POST['txtCaption'],context=request.POST['txtContext'])
                else:
                    for key,value in errors.items():
                        messages.error(request,value,key)
            else:
                errors['noFile']="Please select a picture. Preferrably 315x420 images."
                for key,value in errors.items():
                    messages.error(request,value,key)

        return redirect('/admin')
    else:
        return redirect('/')

def deleteCarouselItem(request,id):
    if request.method == 'GET':
        carousel_item = Carousel.objects.get(id=id)
        
        if deleteImage(carousel_item.filename):
            carousel_item.delete()

        return redirect('/admin')
    
def saveCarouselEdits(request):
    if "ID" in request.session:
        if request.method == 'POST':
            errors={}
            user = Users.objects.get(id=int(request.session['ID']))
            carousel_item = Carousel.objects.get(id=int(request.POST['hdnID']))
            request.session['carousel'] = carousel_item.id
            filepath = request.FILES.get('carouselItem', False)
            errors = Carousel.objects.edit_carousel_validator(request.POST)
            if filepath:
                deleteImage(carousel_item.filename)
                item_img = request.FILES['carouselItem']
                fs = FileSystemStorage()
                filename = fs.save(item_img.name,item_img)
                uploaded_file_url = fs.url(filename)
                carousel_item.img_url=uploaded_file_url
                carousel_item.filename=filename
            if len(errors) == 0:
                carousel_item.caption=request.POST['txtEditCaption']
                carousel_item.context=request.POST['txtEditContext']
                carousel_item.save()
                errors['saved'] = "Saved!"
        
            for key,value in errors.items():
                messages.error(request,value,key)
            
        return redirect('/admin')

def adminFlavors(request):
    if "ID" in request.session:
        user = Users.objects.get(id=int(request.session['ID']))
        flavors = Flavors.objects.all()
        if user.access_type == 'admin':
            context={
                'user':user,
                'flavors':flavors
            }
            return render(request,'ChiesCakesApp/adminFlavors.html',context)
        else:
            return redirect('/flavors')
    else:
        return redirect('/')

def addFlavorItem(request):
    if "ID" in request.session:
        errors={}
        user = Users.objects.get(id=int(request.session['ID']))
        if request.method == 'POST':
            filepath = request.FILES.get('flavorsItem', False)
            if filepath:
                errors = Flavors.objects.flavor_validator(request.POST)
                if len(errors)==0:
                    item_img = request.FILES['flavorsItem']
                    print("item_img:", item_img)
                    fs = FileSystemStorage()
                    filename = fs.save(item_img.name,item_img)
                    uploaded_file_url = fs.url(filename)
                    flavor_item = Flavors.objects.create(img_url=uploaded_file_url,filename=filename,flavor=request.POST['txtCaption'])
                else:
                    for key,value in errors.items():
                        messages.error(request,value,key)
            else:
                errors['noFile']="Please select a picture. Preferrably 315x420 images."
                for key,value in errors.items():
                    messages.error(request,value,key)

        return redirect('/adminFlavors')
    else:
        return redirect('/')

def deleteFlavorItem(request,id):
    if request.method == 'GET':
        flavor_item = Flavors.objects.get(id=id)
        
        if deleteImage(flavor_item.filename):
            flavor_item.delete()

        return redirect('/adminFlavors')

def saveFlavorEdits(request):
    if "ID" in request.session:
        if request.method == 'POST':
            errors={}
            user = Users.objects.get(id=int(request.session['ID']))
            flavor_item = Flavors.objects.get(id=int(request.POST['hdnID']))
            request.session['flavor'] = flavor_item.id
            filepath = request.FILES.get('flavorItem', False)
            errors = Flavors.objects.edit_flavor_validator(request.POST)
            if filepath:
                deleteImage(flavor_item.filename)
                item_img = request.FILES['flavorItem']
                fs = FileSystemStorage()
                filename = fs.save(item_img.name,item_img)
                uploaded_file_url = fs.url(filename)
                flavor_item.img_url=uploaded_file_url
                flavor_item.filename=filename
            if len(errors) == 0:
                flavor_item.flavor=request.POST['txtEditCaption']
                flavor_item.save()
                errors['saved'] = "Saved!"
        
            for key,value in errors.items():
                messages.error(request,value,key)
            
        return redirect('/adminFlavors')

def adminGallery(request):
    if "ID" in request.session:
        user = Users.objects.get(id=int(request.session['ID']))
        details = Gallery.objects.all()
        if user.access_type == 'admin':
            context={
                'user':user,
                'details':details
            }
            return render(request,'ChiesCakesApp/adminGallery.html',context)
        else:
            return redirect('/gallery')
    else:
        return redirect('/')

def addGalleryItem(request):
    if "ID" in request.session:
        user = Users.objects.get(id=int(request.session['ID']))
        if request.method == 'POST':
            filepath = request.FILES.get('flavorsItem', False)
            if filepath:
                item_img = request.FILES['flavorsItem']
                fs = FileSystemStorage()
                filename = fs.save(item_img.name,item_img)
                uploaded_file_url = fs.url(filename)
                gallery_item = Gallery.objects.create(img_url=uploaded_file_url,filename=filename,description="")
            else:
                errors['noFile']="Please select a picture. Preferrably 315x420 images."
                for key,value in errors.items():
                    messages.error(request,value,key)

        return redirect('/adminGallery')
    else:
        return redirect('/')

def deleteGalleryItem(request,id):
    if request.method == 'GET':
        gallery_item = Gallery.objects.get(id=id)
        
        if deleteImage(gallery_item.filename):
            gallery_item.delete()

        return redirect('/adminGallery')

def adminReservations(request,day,month):
    if 'ID' in request.session:
        user=Users.objects.get(id=int(request.session['ID']))
        
        reservations = Reservations.objects.filter(event_date=datetime(datetime.now().year,int(month),int(day)))
        print(len(reservations))
        print(user.reserves)

        for reservation in reservations:
            print(reservation.orders)

        context={
            'user':user,
            'monthName':datetime(datetime.now().year,int(month),int(day)).strftime('%B'),
            'month':month,
            'day':day,
            'year':str(datetime.now().year),
            'date':datetime(datetime.now().year,int(month),int(day)).strftime('%A %d, %B %Y'),
            'reservations':reservations
        }

        return render(request,'ChiesCakesApp/adminReservations.html',context)
        
    else:
        return redirect('/register')

def adminViewReservation(request,day,month,cid):
    if 'ID' in request.session:
        user=Users.objects.get(id=int(request.session['ID']))
        customer=Users.objects.get(id=int(cid))
        edit=False
        context={}

        if customer.reserves.count() > 0:
            for reserved in customer.reserves.all():
                if reserved.event_date.day == int(day) and reserved.event_date.month == int(month) and reserved.event_date.year == datetime.now().year:
                    reservation=reserved
                    order=reservation.orders.get(order_by=customer)
                    edit=False
                    
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
                    return render(request,'ChiesCakesApp/adminViewReservation.html',context)

    else:
        return redirect('/register')

def adminContactUs(request):
    if "ID" in request.session:
        user = Users.objects.get(id=int(request.session['ID']))
        if user.access_type == 'admin':
            context={
                'user':user
            }
            return render(request,'ChiesCakesApp/adminContactUs.html',context)
        else:
            return redirect('/contacts')
    else:
        return redirect('/')

def deleteImage(filename):
        orig_path = os.getcwd()
        media_path = os.getcwd() + '/media'
        os.chdir(media_path)
        isDeleted = False

        if os.path.exists(filename):
            os.remove(filename)
            isDeleted = True
            
        os.chdir(orig_path)
        return isDeleted

