from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404

from pomodoro.models import TaskSheet, Task, InboxItem, Reflection, Pomodoro, \
        InternalInterruption, ExternalInterruption

# task sheets
def task_sheets_index(request, template_name='pomodoro/task_sheets_index.html'):
    if request.method == 'GET':
        task_sheets = TaskSheet.objects.all()
        return render_to_response(
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
            return HttpResponseRedirect(
                    reverse('task_sheet_detail', kwargs={'task_sheet_id': task_sheet.id}))
        else:
            return render_to_response(
                    'pomodoro/new_task_sheet.html',
                    {
                        'form': form,
                        },
                    context_instance=RequestContext(request),
                    )

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
    if request.method == 'GET':
        return render_to_response(
                template_name,
                {
                    'task_sheet': task_sheet,
                    'inbox_item_form': inbox_item_form,
                    'task_form': task_form,
                    },
                context_instance=RequestContext(request),
                )
        # update existing resource
    elif request.method == 'POST':
        form = TaskSheetForm(request.POST, instance=task_sheet)
        # if form saves, return detail for saved resource
        if form.is_valid():
            task_sheet = form.save()
            return render_to_response(
                    template_name,
                    {
                        'task_sheet': task_sheet,
                        },
                    context_instance=RequestContext(request),
                    )
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
    

def pomodoros_index(request, task_sheet_id, task_id, template_name='pomodoro/pomodoros_index.html'):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    task = get_object_or_404(Task, task_sheet=TaskSheet, id=task_id)
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
        form = PomodoroForm(request.POST)
        if form.is_valid():
            pomodoro = form.save(commit=False)
            pomodoro.task = task
            pomodoro.save()
            return HttpResponseRedirect(reverse('task_sheet_detail', kwargs={'task_sheet_id': task_sheet_id,}))
        else:
            template_name = 'pomodoro/new_pomodoro.html'
            return render_to_response(
                    template_name,
                    {
                        'form': form,
                        'task': task,
                        },
                    context_instance=RequestContext(request),
                    )

def pomodoro_detail(request, task_sheet_id, task_id, pomodoro_id, template_name='pomodoro/pomodoro_detail.html'):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    task = get_object_or_404(Task, task_sheet=TaskSheet, id=task_id)
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

def internal_interruptions_index(request, task_sheet_id, task_id, template_name='pomodoro/internal_interruptions_index.html'):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    task = get_object_or_404(Task, task_sheet=TaskSheet, id=task_id)
    if request.method == 'GET':
        internal_interruptions = InternalInterruption.objects.filter(task=task)
        return render_to_response(
                template_name,
                {
                    'task': task,
                    'internal_interruptions': internal_interruptions,
                    },
                context_instance=RequestContext(request),
                )
    elif request.method == 'POST':
        form = InternalInterruptionForm(request.POST)
        if form.is_valid():
            internal_interruption = form.save(commit=False)
            internal_interruption.task = task
            internal_interruption.save()
            return HttpResponseRedirect(reverse('internal_interruption_detail', kwargs={'task_id': task.id, 'internal_interruption_id': internal_interruption.id}))
        else:
            template_name = 'pomodoro/new_internal_interruption.html'
            return render_to_response(
                    template_name,
                    {
                        'form': form,
                        'task': task,
                        },
                    context_instance=RequestContext(request),
                    )


def external_interruptions_index(request, task_sheet_id, task_id, template_name='pomodoro/external_interruptions_index.html'):
    task_sheet = get_object_or_404(TaskSheet, id=task_sheet_id)
    task = get_object_or_404(Task, task_sheet=TaskSheet, id=task_id)
    if request.method == 'GET':
        external_interruptions = ExternalInterruption.objects.filter(task=task)
        return render_to_response(
                template_name,
                {
                    'task': task,
                    'external_interruptions': external_interruptions,
                    },
                context_instance=RequestContext(request),
                )
    elif request.method == 'POST':
        form = ExternalInterruptionForm(request.POST)
        if form.is_valid():
            external_interruption = form.save(commit=False)
            external_interruption.task = task
            external_interruption.save()
            return HttpResponseRedirect(reverse('external_interruption_detail', kwargs={'task_id': task.id, 'external_interruption_id': external_interruption.id}))
        else:
            template_name = 'pomodoro/new_external_interruption.html'
            return render_to_response(
                    template_name,
                    {
                        'form': form,
                        'task': task,
                        },
                    context_instance=RequestContext(request),
                    )


