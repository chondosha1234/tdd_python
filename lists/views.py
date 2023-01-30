from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, NewListForm

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
    form = NewListForm(data=request.POST)
    if form.is_valid():
<<<<<<< HEAD
        list_ = form.save(owner=request.user)
        #return redirect(list_)
        return redirect(str(list_.get_absolute_url()))
    return render(request, 'home.html', {'form': form})
=======
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form}) #form has error message

>>>>>>> b62afb5ab45d6c72630b9fac52b266bbf8db3e39

def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})
