from django.shortcuts import render, redirect
from .utils import extract_text_from_pdf, extract_skills
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .scraper import scrape_jobs
from .matcher import match_jobs
from .forms import Resumebuilderform,ResumeForm
from .utils import ats_score
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import HRFlowable
from .models import Resume,Resumebuilder,Job
def home(request):
    return render(request, "home.html") 


def upload_resume(request):
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)

        if form.is_valid():
            resume = form.save()

            # Extract text
            text = extract_text_from_pdf(resume.file)

            # Extract skills
            skills = extract_skills(text)

            print("Extracted Skills:", skills)

            # Pass skills to scraper
            jobs = scrape_jobs(skills)

            # Store in session
            request.session["matched_jobs"] = jobs

            return redirect("job_results")

        else:
            print("Form errors:", form.errors)

    else:
        form = ResumeForm()

    return render(request, "upload.html", {"form": form})

def job_results(request):
    jobs = request.session.get("matched_jobs", [])
    print("Jobs Received in Results:", len(jobs))

    return render(request, "results.html", {"jobs": jobs})


  # adjust import if needed

def resumebuilder(request):
    form = Resumebuilderform()

    if request.method == "POST":
        form = Resumebuilderform(request.POST)

        if form.is_valid():
            resume = form.save(commit=False)

            try:
                score, matched, keywords = ats_score(
                    resume.combined_text(),
                    resume.target_role
                )

                resume.ats_score = score
                resume.save()

                return render(request, "atsresult.html", {
                    "resume": resume,
                    "score": score,
                    "matched": matched,
                    "missing": list(set(keywords) - set(matched))
                })

            except Exception as e:
                return render(request, "Resumebuilder.html", {
                    "form": form,
                    "error": f"ATS calculation failed: {str(e)}"
                })

    return render(request, "Resumebuilder.html", {"form": form})



def download_resume(request, resume_id):
    resume = get_object_or_404(Resumebuilder, id=resume_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_{resume.full_name}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    heading_style = styles["Heading1"]
    normal_style = styles["Normal"]

    elements.append(Paragraph(resume.full_name, heading_style))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"{resume.email} | {resume.phone}", normal_style))
    elements.append(Paragraph(f"{resume.linkedin} | {resume.github}", normal_style))
    elements.append(Spacer(1, 0.3 * inch))

    def add_section(title, content):
        elements.append(Paragraph(f"<b>{title}</b>", styles["Heading3"]))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        elements.append(Spacer(1, 0.1 * inch))
        elements.append(Paragraph(content.replace("\n", "<br/>"), normal_style))
        elements.append(Spacer(1, 0.3 * inch))

    add_section("Summary", resume.summary)
    add_section("Skills", resume.skills)
    add_section("Experience", resume.experience)
    add_section("Projects", resume.projects)
    add_section("Education", resume.education)
    add_section("Certifications", resume.certifications)
    add_section("Achievements", resume.achievements)

    doc.build(elements)
    return response

def atsresult(request):
    return render(request, "atsresult.html")