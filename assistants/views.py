from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Assistant, KnowledgeSource
from .forms import AssistantForm, KnowledgeSourceForm
from .microservice_client import MicroserviceClient
from django.http import JsonResponse
import time

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
            client = MicroserviceClient()

            # 1. Create assistant in our DB
            assistant = assistant_form.save(commit=False)
            assistant.user = request.user

            # 2. Create assistant in microservice
            microservice_assistant = client.create_assistant(
                name=assistant.name,
                instructions=assistant.description,
                model='gpt-4o-mini' # Or get from form
            )
            assistant.microservice_assistant_id = microservice_assistant['id']

            # 3. Handle knowledge source
            knowledge = knowledge_form.save(commit=False)
            if knowledge.source_type == 'file' and knowledge.file:
                # Upload file to microservice
                uploaded_file = client.upload_file(knowledge.file)

                # Create vector store
                vector_store = client.create_vector_store(name=f"{assistant.name} VS")
                assistant.microservice_vector_store_id = vector_store['id']

                # Add file to vector store
                client.add_file_to_vector_store(vector_store['id'], uploaded_file['id'])

                # Update assistant with vector store
                client.update_assistant_vector_store(assistant.microservice_assistant_id, vector_store['id'])

            assistant.save()
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

class ChatView(LoginRequiredMixin, View):
    def get(self, request, assistant_id):
        assistant = Assistant.objects.get(id=assistant_id, user=request.user)
        return render(request, 'assistants/chat.html', {'assistant': assistant})

    def post(self, request, assistant_id):
        assistant = Assistant.objects.get(id=assistant_id, user=request.user)
        message = request.POST.get('message')
        client = MicroserviceClient()

        # Create a new thread for each conversation for simplicity
        thread = client.create_thread(initial_message=message)
        thread_id = thread['thread_id']

        # Run the thread
        client.run_thread(thread_id, assistant.microservice_assistant_id)

        # Poll for status
        while True:
            status_response = client.get_thread_status(thread_id)
            if status_response['status'] == 'completed':
                break
            time.sleep(1)

        # Get the latest message
        latest_message = client.get_latest_message(thread_id)

        return JsonResponse({'response': latest_message['content']})
