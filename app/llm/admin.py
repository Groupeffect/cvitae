from django.contrib import admin
from llm.database import collector

# Register your models here.
admin.site.register(collector.LLMClient)
admin.site.register(collector.PromptClient)
admin.site.register(collector.PromptPreface)
