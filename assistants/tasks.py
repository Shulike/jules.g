from celery import shared_task
from .models import KnowledgeSource
import pypdf
import requests
from bs4 import BeautifulSoup

@shared_task
def process_knowledge_source(knowledge_source_id):
    try:
        knowledge_source = KnowledgeSource.objects.get(id=knowledge_source_id)
        if knowledge_source.source_type == 'file':
            if knowledge_source.file.name.endswith('.pdf'):
                reader = pypdf.PdfReader(knowledge_source.file.path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                knowledge_source.processed_text = text
                knowledge_source.save()
        elif knowledge_source.source_type == 'url':
            response = requests.get(knowledge_source.url)
            soup = BeautifulSoup(response.content, 'html.parser')
            knowledge_source.processed_text = soup.get_text()
            knowledge_source.save()
    except KnowledgeSource.DoesNotExist:
        # Handle error
        pass
