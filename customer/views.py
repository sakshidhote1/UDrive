from pyexpat.errors import messages

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from djoser.conf import User
from .forms import *
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from cardealer.models import *

# Create your views here.
def index(request):
    return render(request,"index.html")

def aboutus(request):
    return render(request,"about-us.html")

def sendmailview1(request,email):
    subject = 'Registered Successfully'
    message = "Congratulations!!!  You are Successfully registred."
    email_from = settings.EMAIL_HOST_USER
    print(email)
    recipient_list = [email]
    sad = send_mail(subject, message, email_from, recipient_list)
    print(sad)
    return sad



def contactus(request):
    if request.method == "POST":
        form = contactusform(request.POST)
        if form.is_valid():
            try:
                form.save()
                print("save")
                print("**************************")
                uemail = request.data["email"]
                print("___________________________________________________________**********************")
                print(uemail)
                sendmailview1(request, uemail)
                return render(request,"contact.html",{"message":"Data Inserted Succssefully"})
            except:
                pass
    else:
        form = contactusform()
    return render(request,"contact.html",{"message":"Invalid Data"})


def login_failed(request):
    return render(request, 'login_failed.html')

def notapproved(request):
    return render(request, 'notapproved.html')

def customerreg(request):
    return render(request, 'customersignp.html')

def customersignup(request):


    success='Registered successfully !'
    dealererror='Username Already exist !'

    username = request.POST.get('username')
    password = request.POST.get('password')
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')

    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = firstname
        user.lastname = lastname
        user.email = email
        user.save()
    except:
        return render(request, 'customersignp.html',{'dealererror':dealererror})

    customer = tblcustomersignup(user=user, mobile=mobile)
    customer.save()
    user.save()

    return render(request, 'customersignp.html',{'success':success})


def customerlogin(request):
    error="Login Failed!"
    if request.user.is_authenticated:
        return render(request, 'customerdashboard.html')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username and password:
                user = authenticate(username=username, password=password)
                print(user)
                rawq = "select is_staff from auth_user where username = %s"
                lgarr = []
                lgarr.append(str(username))
                lst = User.objects.raw(rawq, lgarr)
                print(username + ":-     " + password)
                print(User.objects.filter(username=username, password=password))
                print(request.user.is_staff)
                if user is not None:
                    login(request, user)
                    print("#############################")
                    return render(request, 'customerdashboard.html')
                else:
                    return render(request, 'customerlogin.html',{'error':error})
            else:
                return render(request, 'customerlogin.html',{'error':error})
        else:
            return render(request, 'customerlogin.html')



@login_required(login_url=customerlogin)
def customerdashboard(request):
    return render(request, 'customerdashboard.html')

@login_required(login_url=customerlogin)
def search(request):
    return render(request, 'search.html')

@login_required(login_url=customerlogin)
def search_results(request):
    city = request.POST.get('city')
    vehicletype = request.POST.get('vehicletype')
    capacity = request.POST.get('capacity')
    # city = city.lower()
    vehicles_list = []
    area = Area.objects.filter(city = city)
    # area = Area.objects.filter(city = city)
    for a in area:
        vehicles = Vehicles.objects.filter(area = a, vehicletype = vehicletype,capacity=capacity)
        for car in vehicles:
            if car.is_available == True:
                return render(request,'search_results.html',{'vehicle_list':vehicles})
    request.session['vehicles_list'] = vehicles_list
    return render(request, 'search_results.html')


@login_required(login_url=customerlogin)
def rent_vehicle(request):
    id = request.POST['id']
    vehicle = Vehicles.objects.get(id = id)
    cost_per_day = int(vehicle.price)
    return render(request, 'confirmation.html', {'vehicle':vehicle, 'cost_per_day':cost_per_day})

@login_required(login_url=customerlogin)
def confirm(request):
    orderfail="Order Failed!!"
    ordersuccess="Order Completed!!"
    ordersuccessfull="Your vehicle order was successful !"
    vehicle_id = request.POST['id']
    username = request.user
    user = User.objects.get(username = username)
    days = request.POST['days']
    vehicle = Vehicles.objects.get(id = vehicle_id)
    if vehicle.is_available:
        car_dealer = vehicle.dealer
        rent = (int(vehicle.price))*(int(days))
        car_dealer.wallet += rent
        car_dealer.save()
        try:
            order = Orders(vehicle = vehicle, car_dealer = car_dealer, user = user, rent=rent, days=days)
            order.save()
        except:
            order = Orders.objects.get(vehicle = vehicle, car_dealer = car_dealer, user = user, rent=rent, days=days)
        vehicle.is_available = False
        vehicle.save()
        return render(request, 'confirmed.html', {'order':order,'ordersuccess':ordersuccess,'ordersuccessfull':ordersuccessfull})
    else:
        return render(request, 'confirmed.html', {'orderfail':orderfail})

@login_required(login_url=customerlogin)
def manage(request):
    order_list = []
    user = User.objects.get(username = request.user)
    try:
        orders = Orders.objects.filter(user = user)
    except:
        orders = None
    if orders is not None:
        for o in orders:
            if o.is_complete == False:
                order_dictionary = {'id':o.id,'rent':o.rent, 'vehicle':o.vehicle, 'days':o.days, 'car_dealer':o.car_dealer}
                order_list.append(order_dictionary)
    return render(request, 'managecustomer.html', {'od':order_list})

@login_required(login_url=customerlogin)
def update_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    vehicle = order.vehicle
    vehicle.is_available = True
    vehicle.save()
    car_dealer = order.car_dealer
    car_dealer.wallet -= int(order.rent)
    car_dealer.save()
    order.delete()
    cost_per_day = int(vehicle.capacity)*300
    return render(request, 'confirmation.html', {'vehicle':vehicle}, {'cost_per_day':cost_per_day})

@login_required(login_url=customerlogin)
def delete_order(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    car_dealer = order.car_dealer
    car_dealer.wallet -= int(order.rent)
    car_dealer.save()
    vehicle = order.vehicle
    vehicle.is_available = True
    vehicle.save()
    order.delete()
    return HttpResponseRedirect('/manage/')
