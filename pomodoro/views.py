import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from pomodoro.models import TaskSheet, Task, InboxItem, Reflection, Pomodoro, Mark
from pomodoro.forms import TaskSheetForm, InboxItemForm, TaskForm, MarkForm

# task sheets

def active_sheet(request):
    active_sheet = TaskSheet.objects.get_current()
    if active_sheet is not None:
        response = HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': active_sheet.id}))
    else:
        response = HttpResponseRedirect(reverse('new_task_sheet'))
    return response

def close_task_sheet(request, task_sheet_id):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    if request.method == 'POST':
        task_sheet.closed = datetime.datetime.now()
    return HttpResponseRedirect(reverse('home'))

def task_sheets_index(request, template_name='pomodoro/task_sheets_index.html'):
    if request.method == 'GET':
        task_sheets = TaskSheet.objects.all()
        if request.is_ajax():
            response = HttpResponse(json.dumps([sheet.serialize() for sheet in task_sheets]))
        else:
            response =  render_to_response(
                    template_name,
                    {
                        'task_sheets': task_sheets,
                        },
                    context_instance=RequestContext(request),
                    )
    elif request.method == 'POST':
        form = TaskSheetForm(request.POST)
        if form.is_valid():
            task_sheet = form.save()
            if request.is_ajax():
                response = HttpResponse(json.dumps(task_sheet.serialize()))
            else:
                response =  HttpResponseRedirect(
                        reverse('task_sheet_detail', kwargs={'task_sheet_id': task_sheet.id}))
        else:
            # need to serialize form errors here
            response =  render_to_response(
                    'pomodoro/new_task_sheet.html',
                    {
                        'form': form,
                        },
                    context_instance=RequestContext(request),
                    )
    return response

def new_task_sheet(request, template_name='pomodoro/new_task_sheet.html'):
    if request.method == 'POST':
        return task_sheets_index(request)
    form = TaskSheetForm()
    return render_to_response(
            template_name,
            {
                'form': form,
                },
            context_instance=RequestContext(request),
            )

def task_sheet_detail(request, task_sheet_id, template_name='pomodoro/task_sheet_detail.html'):
    try:
        task_sheet = TaskSheet.objects.select_related().get(id=task_sheet_id)
    except TaskSheet.DoesNotExist:
        raise Http404('No TaskSheet matches the given query.')

    # retrieve details
    if request.method == 'POST':
        form = TaskSheetForm(request.POST, instance=task_sheet)
        # if form saves, return detail for saved resource
        if form.is_valid():
            task_sheet = form.save()
        # if save fails, go back to edit_resource page
        else:
            return render_to_response(
                    'pomodoro/edit_task_sheet.html',
                    {
                        'form': form,
                        'task_sheet': task_sheet,
                        },
                    context_instance=RequestContext(request),
                    )
    inbox_item_form = InboxItemForm()
    task_form = TaskForm()
    current_pomodoro = Pomodoro.objects.get_current()
    return render_to_response(
            template_name,
            {
                'task_sheet': task_sheet,
                'inbox_item_form': inbox_item_form,
                'task_form': task_form,
                'current_pomodoro': current_pomodoro,
                },
            context_instance=RequestContext(request),
            )

def edit_task_sheet(request, task_sheet_id, template_name='pomodoro/edit_task_sheet.html'):
    if request.method == 'POST':
        return task_sheet_detail(request, task_sheet_id)
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    form = TaskSheetForm(instance=task_sheet)
    return render_to_response(
            template_name,
            {
                'form': form,
                'task_sheet': task_sheet,
                },
            context_instance=RequestContext(request),
            )
def delete_task_sheet(request, task_sheet_id):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    if request.method == 'POST':
        task_sheet.delete()
        return HttpResponseRedirect(reverse('task_sheets_index'))
    
def complete_task(request, task_sheet_id, task_id):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    task = get_object_or_404(Task, task_sheet=task_sheet, id=task_id)
    if request.method == 'POST':
        task.completed = datetime.datetime.now()
        task.save()
    return HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': task_sheet.id }))
