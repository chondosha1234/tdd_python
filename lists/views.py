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
    error = None

    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_) # uses get absolute url
        except ValidationError:
            item.delete()
            error = "You can't have an empty list item"

    context = {
        'list': list_,
        'error': error,
    }
    return render(request, 'list.html', context)

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(list_)  # uses get absolute url method
