from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from django.http import HttpResponse

# Create your views here.
def index(request , *args, **kwargs):
    
    mytodos= Todo.objects.all()
    template_name = 'frontend/index.html'
    context = {'todos': mytodos}
    return render(request, template_name, context)

def add(request):
    if request.method == 'POST':
        title = request.POST.get('title') 
        description = request.POST.get('description')

        if not title or not description:
            return HttpResponse('Title and description are required.', status=400)

        todo = Todo(title=title, description=description)
        todo.save()
        return redirect('todo_list')
    
    return render(request, 'frontend/add.html')


def update_todo(request, id):
    todo = get_object_or_404(Todo, id=id)
    if request.method == 'POST':
        todo.title = request.POST['title']
        todo.description = request.POST.get('description', '')
        todo.is_completed = 'is_completed' in request.POST
        todo.save()
        return redirect('todo_list')

    return render(request, 'frontend/update.html', {'todo': todo}) 

def delete(request, id):
    todo = get_object_or_404(Todo, id=id)
    todo.delete()
    return redirect('todo_list')