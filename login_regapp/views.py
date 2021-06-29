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
        request.session["id"] = user.id
        request.session["name"] = user.first_name
        request.session["email"] = user.email
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
    request.session["id"] = user[0].id
    request.session["name"] = user[0].first_name
    request.session["email"] = user[0].email
    return redirect("/pass")

def logout(request):
    request.session.clear()
    return redirect("/")

def inpage(request):  
    if  request.session["logged"] != 1:
        return redirect("/") 
    id = Userreg.objects.filter(email = request.session["email"])
    id2 = id[0].id
    context ={
        "identifier" : id2,
        "tobedeleted" : Userreg.objects.all()
    }
    if request.session["logged"] != 1:
        return redirect('/')
    return render(request, "pass.html", context)

# def properties(request):
#     if "logged" not in request.session:
#         return redirect('/')
#     user = Userreg.objects.create(
#     address_number = request.POST['Hi_MY_name_is_error'],
#     street = request.POST['street'],
#     city = request.POST[' city'],
#     state  = request.POST['state'],
#     zip_code  = request.POST['zip_code'],
#     home_type  = request.POST['home_type'],
#     creator  =  Userreg.objects.get(id = request.session["id"] )
#     )       
    
#     return render(request, "properties_all.html")

def create_property(request):
    if "logged" not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Property.objects.property_validator(request.POST)
        if len(errors) > 0:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/pass')
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
            return redirect('/pass')

def property_detail(request, property_id):
    if "logged" not in request.session:
        return redirect('/')
    property_with_id = Property.objects.filter(id=property_id)
    if len(property_with_id) == 0:
        return redirect('/pass')
    context = {
        "current_user" : Userreg.objects.get(email=request.session["email"]),
        "one_property" : Property.objects.get(id=property_id),
    }
    return render(request, "property_detail.html", context)

def delete_property(request, property_id):
    if "logged" not in request.session:
        return redirect('/')
    property_with_id = Property.objects.filter(id=property_id)
    if len(property_with_id) == 0:
        return redirect('/pass')
    if request.method == "POST":
        property_to_delete = Property.objects.get(id=property_id)
        if property_to_delete.creator.email == request.session['email']:
            property_to_delete.delete()
    return redirect('/pass')

def all_properties(request, id):
    #generates a list of all your properties 
    creator_properties = Property.objects.filter(creator = Userreg.objects.get(id = id))
    
    
    context = {
        "all_my_properties" : creator_properties        
    }

    return render ( request,"property_detail.html", context)


def like_property(request, property_id):
    if "logged" not in request.session:
        return redirect('/')
    if request.method == "POST":
        one_property = Property. objects.get(id=property_id)
        current_user = Userreg.objects.get(email=request.session['email'])
        one_property.users_that_like.add(current_user)
    return redirect(f'/property/{one_property.id}')

def unlike_property(request, property_id):
    if "logged" not in request.session:
        return redirect('/')
    if request.method == "POST":
        one_property = Property. objects.get(id=property_id)
        current_user = Userreg.objects.get(email=request.session['email'])
        one_property.users_that_like.remove(current_user)
    return redirect(f'/property/{one_property.id}')
