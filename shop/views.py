from django.shortcuts import render, redirect
from sell.models import Image
from sell.forms import ImageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Order, OrderItems
from django.db.models import Sum


# Create your views here.

def welcome(request):
    return render(request, 'welcome.html')

def about(request):
    return render(request, 'about.html')

def gallery(request):
    all_images = Image.objects.filter(status='for-sale')
    return render(request, 'gallery.html', context={'images': all_images})

def image_info(request, id):
    image = Image.objects.get(id=id)
    return render(request, 'image_info.html', {'image': image})

@login_required()
def add_to_cart(request, id):
    order, created = Order.objects.get_or_create(finalized=False, buyer=request.user)
    image = Image.objects.get(id=id)
    image.status='in-cart'
    image.save()
    item, created = OrderItems.objects.get_or_create(item=image, order=order)
    return redirect('cart')

@login_required()
def cart(request):
    order, created = Order.objects.get_or_create(finalized=False, buyer=request.user)
    for orderitem in order.items.all():
        if orderitem.item.status != 'in-cart':
            orderitem.item.delete()
    total = order.items.aggregate(Sum('item__price'))
    return render(request, 'cart.html', {'order':order, 'total':total['item__price__sum']})

@login_required()
def remove_item(request, id):
    item = OrderItems.objects.get(id=id)
    item.image.status = 'for-sale'
    item.image.save()
    item.delete()
    return redirect('cart')


@login_required()
def order_list(request):
    orders = Order.objects.filter(finalized='True', buyer=request.user)
    return render(request, 'order_list.html', {'orders':orders})

@login_required()
def order(request,id):
    items = Order.objects.get(id=id)
    total = items.items.aggregate(Sum('item__price'))
    return render(request, 'order.html', {'items':items, 'total':total['item__price__sum']})

@login_required()
def buy(request, id):   
    order = Order.objects.get(id=id)
    for orderitem in order.items.all():
        image = orderitem.item
        image.status='sold'
        image.save()
        email_seller(request, image)
    order.finalized='True'
    order.save()
    email_buyer(request, order)
    messages.success(request, f'Your order has gone through. You will be receiving email confirmation shortly.')
    return redirect('gallery')

@login_required()
def delete(request, id):
    image = Image.objects.get(id=id)
    if request.user == image.seller:
        image.delete()
    else:
        messages.warning(request, f"You do not have permission to delete this image.")
    return redirect('gallery')
    
@login_required()
def admin_flag(request, id):
    image = Image.objects.get(id=id)
    if request.user.is_superuser:
        image.status = 'flagged'
        image.save()
        subject = f'Your image, {image.title}, has been flagged.'
        message = f'You image, {image.title}, has been flagged by admin as inappropriate. If you would like to edit or delete your image, please got to Flagged Images'
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [image.seller.email,]
        send_mail( subject, message, email_from, recipient_list) 
        messages.success(request, f'You have flagged "{image.title}". An email notice will be send to the seller.')
        return redirect('gallery')
    else:
        messages.warning(request, f"You do not have permission to edit this image.")
        return redirect('gallery')


@login_required()
def edit(request, id):
    image = Image.objects.get(id=id)
    if request.user == image.seller:
        if request.method == 'POST':
            form = ImageForm(request.POST, instance=image)
            if form.is_valid():
                form.save()
                messages.success(request, f"Your image's changes have been updated.")
                return redirect('gallery')

        else:
            form = ImageForm(instance=image)
            return render(request, 'edit_image.html', {'form': form})
    else:
        messages.warning(request, f"You do not have permission to edit this image.")
        return redirect('gallery')

        
def email_buyer(request, order):

    subject = f'Your Order #{order.id}'
    message = f'Thank you for purchasing at ArtSellNShop. Your order number is {order.id}.'
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [request.user.email,]
    send_mail( subject, message, email_from, recipient_list) 
    return

def email_seller(request, image):
    seller = image.seller
    subject = f'Your Artwork has been sold!'
    message = f'Thank you for using ArtSellNShop. Your artwork {image.title} has been purchased by {request.user}. Buyers contact email is {request.user.email}'
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [seller.email,]
    send_mail( subject, message, email_from, recipient_list) 
    return

@login_required()
def flagged_images(request):
    if request.user.is_superuser:
        flagged_images = Image.objects.filter(status='flagged')   
    else:
        flagged_images = Image.objects.filter(seller=request.user,status='flagged')
    return render(request, 'flagged_images.html', context={'images': flagged_images})



@login_required()
def remove_flag(request, id):
    if request.user.is_superuser:
        image = Image.objects.get(id=id)
        image.status = 'for-sale'
        image.save()
        subject = f"Your image, {image.title}, has been unflagged."
        message = f"Your image, {image.title}, has been unflagged and returned to gallery." 
        email_from = settings.EMAIL_HOST_USER 
        recipient_list = [image.seller.email,]
        send_mail( subject, message, email_from, recipient_list)
        messages.success(request, f'{image.title}" has been unflagged.')
        return redirect('flagged_images')
    else:
        messages.warning(request, f"You do not have permission to edit this image.")
        return redirect('gallery')

