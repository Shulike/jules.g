from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Assistant
from .forms import AssistantForm, KnowledgeSourceForm

class AssistantListView(LoginRequiredMixin, ListView):
    model = Assistant
    template_name = 'assistants/assistant_list.html'
    context_object_name = 'assistants'

    def get_queryset(self):
        return Assistant.objects.filter(user=self.request.user)

def create_assistant(request):
    if request.method == 'POST':
        assistant_form = AssistantForm(request.POST)
        knowledge_form = KnowledgeSourceForm(request.POST, request.FILES)
        if assistant_form.is_valid() and knowledge_form.is_valid():
            assistant = assistant_form.save(commit=False)
            assistant.user = request.user
            assistant.save()
            knowledge = knowledge_form.save(commit=False)
            knowledge.assistant = assistant
            knowledge.save()
            return redirect('assistant_list')
    else:
        assistant_form = AssistantForm()
        knowledge_form = KnowledgeSourceForm()
    return render(request, 'assistants/create_assistant.html', {
        'assistant_form': assistant_form,
        'knowledge_form': knowledge_form
    })
