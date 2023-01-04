from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/only_url')

    context = {}
    return render(request, "home.html", context)

def view_list(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, "list.html", context)
