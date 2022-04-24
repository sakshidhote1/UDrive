from django.shortcuts import render,HttpResponseRedirect
from djoser.conf import User
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from customer.models import *
# Create your views here.

def dealerreg(request):
    return render(request, 'signup.html')

def dealersignup(request):
    success='Registered successfully !'
    dealererror='Username Already exist !'
    username = request.POST.get('username')
    password = request.POST.get('password')
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    city = request.POST.get('city')
    # city = city.lower()
    pincode = request.POST.get('pincode')
    adharno = request.POST.get('adharno')

    try:
        user = User.objects.create_user(username = username, password = password, email = email)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
    except:
        return render(request, 'login.html',{'dealererror':dealererror})
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        car_dealer = CarDealer(car_dealer = user, mobile = mobile, area=area,adharno=adharno)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        car_dealer = CarDealer(car_dealer = user, mobile = mobile, area=area,adharno=adharno)
    car_dealer.save()
    return render(request, 'login.html',{'success':success})

def dealerlogin(request):
    return render(request, 'login.html')

def deleardashboard(request):
    return render(request, 'dealerdashboard.html')

def auth_view(request):
    error = "Login Failed!"
    notapproved= "Sorry ! Not Approved"
    if request.user.is_authenticated:
        return render(request, 'dealerdashboard.html')
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
                    if  user.is_staff:
                        login(request, user)
                        print("#############################")
                        return render(request, 'dealerdashboard.html')
                    else:
                        return render(request,'login.html',{'notapproved':notapproved})
                else:
                    return render(request, 'login.html',{'error':error})

            else:
                return render(request, 'login.html',{'error':error})
        else:
            # print("/??/////////////////////")
            return render(request, 'login.html')


@login_required(login_url=dealerlogin)
def add_vehicle(request):
    vehicle_name = request.POST['vehicle_name']
    vehicle_no = request.POST['vehicle_no']
    color = request.POST['color']
    cd = CarDealer.objects.get(car_dealer=request.user)
    insuranceno = request.POST['insuranceno']
    licenseno = request.POST['licenseno']
    rcno = request.POST['rcno']
    price = request.POST['price']
    vehicletype = request.POST['vehicletype']
    transmission = request.POST['transmission']
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']
    description = request.POST['description']
    capacity = request.POST['capacity']
    photo = request.FILES['photo']
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        car = Vehicles(vehicle_name=vehicle_name,vehicle_no=vehicle_no, color=color, dealer=cd, area = area,
                       insuranceno=insuranceno,licenseno=licenseno,rcno=rcno,price=price,vehicletype=vehicletype,
                       transmission=transmission,description = description, capacity=capacity,photo=photo)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        # car = Vehicles(vehicle_name=vehicle_name, color=color, dealer=cd, area = area,description=description, capacity=capacity)
        car = Vehicles(vehicle_name=vehicle_name,vehicle_no=vehicle_no, color=color, dealer=cd, area = area,
                       insuranceno=insuranceno,licenseno=licenseno,rcno=rcno,price=price,vehicletype=vehicletype,
                       transmission=transmission,description = description, capacity=capacity,photo=photo)
    car.save()
    return render(request, 'vehicle_added.html')

@login_required(login_url=dealerlogin)
def manage_vehicles(request):
    username = request.user
    user = User.objects.get(username = username)
    car_dealer = CarDealer.objects.get(car_dealer = user)
    vehicle_list = []
    vehicles = Vehicles.objects.filter(dealer = car_dealer)
    for v in vehicles:
        vehicle_list.append(v)
    return render(request, 'managedelear.html', {'vehicle_list':vehicle_list})

@login_required(login_url=dealerlogin)
def order_list(request):
    username = request.user
    user = User.objects.get(username = username)
    car_dealer = CarDealer.objects.get(car_dealer = user)
    orders = Orders.objects.filter(car_dealer = car_dealer)
    order_list = []
    for o in orders:
        if o.is_complete == False:
            order_list.append(o)
    return render(request, 'order_list.html', {'order_list':order_list})

@login_required(login_url=dealerlogin)
def complete(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    vehicle = order.vehicle
    order.is_complete = True
    order.save()
    vehicle.is_available = True
    vehicle.save()
    return HttpResponseRedirect('/order_list/')


@login_required(login_url=dealerlogin)
def history(request):
    user = User.objects.get(username = request.user)
    car_dealer = CarDealer.objects.get(car_dealer = user)
    orders = Orders.objects.filter(car_dealer = car_dealer)
    order_list = []
    for o in orders:
        order_list.append(o)
    return render(request, 'history.html', {'wallet':car_dealer.wallet, 'order_list':order_list})

@login_required(login_url=dealerlogin)
def delete(request, id):
    employee = Vehicles.objects.get(id=id)
    employee.delete()
    return HttpResponseRedirect("/manage_vehicles/")
