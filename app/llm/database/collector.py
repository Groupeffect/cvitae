from django.db import models
from django.contrib.auth import get_user_model
from api import models as api_models
from django_lifecycle import (
    LifecycleModelMixin,
    hook,
    AFTER_CREATE,
    BEFORE_CREATE,
    AFTER_UPDATE,
)
from django_lifecycle.conditions import WhenFieldValueChangesTo
from llm.manager.template import prompting
from cvitae.settings import BASE_DIR
import os

UserModel = get_user_model()


class MetaModel(LifecycleModelMixin, models.Model):
    name = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    user = models.ForeignKey(
        UserModel, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    updated = models.DateTimeField(auto_now_add=True)
    version = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.name}-{self.id}-{self.version}"


class PromptPreface(MetaModel):
    formatting = models.TextField(null=True, blank=True)
    instruction = models.TextField(null=True, blank=True)
    context_text = models.TextField(null=True, blank=True)
    jobpostings = models.ManyToManyField(api_models.JobPosting, blank=True)
    persons = models.ManyToManyField(api_models.Person, blank=True)
    letters = models.ManyToManyField(api_models.CoverLetter, blank=True)
    addresses = models.ManyToManyField(api_models.Address, blank=True)
    companies = models.ManyToManyField(api_models.Company, blank=True)
    qualifications = models.ManyToManyField(api_models.Qualification, blank=True)
    skills = models.ManyToManyField(api_models.Skill, blank=True)
    internships = models.ManyToManyField(api_models.Internship, blank=True)
    educations = models.ManyToManyField(api_models.Education, blank=True)
    reset = models.BooleanField(
        default=False, help_text="reset the formatting, instruction"
    )

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE, condition=WhenFieldValueChangesTo("reset", True))
    def set_defaults(self):
        files = [
            ["formatting", "concept-formatting.md"],
            ["instruction", "concept-assistant.md"],
        ]

        for i in files:
            path = os.path.join(BASE_DIR, f"llm/manager/template/assets/{i[1]}")
            with open(path, "r") as f:
                setattr(self, i[0], f.read())
        self.reset = False
        self.save()


class LLMClient(MetaModel):
    token = models.TextField(blank=True, null=True)


def preface_fields(*args, **kwargs):
    all = PromptPreface._get_field_names()
    filtered = [i for i in all if i not in [*MetaModel._get_field_names(), "id"]]
    return filtered


class PromptClient(MetaModel):
    prompt = models.TextField(null=True, blank=True)
    prefaces = models.ManyToManyField(PromptPreface, blank=True)
    preface_fields = models.JSONField(default=preface_fields, null=True, blank=True)
    client = models.ForeignKey(
        LLMClient, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    template = models.TextField(
        null=True, blank=True, help_text="auto generated template from preface config"
    )
    refresh = models.BooleanField(default=False, help_text="regenerate the template")
    refresh_preface_fields = models.BooleanField(
        default=False, help_text="reset the preface fields list"
    )
    response_json = models.JSONField(
        null=True, blank=True, help_text="llm response to the template as json"
    )
    response_text = models.TextField(
        null=True, blank=True, help_text="llm response to the template as text"
    )

    @hook(AFTER_CREATE)
    @hook(
        AFTER_UPDATE,
        condition=WhenFieldValueChangesTo("refresh", True),
    )
    def generate_template(self):
        self.refresh = False
        instance = prompting.PrefacePromptGenerator(self).write_template()
        instance.save()

    @hook(BEFORE_CREATE)
    def set_preface_fields(self):
        self.preface_fields = preface_fields()

    @hook(
        AFTER_UPDATE, condition=WhenFieldValueChangesTo("refresh_preface_fields", True)
    )
    def set_preface_fields(self):
        self.preface_fields = preface_fields()
        self.refresh_preface_fields = False
        self.save()
