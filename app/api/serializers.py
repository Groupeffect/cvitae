from rest_framework import serializers
from api import models
from urllib import parse


class MetaSerializer(serializers.ModelSerializer):
    pass


class AddressModelSerializer(MetaSerializer):
    class Meta:
        model = models.Address
        fields = "__all__"


class PhotoModelSerializer(MetaSerializer):
    class Meta:
        model = models.Photo
        fields = "__all__"


class CompanyModelSerializer(MetaSerializer):
    address = AddressModelSerializer(read_only=True)

    class Meta:
        model = models.Company
        fields = "__all__"


class PersonModelSerializer(MetaSerializer):
    address = AddressModelSerializer(read_only=True)
    avatar = PhotoModelSerializer(read_only=True)

    class Meta:
        model = models.Person
        fields = "__all__"


class EducationModelSerializer(MetaSerializer):
    address = AddressModelSerializer(read_only=True)

    class Meta:
        model = models.Education
        fields = "__all__"


class WorkExperienceModelSerializer(MetaSerializer):
    companies = CompanyModelSerializer(read_only=True, many=True)

    class Meta:
        model = models.WorkExperience
        fields = "__all__"


class JobPostingModelSerializer(MetaSerializer):
    class Meta:
        model = models.JobPosting
        fields = "__all__"


class SkillModelSerializer(MetaSerializer):
    class Meta:
        model = models.Skill
        fields = "__all__"


class QualificationModelSerializer(MetaSerializer):
    class Meta:
        model = models.Qualification
        fields = "__all__"


class InternshipModelSerializer(MetaSerializer):
    class Meta:
        model = models.Internship
        fields = "__all__"


class CoverLetterModelSerializer(MetaSerializer):
    class Meta:
        model = models.CoverLetter
        fields = "__all__"


class TemplateConfigModelSerializer(MetaSerializer):
    class Meta:
        model = models.TemplateConfig
        fields = "__all__"


class ApplicationSlimModelSerializer(MetaSerializer):
    links = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Application
        fields = ["id", "company", "template", "links"]

    def get_links(self, instance):
        r = self.context["request"]
        a = self.context["view"].action
        url = r.build_absolute_uri()
        params = ["edit", "app", "api", "cv", "letter", "slim", "json"]
        uri = parse.urljoin(url, str(instance.id))
        links = [parse.urljoin(uri, f"?format={i}") for i in params]
        if a in ["list"]:
            return links
        return url


class ApplicationModelSerializer(ApplicationSlimModelSerializer):
    company = CompanyModelSerializer(read_only=True)
    cover_letter = CoverLetterModelSerializer(read_only=True)
    job_posting = JobPostingModelSerializer(read_only=True)
    educations = EducationModelSerializer(read_only=True, many=True)
    person = PersonModelSerializer(read_only=True)
    skills = SkillModelSerializer(read_only=True, many=True)
    qualifications = QualificationModelSerializer(read_only=True, many=True)
    work = WorkExperienceModelSerializer(read_only=True, many=True)
    internships = InternshipModelSerializer(read_only=True, many=True)
    avatar = PhotoModelSerializer(read_only=True)
    template = TemplateConfigModelSerializer(read_only=True)

    class Meta:
        model = models.Application
        fields = "__all__"


class ApplicationEditModelSerializer(ApplicationModelSerializer):
    template_options = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Application
        fields = "__all__"

    def get_template_options(self, instance):
        configs = models.TemplateConfig.objects.all()
        return list(configs.values())