def tasks_index(request, task_sheet_id, template_name='pomodoro/tasks_index.html'):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    if request.method == 'GET':
        tasks = Task.objects.filter(task_sheet=task_sheet)
        return render_to_response(
                template_name,
                {
                    'task_sheet': task_sheet,
                    'tasks': tasks,
                    },
                context_instance=RequestContext(request),
                )
    elif request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_sheet = task_sheet
            task.save()
            return HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': task_sheet.id,}))
        else:
            template_name = 'pomodoro/new_task.html'
            return render_to_response(
                    template_name,
                    {
                        'form': form,
                        'task_sheet': task_sheet,
                        },
                    context_instance=RequestContext(request),
                    )

def new_task(request, task_sheet_id, template_name='pomodoro/new_task.html'):
    # Handle POST to new as a create request
    if request.method == 'POST':
        return tasks_index(request, task_sheet_id)
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    form = TaskForm()
    return render_to_response(
            template_name,
            {
                'form': form,
                'task_sheet': task_sheet,
                },
            context_instance=RequestContext(request),
            )
def task_detail(request, task_sheet_id, task_id, template_name='pomodoro/task_detail.html'):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    task = get_object_or_404(Task, id=task_id)
    # retrieve details
    if request.method == 'GET':
        return render_to_response(
                template_name,
                {
                    'task': task,
                    'task_sheet': task_sheet,
                    },
                context_instance=RequestContext(request),
                )
        # update existing resource
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        # if form saves, return detail for saved resource
        if form.is_valid():
            task = form.save()
            return render_to_response(
                    template_name,
                    {
                        'task': task,
                        'task_sheet': task_sheet,
                        },
                    context_instance=RequestContext(request),
                    )
            # if save fails, go back to edit_resource page
        else:
            return render_to_response(
                    'pomodoro/edit_task.html',
                    {
                        'form': form,
                        'task': task,
                        'task_sheet': task_sheet,
                        },
                    context_instance=RequestContext(request),
                    )

def edit_task(request, task_sheet_id, task_id, template_name='pomodoro/edit_task.html'):
    # if a POST is received, direct it to resource detail for update
    if request.method == 'POST':
        return task_detail(request, task_sheet_id, task_id)
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    task = get_object_or_404(Task, id=task_id)
    form = TaskForm(instance=task)
    return render_to_response(
            template_name,
            {
                'form': form,
                'task': task,
                'task_sheet': task_sheet,
                },
            context_instance=RequestContext(request),
            )
def delete_task(request, task_sheet_id, task_id):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': task_sheet.id}))
    


def inbox_item_done(request, inbox_item_id):
    inbox_item = get_object_or_404(InboxItem, id=inbox_item_id)
    if request.method == 'POST':
        inbox_item.dealt_with = datetime.datetime.now()
        inbox_item.save()
    return HttpResponseRedirect(reverse('home'))
def inbox_items_index(request, template_name='pomodoro/inbox_items_index.html'):
    if request.method == 'GET':
        inbox_items = InboxItem.objects.filter(dealt_with=False)
        return render_to_response(
                template_name,
                {
                    'inbox_items': inbox_items,
                    },
                context_instance=RequestContext(request),
                )
    elif request.method == 'POST':
        form = InboxItemForm(request.POST)
        if form.is_valid():
            inbox_item = form.save()
            # get current task_sheet
            task_sheet = TaskSheet.objects.get_current()
            if task_sheet:
                return HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': task_sheet.id,}))
            else:
                return HttpResponseRedirect(reverse('home'))
        else:
            template_name = 'pomodoro/new_inbox_item.html'
            return render_to_response(
                    template_name,
                    {
                        'form': form,
                        'task_sheet': task_sheet,
                        },
                    context_instance=RequestContext(request),
                    )

def new_inbox_item(request, template_name='pomodoro/new_inbox_item.html'):
    # Handle POST to new as a create request
    if request.method == 'POST':
        return inbox_items_index(request)
    form = InboxItemForm()
    return render_to_response(
            template_name,
            {
                'form': form,
                },
            context_instance=RequestContext(request),
            )
def inbox_item_detail(request, inbox_item_id, template_name='pomodoro/inbox_item_detail.html'):
    inbox_item = get_object_or_404(InboxItem, id=inbox_item_id)
    # retrieve details
    if request.method == 'GET':
        return render_to_response(
                template_name,
                {
                    'inbox_item': inbox_item,
                },
                context_instance=RequestContext(request),
            )
        # update existing resource
    elif request.method == 'POST':
        form = InboxItemForm(request.POST, instance=inbox_item)
        # if form saves, return detail for saved resource
        if form.is_valid():
            inbox_item = form.save()
            return render_to_response(
                    template_name,
                    {
                        'inbox_item': inbox_item,
                        },
                    context_instance=RequestContext(request),
                    )
            # if save fails, go back to edit_resource page
        else:
            return render_to_response(
                    'pomodoro/edit_inbox_item.html',
                    {
                        'form': form,
                        'inbox_item': inbox_item,
                        },
                    context_instance=RequestContext(request),
                    )

