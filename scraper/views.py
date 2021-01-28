from django.shortcuts import render, redirect
from .forms import SearchForm, AddRecipeForm
from . import recipeScraper as rs
from .models import TempRecipe
from django.views.generic import ListView
# Create your views here.

#   

def index(request):
    form = SearchForm()
    context ={
        "form": form
    }
    
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data['search_keywords']
            sortby = form.cleaned_data['sort_method']
            links = rs.compileSearchUrl(keywords, sortby)
            TempRecipe.objects.all().delete()
            for key, value in links.items():
                recipe_title = links[key]['title']
                recipe_link = links[key]['link']
                recipe_img = links[key]['image']
                recipe_desc = links[key]['description']
              
                index_of_last_space = recipe_desc[:100].rindex(' ')
                recipe_snippet = recipe_desc[:index_of_last_space] + '...'
                
                
                TempRecipe.objects.create(title=recipe_title, link=recipe_link, desc=recipe_desc,
                                         img=recipe_img, snippet=recipe_snippet,selected=False)
                
        return redirect('results/')    

            
    return render(request, 'scraper/index.html' , context )

class ResultsList(ListView):
    form = AddRecipeForm()
    model = TempRecipe
    context_object_name = "temp_recipes"
    paginate_by = 20
    template_name = 'scraper/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        context["added"] = TempRecipe.objects.filter(selected = True)
        return context
    
    def post(self, request, *args, **kwargs):
        
        self.object = TempRecipe.objects.get(pk = request.POST.get("selected"))
        self.object.selected = True
        self.object.save()
        print(self.object.title)
        return super().get(request, *args, **kwargs)
        
    

def success(request):
    return render(request, 'scraper/success.html')