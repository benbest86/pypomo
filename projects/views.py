# Create your views here.
# Create your views here.

from django.pimentech.network import JSONRPCService, jsonremote
from django.utils import simplejson as json
from projects.models import Task, Project
from projects.forms import ProjectForm

service = JSONRPCService()

@jsonremote(service)
def getProjects(request):
    return [project.serialize() for project in Project.objects.all()]

@jsonremote(service)
def addProject(request, name, success_statement):
    form = ProjectForm({'name':name, 'success_statement':success_statement})
    if form.is_valid():
        p = form.save()
        return p.serialize()
    else:
        return {'status': 'error'}

@jsonremote(service)
def deleteProject (request,idFromJson):
    p = Project.objects.get(id=idFromJson)
    p.delete()
    return getProjects(request)
