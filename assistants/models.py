from django.db import models
from django.conf import settings

class Assistant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    microservice_assistant_id = models.CharField(max_length=255, blank=True)
    microservice_vector_store_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class KnowledgeSource(models.Model):
    assistant = models.ForeignKey(Assistant, related_name='knowledge_sources', on_delete=models.CASCADE)
    source_type = models.CharField(max_length=10, choices=[('file', 'File'), ('url', 'URL')])
    file = models.FileField(upload_to='knowledge_files/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    processed_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_source_type_display()} for {self.assistant.name}"
