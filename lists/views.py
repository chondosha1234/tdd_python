from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm

User = get_user_model()

# Create your views here.
def home_page(request):
    form = ItemForm()
    context = {
        'form': form,
    }
    return render(request, 'home.html', context)

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_) # uses get absolute url from model

    context = {
        'list': list_,
        'form':form,
    }
    return render(request, 'list.html', context)

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List()
        list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form}) #form has error message


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})
