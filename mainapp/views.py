from django.shortcuts import render
from .models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    context = {
        'title': 'geekshop',
    }
    return render(request, 'mainapp/index.html', context)

def products(request, category_id=None, page=1):
    context = {'title': 'Geekshop - каталог',
                'categories' : ProductCategory.objects.all()}
    products = Product.objects.filter(category=category_id) if category_id else Product.objects.all()
    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context.update({'products': products_paginator})
    return render(request, 'mainapp/products.html', context)
