import base64
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class MetaModel(models.Model):
    allow_access = models.ManyToManyField(User, blank=True)
    sorting = models.FloatField(default=0.1)

    class Meta:
        abstract = True
        ordering = ["sorting"]


class MetaCardModelMixin(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    css_classes = models.TextField(blank=True, null=True)
    css_id = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        if hasattr(self, "title"):
            if self.title:
                return f"{self.title} - {self.id}"
        return f"{self.name} - {self.id}"


class Photo(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    css_classes = models.TextField(blank=True, null=True)
    css_id = models.TextField(blank=True, null=True)
    image_b64 = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="photos")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        file = self.image.file
        self.name = file.name.split("/")[-1]
        b64 = f"data:image/{file.name.split('.')[-1]};base64, {base64.b64encode(file.read()).decode('ascii')}"
        self.image_b64 = b64
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        return f"{self.name}"


class Address(MetaModel):
    street = models.CharField(max_length=100, blank=True, null=True)
    house_number = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.street} {self.house_number} {self.city}"


class Person(MetaModel):
    description = models.TextField(blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ForeignKey(
        Photo, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.ForeignKey(
        Address, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    website = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.id}"


class Company(MetaModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=400, blank=True, null=True)
    address = models.ForeignKey(
        Address, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    def __str__(self) -> str:
        return f"{self.name}"


class JobPosting(MetaModel):
    website = models.URLField(blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    document = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.company.name} - {self.title}"


class WorkExperience(MetaCardModelMixin, MetaModel):
    companies = models.ManyToManyField(Company, blank=True)
    duration_years = models.FloatField(default=1.5)


class Education(MetaCardModelMixin, MetaModel):
    institution = models.CharField(max_length=100, blank=True, null=True)
    address = models.ForeignKey(
        Address, on_delete=models.DO_NOTHING, blank=True, null=True
    )


class Skill(MetaCardModelMixin, MetaModel):
    pass


class Qualification(MetaCardModelMixin, MetaModel):

    institution = models.CharField(max_length=100, blank=True, null=True)
    address = models.ForeignKey(
        Address, on_delete=models.DO_NOTHING, blank=True, null=True
    )


class Internship(MetaCardModelMixin, MetaModel):
    address = models.ForeignKey(
        Address, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    institution = models.CharField(max_length=100, blank=True, null=True)


class CoverLetter(MetaModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    greeting = models.TextField(blank=True, null=True)
    header = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    footer = models.TextField(blank=True, null=True)
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    start = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"


class TemplateConfig(MetaModel):
    name = models.TextField(blank=True, null=True)
    cv_header = models.TextField(blank=True, null=True)
    cv_body = models.TextField(blank=True, null=True)
    letter_header = models.TextField(blank=True, null=True)
    letter_body = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Application(MetaModel):
    avatar = models.ForeignKey(
        Photo, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    language = models.CharField(
        max_length=2, choices=[["de", "DE"], ["en", "EN"]], default="de"
    )
    job_posting = models.ForeignKey(
        JobPosting, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    person = models.ForeignKey(
        Person, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    company = models.ForeignKey(
        Company, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    cover_letter = models.ForeignKey(
        CoverLetter, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    educations = models.ManyToManyField(Education, blank=True)
    internships = models.ManyToManyField(Internship, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    qualifications = models.ManyToManyField(Qualification, blank=True)
    work = models.ManyToManyField(WorkExperience, blank=True)
    template = models.ForeignKey(
        TemplateConfig, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    def __str__(self) -> str:
        if hasattr(self.job_posting, "title"):
            return f"{self.job_posting.title} - {self.id}"
        return f"{self.id}"
