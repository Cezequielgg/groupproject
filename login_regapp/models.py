from django.db import models
import re	
import bcrypt

# Create your models here.
class Regvalidate(models.Manager):
    def basic_validation(request, postData):        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}   
        email_count = Userreg.objects.filter(email= postData['email'])       
        # add keys and values to errors dictionary for each invalid field
        if (postData['first_name']).isnumeric() == True:
            errors["first_name"] = "A Name cannot be numbers"
        if (postData['last_name']).isnumeric() == True:
            errors["last_name"] = "A Last name cannot be numbers"     
        if len(postData['first_name']) < 2:          
            errors["first_name"] = "Name should be at least 2 characters"
        if len(postData['last_name']) < 2:          
            errors["last_name"] = "Last name should be at least 2 characters"
        if postData['password'] != postData['password2']:
            errors["password"] = "Both password have to match"
        if not EMAIL_REGEX.match(postData['email']):        
            errors['email'] = ("Invalid email address!")          
        if email_count:
            errors['email_duplicate'] = ("email address is already in use")              
        return errors
    
    def basic_login(request, postData):
        user = Userreg.objects.filter(email = postData['email'])
        errors2 = {}  
        if len(user) == 0:
            errors2['username'] = ("This email address hasn't been register")
        else:
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                errors2['password'] = ("wrong password")           
        return errors2

class Userreg(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = Regvalidate() 

class PropertyManager(models.Manager):
    def property_validator(request, postData):
        errors = {}
        if (postData['address_number']).isnumeric() == False:
            errors["address_num"] = "Address number must be a number"
        if len(postData['address_number']) < 1:
            errors["address_length"] = "Address number must be at least 1 number long"
        if len(postData['street']) < 2:
            errors["street_length"] = "Street must be at least 2 characters long"
        if len(postData['city']) < 2:
            errors["city_length"] = "City must be at least 2 characters long"
        if len(postData['state']) > 2:
            errors["street_length"] = "Please use state abbreviation"
        if (postData['zip_code']).isnumeric() == False:
            errors["zipcode_number"] = "Zip code must be a number"
        if len(postData['zip_code']) != 5:
            errors["zip_code_length"] = "Zip code must be 5 character long"
        return errors

class Property(models.Model):
    address_number = models.IntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip_code = models.IntegerField()
    home_type = models.CharField(max_length=255)
    creator = models.ForeignKey(Userreg, related_name = "property_created", on_delete=models.CASCADE)
    users_that_liked = models.ManyToManyField(Userreg, related_name= "property_liked")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = PropertyManager()