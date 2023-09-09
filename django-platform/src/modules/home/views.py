from django.shortcuts import render, get_object_or_404

def index(request):        
        # return render(request, 'courses/index.html', {'response' : courses})
        return render(request, 'index.html')

def contact(request):        
        # return render(request, 'courses/index.html', {'response' : courses})
        return render(request, 'contact.html')