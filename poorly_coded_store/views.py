from django.shortcuts import redirect, render
from .models import Order, Product
from django.db.models import Count, Sum, Min, Max, Avg

def index(request):
    context = {
        "all_products": Product.objects.all(),
    }
    return render(request, "store/index.html", context)

def process(request):
    this_product= Product.objects.get(id= int(request.POST['product_id']))
    quantity = int(request.POST["quantity"])
    product_price= float(this_product.price)
    total_charge = quantity * product_price
    Order.objects.create(quantity_ordered= quantity, total_price=total_charge)
    return redirect('/checkout')

def checkout(request):
    all_items= Order.objects.aggregate(Sum('quantity_ordered'))['quantity_ordered__sum']
    all_cost= Order.objects.aggregate(Sum('total_price'))['total_price__sum']
    cost= round(all_cost, 2)
    context={
        'items': all_items,
        'last_order':Order.objects.last(),
        'total_cost': cost,
    }
    return render(request, 'store/checkout.html', context)