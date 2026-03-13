from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


# ================= JOB SOURCE URL TEMPLATES =================
JOB_SOURCES = {
    "naukri": "https://www.naukri.com/{skill}-jobs-{page}",
    "indeed": "https://in.indeed.com/jobs?q={skill}&start={start}",
    "freshersworld": "https://www.freshersworld.com/jobs/jobsearch/{skill}-jobs-for-freshers"
}


# ================= DRIVER SETUP =================
def create_driver():
    options = Options()

    # Uncomment below for headless mode
    # options.add_argument("--headless=new")

    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


# ================= MAIN SCRAPER =================
def scrape_jobs(user_skills, pages=1):

    print("Multi-Platform Skill-Based Scraper Started...")
    print("Searching for skills:", user_skills)

    driver = create_driver()
    wait = WebDriverWait(driver, 15)

    all_jobs = []
    seen_links = set()

    for skill in user_skills:
        formatted_skill = skill.replace(" ", "-")

        for source, url_template in JOB_SOURCES.items():

            print(f"\nSearching {source.upper()} for skill: {skill}")

            for page in range(1, pages + 1):

                # -------- GENERATE URL --------
                if source == "naukri":
                    search_url = url_template.format(skill=formatted_skill, page=page)

                elif source == "indeed":
                    start = (page - 1) * 10
                    search_url = url_template.format(skill=skill, start=start)

                elif source == "freshersworld":
                    search_url = url_template.format(skill=formatted_skill)

                else:
                    continue

                driver.get(search_url)
                time.sleep(3)

                try:
                    # -------- PLATFORM-SPECIFIC SELECTORS --------
                    if source == "naukri":
                        job_cards = driver.find_elements(By.CSS_SELECTOR, "a.title")

                    elif source == "indeed":
                        job_cards = driver.find_elements(By.CSS_SELECTOR, "h2.jobTitle a")

                    elif source == "freshersworld":
                        job_cards = driver.find_elements(By.CSS_SELECTOR, "span.wrap-title a")

                    print(f"Found {len(job_cards)} jobs on {source} page {page}")

                except Exception as e:
                    print(f"No jobs found on {source}: {e}")
                    continue

                # -------- EXTRACT JOB DATA --------
                for job in job_cards:
                    try:
                        title = job.text.strip()
                        link = job.get_attribute("href")

                        if not link or link in seen_links:
                            continue

                        seen_links.add(link)

                        all_jobs.append({
                            "title": title,
                            "company": "Check Website",
                            "link": link,
                            "matched_skill": skill,
                            "source": source.capitalize()
                        })

                    except:
                        continue

    driver.quit()

    print("\nTotal Unique Jobs Collected:", len(all_jobs))

    return rank_jobs(all_jobs, user_skills)


# ================= RANKING SYSTEM =================
def rank_jobs(jobs, user_skills):

    ranked = []

    for job in jobs:

        combined_text = (
            job.get("title", "") + " " +
            job.get("company", "")
        ).lower()

        matched_skills = []
        score = 0

        for skill in user_skills:
            if skill.lower() in combined_text:
                matched_skills.append(skill)
                score += 1

        match_score = round((score / len(user_skills)) * 100, 2) if user_skills else 0

        job["matched_skills"] = matched_skills
        job["match_score"] = match_score

        ranked.append(job)

    ranked.sort(key=lambda x: x["match_score"], reverse=True)

    return ranked


# ================= RUN SCRIPT =================
if __name__ == "__main__":

    skills = ["python", "machine learning"]
    pages_to_scrape = 2

    results = scrape_jobs(skills, pages=pages_to_scrape)

    print("\nTop Ranked Jobs:\n")

    for job in results[:10]:
        print("Title:", job["title"])
        print("Source:", job["source"])
        print("Match Score:", job["match_score"], "%")
        print("Link:", job["link"])
        print("-" * 60)