def edit_inbox_item(request, inbox_item_id, template_name='pomodoro/edit_inbox_item.html'):
    # if a POST is received, direct it to resource detail for update
    if request.method == 'POST':
        return inbox_item_detail(request, inbox_item_id)
    inbox_item = get_object_or_404(InboxItem, id=inbox_item_id)
    form = InboxItemForm(instance=inbox_item)
    return render_to_response(
            template_name,
            {
                'form': form,
                'inbox_item': inbox_item,
                },
            context_instance=RequestContext(request),
            )
def delete_inbox_item(request, task_sheet_id, inbox_item_id):
    inbox_item = get_object_or_404(InboxItem, id=inbox_item_id)
    task_sheet = TaskSheet.objects.get_current()
    if request.method == 'POST':
        inbox_item.delete()
        if task_sheet:
            return HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': task_sheet.id}))
        else:
            return HttpResponseRedirect(reverse('home'))


def reflections_index(request, task_sheet_id, template_name='pomodoro/reflections_index.html'):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    if request.method == 'GET':
        reflections = Reflection.objects.filter(task_sheet=task_sheet)
        return render_to_response(
                template_name,
                {
                    'task_sheet': task_sheet,
                    'reflections': reflections,
                    },
                context_instance=RequestContext(request),
                )
    elif request.method == 'POST':
        form = ReflectionForm(request.POST)
        if form.is_valid():
            reflection = form.save(commit=False)
            reflection.task_sheet = task_sheet
            reflection.save()
            return HttpResponseRedirect(reverse('reflection_detail', kwargs={'task_sheet_id': task_sheet.id, 'reflection_id': reflection.id}))
        else:
            template_name = 'pomodoro/new_reflection.html'
            return render_to_response(
                    template_name,
                    {
                        'form': form,
                        'task_sheet': task_sheet,
                        },
                    context_instance=RequestContext(request),
                    )

def new_reflection(request, task_sheet_id, template_name='pomodoro/new_reflection.html'):
    # Handle POST to new as a create request
    if request.method == 'POST':
        return reflections_index(request, task_sheet_id)
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    form = ReflectionForm()
    return render_to_response(
            template_name,
            {
                'form': form,
                'task_sheet': task_sheet,
                },
            context_instance=RequestContext(request),
            )
def reflection_detail(request, task_sheet_id, reflection_id, template_name='pomodoro/reflection_detail.html'):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    reflection = get_object_or_404(Reflection, id=reflection_id, task_sheet=task_sheet)
    # retrieve details
    if request.method == 'GET':
        return render_to_response(
                template_name,
                {
                    'reflection': reflection,
                    'task_sheet': task_sheet,
                    },
                context_instance=RequestContext(request),
                )
        # update existing resource
    elif request.method == 'POST':
        form = ReflectionForm(request.POST, instance=reflection)
        # if form saves, return detail for saved resource
        if form.is_valid():
            reflection = form.save()
            return render_to_response(
                    template_name,
                    {
                        'reflection': reflection,
                        'task_sheet': task_sheet,
                        },
                    context_instance=RequestContext(request),
                    )
            # if save fails, go back to edit_resource page
        else:
            return render_to_response(
                    'pomodoro/edit_reflection.html',
                    {
                        'form': form,
                        'reflection': reflection,
                        'task_sheet': task_sheet,
                        },
                    context_instance=RequestContext(request),
                    )

def edit_reflection(request, task_sheet_id, reflection_id, template_name='pomodoro/edit_reflection.html'):
    # if a POST is received, direct it to resource detail for update
    if request.method == 'POST':
        return reflection_detail(request, task_sheet_id, reflection_id)
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    reflection = get_object_or_404(Reflection, id=reflection_id, task_sheet=task_sheet)
    form = ReflectionForm(instance=reflection)
    return render_to_response(
            template_name,
            {
                'form': form,
                'reflection': reflection,
                'task_sheet': task_sheet,
                },
            context_instance=RequestContext(request),
            )
