# models.py
from django.db import models
from django.core.validators import FileExtensionValidator


class Resume(models.Model):
    file = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    link = models.URLField()
    skills = models.TextField()
    matched = models.BooleanField(default=False)    


class Resumebuilder(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    summary = models.TextField()

    skills = models.TextField(help_text="Comma or new line separated")

    experience = models.TextField(
        help_text="Each role on a new line with impact"
    )

    projects = models.TextField(
        help_text="Each project on a new line"
    )

    education = models.TextField()

    certifications = models.TextField(blank=True)
    achievements = models.TextField(blank=True)

    target_role = models.CharField(max_length=50)
    # ats_score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def combined_text(self):
        return f"""
        {self.summary}
        {self.skills}
        {self.experience}
        {self.projects}
        {self.education}
        {self.certifications}
        {self.achievements}
        """
    

    