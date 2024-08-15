from django.contrib import admin
from api import models

# Register your models here.
admin.site.site_title = "Groupeffect"
admin.site.site_header = "Groupeffect"
admin.site.register(models.Address)
admin.site.register(models.Application)
admin.site.register(models.Company)
admin.site.register(models.CoverLetter)
admin.site.register(models.Education)
admin.site.register(models.JobPosting)
admin.site.register(models.Person)
admin.site.register(models.WorkExperience)
admin.site.register(models.Internship)
admin.site.register(models.Skill)
admin.site.register(models.Photo)
admin.site.register(models.TemplateConfig)
admin.site.register(models.Qualification)
