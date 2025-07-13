from django import forms
from .models import Assistant, KnowledgeSource

class AssistantForm(forms.ModelForm):
    class Meta:
        model = Assistant
        fields = ['name', 'description']

class KnowledgeSourceForm(forms.ModelForm):
    class Meta:
        model = KnowledgeSource
        fields = ['source_type', 'file', 'url']
