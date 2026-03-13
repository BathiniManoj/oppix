import re
from collections import Counter


# ================= TEXT CLEANER =================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text


# ================= ADVANCED MATCH ENGINE =================
def match_jobs(jobs, user_skills, min_threshold=25, top_n=25):

    if not user_skills:
        return []

    normalized_skills = [skill.lower().strip() for skill in user_skills]
    matched_jobs = []
    seen_links = set()

    for job in jobs:

        link = job.get("link")
        if not link or link in seen_links:
            continue

        seen_links.add(link)

        title = clean_text(job.get("title", ""))
        company = clean_text(job.get("company", ""))
        description = clean_text(job.get("description", ""))

        combined_text = f"{title} {company} {description}"
        word_list = combined_text.split()
        word_counter = Counter(word_list)

        score = 0
        matched_skills = []
        skill_frequency_score = 0

        for skill in normalized_skills:

            skill_words = skill.split()

            # ---------- Exact Phrase Match ----------
            if skill in combined_text:
                score += 5
                matched_skills.append(skill)

            # ---------- Title Priority Boost ----------
            if skill in title:
                score += 4

            # ---------- Description Boost ----------
            if skill in description:
                score += 3

            # ---------- Partial Word Matches ----------
            for word in skill_words:
                if word in word_counter:
                    score += 1
                    skill_frequency_score += word_counter[word]

        # ---------- Skill Density Bonus ----------
        total_words = len(word_list) if len(word_list) > 0 else 1
        density_score = skill_frequency_score / total_words

        score += density_score * 10  # scaled bonus

        # ---------- Multi-Skill Bonus ----------
        unique_matches = len(set(matched_skills))
        if unique_matches > 1:
            score += unique_matches * 2

        # ---------- Normalize ----------
        max_possible = len(normalized_skills) * 10
        match_score = round((score / max_possible) * 100, 2)

        # ---------- Filter Weak Jobs ----------
        if match_score >= min_threshold:
            job["matched_skills"] = list(set(matched_skills))
            job["match_score"] = match_score
            job["raw_score"] = round(score, 2)
            matched_jobs.append(job)

    # ---------- Sort By Best Score ----------
    matched_jobs.sort(
        key=lambda x: x["raw_score"],
        reverse=True
    )

    # ---------- Return Only Top 25 ----------
    return matched_jobs[:top_n]