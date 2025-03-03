from django.shortcuts import render

# Create your views here.
def load_file(request):
    return render(request, "collection_agency/base.html")
