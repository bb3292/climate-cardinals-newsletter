#!/usr/bin/env python3
"""
Climate Cardinals - Automated Weekly Newsletter System
Uses DuckDuckGo (free, no API keys needed)
"""

import os
import sys
import json
import re
import csv
import time
import html
import random
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import requests
import pandas as pd
from bs4 import BeautifulSoup
from dateutil import parser
from ddgs import DDGS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------------- CONFIG ----------------------
POLITE_DELAY = 0.25
MAX_RESULTS_PER_KEYWORD = 4
MAX_ROWS_PER_SECTION = 40
MIN_YEAR = 2025
OUTPUT_FOLDER = Path("weekly_data")
OUTPUT_FOLDER.mkdir(exist_ok=True)
TODAY = datetime.now().date()

# Email config
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
RECIPIENT_EMAILS = [e.strip() for e in os.getenv("RECIPIENT_EMAILS", "").split(",") if e.strip()]

# ---------------------- KEYWORDS ----------------------
GRANT_KEYWORDS = [
    "resilience grant", "sustainability grant", "climate adaptation grant",
    "climate resilience funding", "community resilience grant"
]

EVENT_KEYWORDS = [
    "climate conference", "sustainability summit", "climate week",
    "resilience symposium", "environmental conference"
]

CSR_KEYWORDS = [
    "sustainability report pdf", "ESG report pdf", "impact report pdf",
    "climate disclosure report"
]

EXPERT_QUERIES = [
    "climate nonprofit executive director LinkedIn",
    "head of sustainability nonprofit LinkedIn",
    "climate resilience NGO director LinkedIn"
]

# ---------------------- RELEVANCE FILTER ----------------------
CLIMATE_TERMS = [
    "climate", "resilien", "adapt", "sustain", "environment", "decarbon",
    "net zero", "renewable", "flood", "heat", "wildfire", "community", "justice"
]

def looks_relevant(title, snippet, url):
    blob = f"{title} {snippet} {url}".lower()
    return any(t in blob for t in CLIMATE_TERMS)

# ---------------------- UTILS ----------------------
def clean_text(txt):
    return html.unescape(re.sub(r"\s+", " ", txt or "").strip())

def domain_from_url(url):
    try:
        return urlparse(url).netloc.replace("www.", "")
    except:
        return "—"

def extract_year(text):
    try:
        return parser.parse(text, fuzzy=True).year
    except:
        return None

def extract_date_snippet(text, future=True):
    if not text:
        return "—"
    month_pat = re.compile(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\s+\d{1,2},?\s*(20\d{2})", re.I
    )
    for m in month_pat.finditer(text):
        year = int(m.group(2))
        if year >= MIN_YEAR:
            return m.group(0)
    if future and re.search(r"rolling|ongoing|open until", text, re.I):
        return "Rolling / Ongoing"
    return "—"

# ---------------------- SEARCH ----------------------
def web_search(query, num=8):
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=num):
                results.append({
                    "title": r.get("title", ""),
                    "link": r.get("href", ""),
                    "snippet": r.get("body", "")
                })
    except Exception as e:
        print(f"⚠️  Search error: {e}")
    return results

# ---------------------- CORE PIPELINE ----------------------
def run_section(keywords, future=True):
    rows = []
    seen_domains = set()
    for kw in keywords:
        if len(rows) >= MAX_ROWS_PER_SECTION:
            break
        print(f"🔍 Searching: {kw}")
        items = web_search(kw, num=8)[:MAX_RESULTS_PER_KEYWORD]
        for item in items:
            if len(rows) >= MAX_ROWS_PER_SECTION:
                break
            url = item["link"]
            domain = domain_from_url(url)
            if not url or domain in seen_domains:
                continue
            seen_domains.add(domain)
            title = clean_text(item["title"])
            snippet = clean_text(item["snippet"])
            if not looks_relevant(title, snippet, url):
                continue
            date_info = extract_date_snippet(f"{title} {snippet}", future=future)
            year = extract_year(date_info)
            if year and year < MIN_YEAR:
                continue
            rows.append({
                "Title": title,
                "Organization": domain,
                "Description": snippet,
                "Date Info": date_info,
                "URL": url
            })
        time.sleep(POLITE_DELAY + random.uniform(0, 0.15))
    return rows

def looks_like_person(name):
    return (len(name.split()) >= 2 and name[0].isupper() and
            not any(x in name.lower() for x in ["jobs", "careers", "hiring"]))

def run_experts(queries):
    rows = []
    seen_profiles = set()
    for q in queries:
        print(f"🔍 Searching Experts: {q}")
        items = web_search(q, num=12)
        for item in items:
            url = item["link"]
            if "linkedin.com/in" not in url:
                continue
            if url in seen_profiles:
                continue
            seen_profiles.add(url)
            title = clean_text(item["title"])
            snippet = clean_text(item["snippet"])
            name = title.split("–")[0].split("-")[0].strip()
            if not looks_like_person(name):
                continue
            role = "—"
            parts = re.split(r"–|-", title)
            if len(parts) > 1:
                role = parts[1].strip()
            org = "—"
            if " at " in snippet:
                org = snippet.split(" at ")[-1].split(".")[0].strip()
            rows.append({
                "Name": name,
                "Role": role,
                "Organization": org,
                "LinkedIn": url
            })
        time.sleep(POLITE_DELAY)
        if len(rows) >= 30:
            break
    return rows

# ---------------------- WRITE CSVs ----------------------
def write_csv(name, data):
    path = OUTPUT_FOLDER / name
    if not data:
        print(f"Saved {name} (0 rows)")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {name} ({len(data)} rows)")

# ---------------------- MAIN ----------------------
def main():
    print("=" * 70)
    print("🌍 CLIMATE CARDINALS - AUTOMATED NEWSLETTER")
    print("=" * 70)
    print(f"📅 Date: {TODAY}")
    
    grants_data = run_section(GRANT_KEYWORDS, future=True)
    events_data = run_section(EVENT_KEYWORDS, future=True)
    csr_data = run_section(CSR_KEYWORDS, future=False)
    experts_data = run_experts(EXPERT_QUERIES)
    
    write_csv("grants.csv", grants_data)
    write_csv("events.csv", events_data)
    write_csv("csr_reports.csv", csr_data)
    write_csv("experts.csv", experts_data)
    
    print(f"\n✅ CSVs saved to: {OUTPUT_FOLDER.resolve()}")
    
    # Display summary
    pd.set_option("display.max_colwidth", 120)
    if grants_data:
        print("\n===== 🌍 GRANTS (2025+) =====")
        print(pd.DataFrame(grants_data).to_string())
    if events_data:
        print("\n===== 🎤 EVENTS (2025+) =====")
        print(pd.DataFrame(events_data).to_string())
    if csr_data:
        print("\n===== 🏢 CSR / ESG REPORTS =====")
        print(pd.DataFrame(csr_data).to_string())
    if experts_data:
        print("\n===== 👥 CLIMATE EXPERTS =====")
        print(pd.DataFrame(experts_data).to_string())

if __name__ == "__main__":
    main()