def delete_reflection(request, task_sheet_id, reflection_id):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    reflection = get_object_or_404(Reflection, id=reflection_id, task_sheet=task_sheet)
    if request.method == 'POST':
        reflection.delete()
        return HttpResponseRedirect(reverse('reflections_index', kwargs={'task_sheet_id': task_sheet.id}))
    

def complete_pomodoro(request):
    current_pomodoro = Pomodoro.objects.get_current()
    if request.method == 'POST' and current_pomodoro is not None:
        current_pomodoro.completed = datetime.datetime.now()
        current_pomodoro.save()
    current_task_sheet = TaskSheet.objects.get_current()
    if current_task_sheet:
        response = HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': current_task_sheet.id}))
    else:
        response = HttpResponseRedirect(reverse('home'))
    return response

def cancel_pomodoro(request):
    current_pomodoro = Pomodoro.objects.get_current()
    if current_pomodoro is not None and request.method == 'POST':
        current_pomodoro.delete()
    current_task_sheet = TaskSheet.objects.get_current()
    if current_task_sheet:
        response = HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': current_task_sheet.id}))
    else:
        response = HttpResponseRedirect(reverse('home'))
    return response


def pomodoros_index(request, task_sheet_id, task_id, template_name='pomodoro/pomodoros_index.html'):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    task = get_object_or_404(Task, task_sheet=task_sheet, id=task_id)
    if request.method == 'GET':
        pomodoros = Pomodoro.objects.filter(task=task)
        return render_to_response(
                template_name,
                {
                    'task': task,
                    'pomodoros': pomodoros,
                    },
                context_instance=RequestContext(request),
                )
    elif request.method == 'POST':
        if not Pomodoro.objects.get_current():
            Pomodoro.objects.create(task=task)
        return HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': task_sheet_id,}))

def pomodoro_detail(request, task_sheet_id, task_id, pomodoro_id, template_name='pomodoro/pomodoro_detail.html'):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    task = get_object_or_404(Task, task_sheet=task_sheet, id=task_id)
    pomodoro = get_object_or_404(Pomodoro, task=task, id=pomodoro_id)
    # retrieve details
    if request.method == 'GET':
        return render_to_response(
                template_name,
                {
                    'pomodoro': pomodoro,
                    'task': task,
                    },
                context_instance=RequestContext(request),
                )
        # update existing resource
    elif request.method == 'POST':
        form = PomodoroForm(request.POST, instance=pomodoro)
        # if form saves, return detail for saved resource
        if form.is_valid():
            pomodoro = form.save()
            return render_to_response(
                    template_name,
                    {
                        'pomodoro': pomodoro,
                        'task': task,
                        },
                    context_instance=RequestContext(request),
                    )
            # if save fails, go back to edit_resource page
        else:
            return render_to_response(
                    'pomodoro/edit_pomodoro.html',
                    {
                        'form': form,
                        'pomodoro': pomodoro,
                        'task': task,
                        },
                    context_instance=RequestContext(request),
                    )

def add_internal_interruption(request):
    current_pomodoro = Pomodoro.objects.get_current()
    if current_pomodoro is not None:
        Mark.objects.create(task=current_pomodoro.task, type='internal')
    current_task_sheet = TaskSheet.objects.get_current()
    if current_task_sheet:
        response = HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': current_task_sheet.id}))
    else:
        response = HttpResponseRedirect(reverse('task_sheets_index'))
    return response



def add_external_interruption(request):
    current_pomodoro = Pomodoro.objects.get_current()
    if current_pomodoro is not None:
        Mark.objects.create(task=current_pomodoro.task, type='external')
    current_task_sheet = TaskSheet.objects.get_current()
    if current_task_sheet:
        response = HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': current_task_sheet.id}))
    else:
        response = HttpResponseRedirect(reverse('task_sheets_index'))
    return response


def marks_index(request, task_sheet_id, task_id, template_name='pomodoro/marks_index.html'):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    task = get_object_or_404(Task, task_sheet=task_sheet, id=task_id)
    if request.method == 'GET':
        marks = Mark.objects.filter(task=task)
        return render_to_response(
                template_name,
                {
                    'task': task,
                    'marks': marks,
                    },
                context_instance=RequestContext(request),
                )
    elif request.method == 'POST':
        form = MarkForm(request.POST)
        if form.is_valid():
            mark = form.save(commit=False)
            mark.task = task
            mark.save()
    return HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': current_task_sheet.id}))
