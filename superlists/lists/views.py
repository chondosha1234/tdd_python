from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

# Create your views here.
def home_page(request):
    context = {}
    return render(request, "home.html", context)

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    context = {
        'list': list_
    }
    print('inside view_list func')
    return render(request, "list.html", context)

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    print('inside new_list func')
    return redirect('/lists/%d/' % (list_.id))

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id))
