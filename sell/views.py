from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import Image
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required()
def image_upload_view(request):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.seller = request.user
            img_obj = new_form.save()
            messages.success(request, f'Your image "{new_form.title}" was successfully added to gallery') 
            return render(request, 'index.html', {'form': form})
        else:
            messages.error(request, 'Your image was not saved to gallery. Please try again.') 
            return redirect('upload')

    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})