from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from .bing_search import run_query
from .models import Category,Page
from .forms import CategoryForm,PageForm

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    return render_to_response('rango/index.html', context_dict)

def about(request):
    return render(request,"rango/about.html",{'context':'Rango says here is the about page.'})


def category(request,category_name_slug):
    context_dict={}

    try:
        category = Category.objects.get(slug = category_name_slug)
        context_dict['category_name'] = category.name


        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages

        context_dict['category'] = category
        context_dict['category_name_slug'] = category.slug

    except Category.DoesNotExist:
        pass
    return render(request,'rango/category.html',context_dict)

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request,'rango/add_category.html',{'form':form})
    

def add_page(request,category_name_slug):
    try:
        cat = Category.objects.get(slug = category_name_slug)
    except Exception:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
            else:
                print form.errors
    
    context_dict = {'form':form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)


def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})