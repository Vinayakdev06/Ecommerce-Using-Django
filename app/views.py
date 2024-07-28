from django.shortcuts import render, redirect
from django.views import View
from .models import Product
from django.template.defaultfilters import slugify
from .forms import CustomerRegistrationForm, CustomerProfileForm, Customer
from django.contrib import messages

def home(request):
    return render(request, "app/home.html")


def about(request):
    return render(request, "app/about.html")


def contact(request):
    return render(request, "app/contact.html")

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", {'product': product, 'title': title})

class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title__iexact=val)
        if product.exists():
            category = product[0].category
            titles = Product.objects.filter(category=category).values('title')
            return render(request, "app/category.html", {'product': product, 'title': titles})
        else:
            return render(request, "app/category.html", {'product': [], 'title': []})

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", {'product': product})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, "app/customerregistration.html", {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registered Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
            return render(request, 'app/customerregistration.html', locals())
 
class ProfileView(View):
       def get(self, request):
           form = CustomerProfileForm()
           return render(request, 'app/profile.html', locals())
       def post(self, request):
              form = CustomerProfileForm(request.POST)
              if form.is_valid():
                  user = request.user
                  name = form.cleaned_data['name']
                  locality = form.cleaned_data['locality']
                  city = form.cleaned_data['city']
                  mobile = form.cleaned_data['mobile']
                  state = form.cleaned_data['state']
                  zipcode = form.cleaned_data['zipcode']
                  
                  reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
                  reg.save()
                  messages.success(request, "Congratulations! Profile Save Successfully")
              else:
                  messages.warning(request, "Invalid Input Data")
          
              return render(request, 'app/profile.html', locals())
          
def address(request):
    add = Customer.objects.filter(user=request.user)   
    return render(request, 'app/address.html', locals())  
     
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals()) 
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
                  add = Customer.objects.get(pk=pk)
                  add.name = form.cleaned_data['name']
                  add.locality = form.cleaned_data['locality']
                  add.city = form.cleaned_data['city']
                  add.mobile = form.cleaned_data['mobile']
                  add.state = form.cleaned_data['state']
                  add.zipcode = form.cleaned_data['zipcode']
                  add.save()
                  messages.success(request, 'Congratulations! Profile Update SuccessFully')
        else:
            messages.warning(request, "Invalid Input Data")      
        return redirect("address")