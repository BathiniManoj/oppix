from django import forms
from .models import Resume,Resumebuilder

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']

        widgets = {
            'file': forms.FileInput(attrs={'accept': '.pdf'})
        }

class Resumebuilderform(forms.ModelForm):
    class Meta:
        model = Resumebuilder
        fields = "__all__"

        widgets = {
            "summary": forms.Textarea(attrs={"rows": 3}),
            "skills": forms.Textarea(attrs={"rows": 2}),
            "experience": forms.Textarea(attrs={"rows": 4}),
            "projects": forms.Textarea(attrs={"rows": 4}),
            "education": forms.Textarea(attrs={"rows": 2}),
            "certifications": forms.Textarea(attrs={"rows": 2}),
            "achievements": forms.Textarea(attrs={"rows": 2}),
        }