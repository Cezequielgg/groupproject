from .models import Userreg, Property
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
# Create your views here.
#validations 
def regandlogin(request):
    context ={
        "user_reg" : Userreg.objects.all()
    }
    request.session["logged"] = 0
    return render(request, "regpage.html", context)

def registration(request):
    errors = Userreg.objects.basic_validation(request.POST)
    if len(errors) > 0:          
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:   
        user = Userreg.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        print(user.password)
        request.session["logged"] = 1
        return redirect('/pass')

def login(request):
    count = 0
    context ={
        "log-in" : Userreg.objects.all()
    }
    user = Userreg.objects.filter(email = request.POST['email'])
    errors2 = Userreg.objects.basic_login(request.POST)
    if len(errors2) > 0:          
        for key, value in errors2.items():
            messages.error(request, value)            
        return redirect("/")
    request.session["logged"] = 1
    request.session["name"] = user[0].first_name
    request.session["email"] = user[0].email
    return redirect("/pass")

def logout(request):
    request.session.clear()
    return redirect("/")

def inpage(request):
    id = Userreg.objects.filter(email = request.session["email"])
    id2 = id[0]
    context ={
        "identifier" : id2,
        "tobedeleted" : Userreg.objects.all()
    }
    if request.session["logged"] != 1:
        return redirect('/')
    return render(request, "pass.html", context)

def properties(request):
    if "logged" not in request.session:
        return redirect('/')
    context = {
        "current_user" : Userreg.objects.get(),
        "all_properties" : Property.objects.all(),
    }
    return render(request, "properties_all.html", context)

def create_property(request):
    if "logged" not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Property.objects.post_validator(request.POST)
        if len(errors) > 0:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/thoughts')
        else:
            new_property = Property.objects.create(
                address_number = request.POST["address_number"],
                street = request.POST["street"],
                city = request.POST["city"],
                state =  request.POST["state"],
                zip_code =  request.POST["zip_code"],
                home_type =  request.POST["home_type"],
                creator = Userreg.objects.get(email=request.session["email"])
            )
            return redirect('/properties')

def property_detail(request):
    if "logged" not in request.session:
        return redirect('/')

def delete_property(request):
    if "logged" not in request.session:
        return redirect('/')

def like_property(request):
    if "logged" not in request.session:
        return redirect('/')

def unlike_property(request):
    if "logged" not in request.session:
        return redirect('/')
