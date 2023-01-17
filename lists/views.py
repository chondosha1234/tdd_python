from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from lists.models import Item, List
from lists.forms import ItemForm

# Create your views here.
def home_page(request):
    form = ItemForm()
    context = {
        'form': form,
    }
    return render(request, 'home.html', context)

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    error = None

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_) # uses get absolute url from model

    context = {
        'list': list_,
        'form':form,
        'error': error
    }
    return render(request, 'list.html', context)

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form}) #form has error message
