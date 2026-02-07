#!/usr/bin/env python3
"""
Climate Cardinals - Automated Weekly Newsletter System
FREE VERSION - Uses RapidAPI + DuckDuckGo (no Google API needed)
Runs daily, accumulates data, sends email on Monday, then resets
"""

import os
import sys
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path

# Install dependencies
try:
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
    from dateutil import parser
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", 
                          "requests", "beautifulsoup4", "lxml", "html5lib", "pandas", "python-dateutil"])
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
    from dateutil import parser

import re
import csv
import time
import html
from urllib.parse import urlencode, quote_plus
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------------- CONFIGURATION ----------------------
# Load from environment variables or config file
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")  # Get free key from rapidapi.com

# Email configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS", "").split(",")

# File paths
DATA_DIR = Path("weekly_data")
DATA_DIR.mkdir(exist_ok=True)
STATE_FILE = DATA_DIR / "state.json"
CACHE_FILE = DATA_DIR / "search_cache.json"

GRANTS_FILE = DATA_DIR / "grants.csv"
EVENTS_FILE = DATA_DIR / "events.csv"
CSR_FILE = DATA_DIR / "csr_reports.csv"
EXPERTS_FILE = DATA_DIR / "experts.csv"

# Constants
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
FETCH_TIMEOUT = 10
POLITE_DELAY = 1.0  # Increased for free APIs
DAILY_QUERY_LIMIT = 70  # Conservative limit for free tier

# Keywords (rotating to avoid hitting same queries every day)
ALL_GRANT_KEYWORDS = [
    "climate resilience grant 2026", "sustainability funding opportunity",
    "environmental grant program", "climate adaptation funding",
    "green energy grant", "climate action funding"
]

ALL_EVENT_KEYWORDS = [
    "climate conference 2026", "sustainability summit",
    "environmental conference", "climate week event",
    "green energy summit", "climate action conference"
]

ALL_CSR_KEYWORDS = [
    "sustainability report 2025", "ESG disclosure 2025",
    "corporate climate report", "environmental impact report",
    "carbon emissions report", "sustainability disclosure"
]

ALL_EXPERT_QUERIES = [
    "climate NGO director linkedin", "sustainability director linkedin",
    "environmental program manager linkedin", "climate partnerships director linkedin"
]

# ---------------------- SEARCH CACHE ----------------------
def load_cache():
    """Load search result cache to avoid repeat queries"""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    """Save search cache"""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

# ---------------------- FREE SEARCH FUNCTIONS ----------------------
def rapidapi_search(query, num=10):
    """Search using RapidAPI Real-Time Web Search (free tier available)"""
    if not RAPIDAPI_KEY:
        print("  ⚠️  No RapidAPI key - skipping")
        return []
    
    url = "https://real-time-web-search.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "real-time-web-search.p.rapidapi.com"
    }
    params = {
        "q": query,
        "num": str(num),
        "start": "0",
        "gl": "us",
        "hl": "en",
        "fetch_ai_overviews": "false",
        "nfpr": "0",
        "return_organic_result_video_thumbnail": "false",
        "deduplicate": "true"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            items = []
            
            # Parse the response - Real-Time Web Search returns 'data' array
            for result in data.get("data", [])[:num]:
                items.append({
                    "title": result.get("title", ""),
                    "link": result.get("url", ""),
                    "snippet": result.get("snippet", "")
                })
            
            print(f"  ✓ RapidAPI: {len(items)} results")
            return items
        else:
            print(f"  ⚠️  RapidAPI returned {response.status_code}")
            return []
    except Exception as e:
        print(f"  ⚠️  RapidAPI error: {e}")
        return []

def duckduckgo_search(query, num=10):
    """Fallback: Scrape DuckDuckGo HTML results (unlimited, free)"""
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        items = []
        for result in soup.select(".result")[:num]:
            link_tag = result.select_one(".result__a")
            snippet_tag = result.select_one(".result__snippet")
            
            if link_tag:
                title = link_tag.get_text(strip=True)
                link = link_tag.get("href", "")
                snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
                
                if link and title:
                    items.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet
                    })
        
        print(f"  ✓ DuckDuckGo: {len(items)} results")
        return items
        
    except Exception as e:
        print(f"  ⚠️  DuckDuckGo error: {e}")
        return []

def free_search(query, num=10, use_cache=True):
    """
    Combined free search with caching
    1. Check cache first
    2. Try RapidAPI (structured, 500/month free)
    3. Fallback to DuckDuckGo (unlimited)
    """
    cache = load_cache() if use_cache else {}
    
    # Check cache
    cache_key = f"{query}:{num}"
    if cache_key in cache:
        cached_time = datetime.fromisoformat(cache.get(f"{cache_key}:time", "2020-01-01"))
        age_days = (datetime.now() - cached_time).days
        
        if age_days < 7:  # Cache valid for 1 week
            print(f"  ✓ Cache hit (age: {age_days} days)")
            return cache[cache_key]
    
    # Try RapidAPI first
    items = rapidapi_search(query, num)
    
    # Fallback to DuckDuckGo if no results
    if not items:
        print("  → Falling back to DuckDuckGo...")
        items = duckduckgo_search(query, num)
    
    # Cache results
    if items and use_cache:
        cache[cache_key] = items
        cache[f"{cache_key}:time"] = datetime.now().isoformat()
        save_cache(cache)
    
    return items

# ---------------------- STATE MANAGEMENT ----------------------
def load_state():
    """Load the current state (tracks queries used, last reset, etc.)"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "queries_used_today": 0,
        "last_reset_date": datetime.now().strftime("%Y-%m-%d"),
        "last_email_sent": None,
        "week_start_date": (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
    }

def save_state(state):
    """Save the current state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def reset_daily_counter(state):
    """Reset daily query counter if it's a new day"""
    today = datetime.now().strftime("%Y-%m-%d")
    if state["last_reset_date"] != today:
        state["queries_used_today"] = 0
        state["last_reset_date"] = today
    return state

def should_send_email(state):
    """Check if it's Monday and we haven't sent email this week"""
    today = datetime.now()
    is_monday = today.weekday() == 0  # Monday = 0
    
    last_sent = state.get("last_email_sent")
    if last_sent:
        last_sent_date = datetime.strptime(last_sent, "%Y-%m-%d")
        days_since_sent = (today - last_sent_date).days
        if days_since_sent < 7:
            return False
    
    return is_monday

# ---------------------- DATA EXTRACTION FUNCTIONS ----------------------
def is_future_date(date_str):
    try:
        dt = parser.parse(date_str, fuzzy=True)
        return dt.date() >= datetime.now().date()
    except:
        return False

def is_past_date(date_str):
    try:
        dt = parser.parse(date_str, fuzzy=True)
        return dt.date() < datetime.now().date()
    except:
        return False

def extract_date(url, snippet, mode="future"):
    """Extract dates from page content"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=FETCH_TIMEOUT)
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text("\n", strip=True)
    except:
        text = snippet or ""
    
    text = re.sub(r"[ \t]+", " ", text)
    
    # Look for labeled dates
    labeled_pattern = re.compile(
        r"((?:Deadline|Apply By|Event Date|Conference Date|Published|Issued|Released)[^\n]{0,80}?)"
        r"((?:January|February|March|April|May|June|July|August|September|October|November|December)[^\n]{0,60}?20\d{2})",
        re.I
    )
    
    results = []
    for label, dateStr in labeled_pattern.findall(text):
        date_clean = dateStr.strip()
        valid = is_future_date(date_clean) if mode == "future" else is_past_date(date_clean)
        if valid:
            label_clean = label.strip().rstrip(":").strip()
            results.append(f"{label_clean}: {date_clean}")
    
    if results:
        return " | ".join(results[:3])
    
    # Fallback to any date
    single_date = re.search(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)[^\n]{0,40}20\d{2}",
        text, re.I)
    if single_date:
        d = single_date.group(0).strip()
        if (mode == "future" and is_future_date(d)) or (mode == "past" and is_past_date(d)):
            return d
    
    return "—"

def clean_text(txt):
    return html.unescape(re.sub(r"\s+", " ", txt or "").strip())

def domain_from_url(link):
    try:
        return link.split("/")[2].replace("www.", "")
    except:
        return "—"

def collect_data(keywords, mode="future", max_queries=15):
    """Collect data for a category"""
    data = []
    queries_used = 0
    
    for kw in keywords[:max_queries]:
        if queries_used >= max_queries:
            break
        
        print(f"  Searching: {kw}")
        items = free_search(kw, num=8)  # Reduced to 8 per query
        queries_used += 1
        
        for item in items:
            title = item.get("title", "—")
            link = item.get("link", "#")
            snippet = item.get("snippet", "")
            domain = domain_from_url(link)
            
            if not snippet or len(snippet) < 20:
                continue
            
            date_info = extract_date(link, snippet, mode=mode)
            
            if date_info != "—":
                data.append({
                    "Title": clean_text(title),
                    "Domain": domain,
                    "Description": clean_text(snippet),
                    "Date Info": date_info,
                    "URL": link
                })
        
        time.sleep(POLITE_DELAY)
    
    return data, queries_used

def collect_experts(queries, max_queries=10):
    """Collect expert contacts"""
    data = []
    queries_used = 0
    name_pat = re.compile(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)+")
    
    for q in queries[:max_queries]:
        if queries_used >= max_queries:
            break
        
        print(f"  Searching: {q}")
        items = free_search(q, num=8)
        queries_used += 1
        
        for item in items:
            title = item.get("title", "")
            link = item.get("link", "#")
            snippet = item.get("snippet", "")
            
            if not name_pat.match(title):
                continue
            
            if "linkedin.com/in/" not in link:
                continue
            
            role = "—"
            if " at " in snippet:
                role = snippet.split(" at ")[0].strip().title()
            elif " - " in snippet:
                role = snippet.split(" - ")[0].strip().title()
            
            data.append({
                "Name": title,
                "Role": role,
                "LinkedIn": link
            })
        
        time.sleep(POLITE_DELAY)
    
    return data, queries_used

def append_to_csv(filepath, fieldnames, new_data):
    """Append new data to CSV, avoiding duplicates"""
    # Load existing data
    existing_data = []
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_data = list(reader)
    
    # Create set of existing items (by title or name)
    key_field = "Name" if "Name" in fieldnames else "Title"
    existing_keys = {row[key_field] for row in existing_data}
    
    # Add only new items
    new_items = [item for item in new_data if item.get(key_field, "") not in existing_keys]
    
    # Write all data back
    all_data = existing_data + new_items
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)
    
    return len(new_items)

# ---------------------- EMAIL GENERATION ----------------------
from email_template import generate_email_html

def send_email(html_content, subject):
    """Send email via SMTP"""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("❌ Email credentials not configured!")
        print("Set SENDER_EMAIL and SENDER_PASSWORD environment variables")
        return False
    
    if not RECIPIENT_EMAILS or RECIPIENT_EMAILS == ['']:
        print("❌ No recipient emails configured!")
        print("Set RECIPIENT_EMAILS environment variable")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(RECIPIENT_EMAILS)
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent successfully to {len(RECIPIENT_EMAILS)} recipients")
        return True
    
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def clear_weekly_data():
    """Clear all CSV files and cache after email is sent"""
    for file in [GRANTS_FILE, EVENTS_FILE, CSR_FILE, EXPERTS_FILE, CACHE_FILE]:
        if file.exists():
            file.unlink()
    print("🗑️  Weekly data cleared")

# ---------------------- MAIN EXECUTION ----------------------
def main():
    print("=" * 70)
    print("🌍 CLIMATE CARDINALS - FREE AUTOMATED NEWSLETTER")
    print("=" * 70)
    
    # Load state
    state = load_state()
    state = reset_daily_counter(state)
    
    today = datetime.now()
    print(f"\n📅 Date: {today.strftime('%A, %B %d, %Y')}")
    print(f"📊 Queries used today: {state['queries_used_today']}/{DAILY_QUERY_LIMIT}")
    
    # Check if we should send email (Monday)
    if should_send_email(state):
        print("\n📧 It's Monday! Sending weekly newsletter...")
        
        # Load accumulated data
        try:
            experts_df = pd.read_csv(EXPERTS_FILE) if EXPERTS_FILE.exists() else pd.DataFrame()
            grants_df = pd.read_csv(GRANTS_FILE) if GRANTS_FILE.exists() else pd.DataFrame()
            events_df = pd.read_csv(EVENTS_FILE) if EVENTS_FILE.exists() else pd.DataFrame()
            csr_df = pd.read_csv(CSR_FILE) if CSR_FILE.exists() else pd.DataFrame()
            
            # Generate and send email
            html_content = generate_email_html(experts_df, grants_df, events_df, csr_df)
            subject = f"Climate Cardinals Weekly Intelligence - {today.strftime('%B %d, %Y')}"
            
            if send_email(html_content, subject):
                state["last_email_sent"] = today.strftime("%Y-%m-%d")
                state["week_start_date"] = today.strftime("%Y-%m-%d")
                clear_weekly_data()
            
        except Exception as e:
            print(f"❌ Error generating/sending email: {e}")
    
    else:
        # Not Monday, collect daily data
        print(f"\n📥 Collecting data for the week (Day {today.weekday() + 1}/7)")
        
        remaining_queries = DAILY_QUERY_LIMIT - state['queries_used_today']
        if remaining_queries <= 0:
            print("⚠️  Daily query limit reached. Skipping collection.")
            save_state(state)
            return
        
        # Distribute queries across categories
        queries_per_category = remaining_queries // 4
        
        print(f"\n💰 Collecting Grants ({queries_per_category} queries)...")
        grants_data, used = collect_data(ALL_GRANT_KEYWORDS, mode="future", max_queries=queries_per_category)
        new_grants = append_to_csv(GRANTS_FILE, ["Title", "Domain", "Description", "Date Info", "URL"], grants_data)
        state['queries_used_today'] += used
        print(f"   Added {new_grants} new grants")
        
        print(f"\n📅 Collecting Events ({queries_per_category} queries)...")
        events_data, used = collect_data(ALL_EVENT_KEYWORDS, mode="future", max_queries=queries_per_category)
        new_events = append_to_csv(EVENTS_FILE, ["Title", "Domain", "Description", "Date Info", "URL"], events_data)
        state['queries_used_today'] += used
        print(f"   Added {new_events} new events")
        
        print(f"\n📊 Collecting CSR Reports ({queries_per_category} queries)...")
        csr_data, used = collect_data(ALL_CSR_KEYWORDS, mode="past", max_queries=queries_per_category)
        new_csr = append_to_csv(CSR_FILE, ["Title", "Domain", "Description", "Date Info", "URL"], csr_data)
        state['queries_used_today'] += used
        print(f"   Added {new_csr} new reports")
        
        print(f"\n👥 Collecting Experts ({queries_per_category} queries)...")
        experts_data, used = collect_experts(ALL_EXPERT_QUERIES, max_queries=queries_per_category)
        new_experts = append_to_csv(EXPERTS_FILE, ["Name", "Role", "LinkedIn"], experts_data)
        state['queries_used_today'] += used
        print(f"   Added {new_experts} new experts")
        
        print(f"\n📊 Total queries used today: {state['queries_used_today']}/{DAILY_QUERY_LIMIT}")
    
    # Save state
    save_state(state)
    print("\n✅ Daily run complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()


# Email configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")
RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS", "").split(",")

# File paths
DATA_DIR = Path("weekly_data")
DATA_DIR.mkdir(exist_ok=True)
STATE_FILE = DATA_DIR / "state.json"

GRANTS_FILE = DATA_DIR / "grants.csv"
EVENTS_FILE = DATA_DIR / "events.csv"
CSR_FILE = DATA_DIR / "csr_reports.csv"
EXPERTS_FILE = DATA_DIR / "experts.csv"

# Constants
HEADERS = {"User-Agent": "Mozilla/5.0"}
FETCH_TIMEOUT = 10
POLITE_DELAY = 0.4
DAILY_QUERY_LIMIT = 90  # Stay under 100/day limit

# Keywords (rotating to avoid hitting same queries every day)
ALL_GRANT_KEYWORDS = [
    "resilience grant", "sustainability grant", "climate adaptation grant",
    "climate resilience funding", "community resilience grant",
    "environmental grant", "green energy funding", "climate action grant"
]

ALL_EVENT_KEYWORDS = [
    "climate conference", "sustainability summit", "climate week",
    "resilience symposium", "environmental conference",
    "green energy summit", "climate action event", "sustainability forum"
]

ALL_CSR_KEYWORDS = [
    "corporate sustainability report", "CSR report", "impact report",
    "environmental report", "climate disclosure",
    "ESG report", "sustainability disclosure", "carbon report"
]

ALL_EXPERT_QUERIES = [
    "climate NGO director OR head of sustainability site:linkedin.com/in",
    "climate nonprofit founder OR partnerships director site:linkedin.com/in",
    "environmental program director OR sustainability manager site:linkedin.com/in"
]

# ---------------------- STATE MANAGEMENT ----------------------
def load_state():
    """Load the current state (tracks queries used, last reset, etc.)"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "queries_used_today": 0,
        "last_reset_date": datetime.now().strftime("%Y-%m-%d"),
        "last_email_sent": None,
        "week_start_date": (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
    }

def save_state(state):
    """Save the current state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def reset_daily_counter(state):
    """Reset daily query counter if it's a new day"""
    today = datetime.now().strftime("%Y-%m-%d")
    if state["last_reset_date"] != today:
        state["queries_used_today"] = 0
        state["last_reset_date"] = today
    return state

def should_send_email(state):
    """Check if it's Monday and we haven't sent email this week"""
    today = datetime.now()
    is_monday = today.weekday() == 0  # Monday = 0
    
    last_sent = state.get("last_email_sent")
    if last_sent:
        last_sent_date = datetime.strptime(last_sent, "%Y-%m-%d")
        days_since_sent = (today - last_sent_date).days
        if days_since_sent < 7:
            return False
    
    return is_monday

# ---------------------- DATA COLLECTION FUNCTIONS ----------------------
def google_search(query, num=5):
    """Search using DuckDuckGo (free, no rate limits)"""
    results = []
    try:
        from ddgs import DDGS
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

def is_future_date(date_str):
    try:
        dt = parser.parse(date_str, fuzzy=True)
        return dt.date() >= datetime.now().date()
    except:
        return False

def is_past_date(date_str):
    try:
        dt = parser.parse(date_str, fuzzy=True)
        return dt.date() < datetime.now().date()
    except:
        return False

def extract_date(url, snippet, mode="future"):
    """Extract dates from page content"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=FETCH_TIMEOUT)
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text("\n", strip=True)
    except:
        text = snippet or ""
    
    text = re.sub(r"[ \t]+", " ", text)
    
    # Look for labeled dates
    labeled_pattern = re.compile(
        r"((?:Deadline|Apply By|Event Date|Conference Date|Published|Issued|Released)[^\n]{0,80}?)"
        r"((?:January|February|March|April|May|June|July|August|September|October|November|December)[^\n]{0,60}?20\d{2})",
        re.I
    )
    
    results = []
    for label, dateStr in labeled_pattern.findall(text):
        date_clean = dateStr.strip()
        valid = is_future_date(date_clean) if mode == "future" else is_past_date(date_clean)
        if valid:
            label_clean = label.strip().rstrip(":").strip()
            results.append(f"{label_clean}: {date_clean}")
    
    if results:
        return " | ".join(results[:3])
    
    # Fallback to any date
    single_date = re.search(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)[^\n]{0,40}20\d{2}",
        text, re.I)
    if single_date:
        d = single_date.group(0).strip()
        if (mode == "future" and is_future_date(d)) or (mode == "past" and is_past_date(d)):
            return d
    
    return "—"

def clean_text(txt):
    return html.unescape(re.sub(r"\s+", " ", txt or "").strip())

def domain_from_url(link):
    try:
        return link.split("/")[2].replace("www.", "")
    except:
        return "—"

def collect_data(keywords, mode="future", max_queries=20):
    """Collect data for a category"""
    data = []
    queries_used = 0
    
    for kw in keywords[:max_queries]:  # Limit keywords
        if queries_used >= max_queries:
            break
        
        print(f"  Searching: {kw}")
        items = google_search(kw, num=5)
        queries_used += 1
        
        for item in items:
            # Handle both Google and RapidAPI response formats
            if isinstance(item, dict):
                title = item.get("title") or item.get("name", "—")
                link = item.get("link") or item.get("url", "#")
                snippet = item.get("snippet") or item.get("description", "")
            else:
                continue
            
            domain = domain_from_url(link)
            date_info = extract_date(link, snippet, mode=mode)
            
            if date_info != "—":
                data.append({
                    "Title": clean_text(title),
                    "Domain": domain,
                    "Description": clean_text(snippet),
                    "Date Info": date_info,
                    "URL": link
                })
        
        time.sleep(POLITE_DELAY)
    
    return data, queries_used

def collect_experts(queries, max_queries=15):
    """Collect expert contacts"""
    data = []
    queries_used = 0
    name_pat = re.compile(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)+")
    
    for q in queries[:max_queries]:
        if queries_used >= max_queries:
            break
        
        print(f"  Searching: {q}")
        items = google_search(q, num=5)
        queries_used += 1
        
        for item in items:
            if not isinstance(item, dict):
                continue
            
            title = item.get("title") or item.get("name", "")
            link = item.get("link") or item.get("url", "#")
            snippet = item.get("snippet") or item.get("description", "")
            
            if not name_pat.match(title):
                continue
            
            role = "—"
            if " at " in snippet:
                role = snippet.split(" at ")[0].strip().title()
            
            data.append({
                "Name": title,
                "Role": role,
                "LinkedIn": link
            })
        
        time.sleep(POLITE_DELAY)
    
    return data, queries_used

def append_to_csv(filepath, fieldnames, new_data):
    """Append new data to CSV, avoiding duplicates"""
    # Load existing data
    existing_data = []
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_data = list(reader)
    
    # Create set of existing items (by title or name)
    key_field = "Name" if "Name" in fieldnames else "Title"
    existing_keys = {row[key_field] for row in existing_data}
    
    # Add only new items
    new_items = [item for item in new_data if item.get(key_field, "") not in existing_keys]
    
    # Write all data back
    all_data = existing_data + new_items
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)
    
    return len(new_items)

# ---------------------- EMAIL GENERATION ----------------------
from email_template import generate_email_html

def send_email(html_content, subject):
    """Send email via SMTP"""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("❌ Email credentials not configured!")
        print("Set SENDER_EMAIL and SENDER_PASSWORD environment variables")
        return False
    
    if not RECIPIENT_EMAILS or RECIPIENT_EMAILS == ['']:
        print("❌ No recipient emails configured!")
        print("Set RECIPIENT_EMAILS environment variable")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(RECIPIENT_EMAILS)
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent successfully to {len(RECIPIENT_EMAILS)} recipients")
        return True
    
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def clear_weekly_data():
    """Clear all CSV files after email is sent"""
    for file in [GRANTS_FILE, EVENTS_FILE, CSR_FILE, EXPERTS_FILE]:
        if file.exists():
            file.unlink()
    print("🗑️  Weekly data cleared")

# ---------------------- MAIN EXECUTION ----------------------
def main():
    print("=" * 70)
    print("🌍 CLIMATE CARDINALS - AUTOMATED WEEKLY NEWSLETTER")
    print("=" * 70)
    
    # Load state
    state = load_state()
    state = reset_daily_counter(state)
    
    today = datetime.now()
    print(f"\n📅 Date: {today.strftime('%A, %B %d, %Y')}")
    print(f"📊 Queries used today: {state['queries_used_today']}/{DAILY_QUERY_LIMIT}")
    
    # Check if we should send email (Monday)
    if should_send_email(state):
        print("\n📧 It's Monday! Sending weekly newsletter...")
        
        # Load accumulated data
        try:
            experts_df = pd.read_csv(EXPERTS_FILE) if EXPERTS_FILE.exists() else pd.DataFrame()
            grants_df = pd.read_csv(GRANTS_FILE) if GRANTS_FILE.exists() else pd.DataFrame()
            events_df = pd.read_csv(EVENTS_FILE) if EVENTS_FILE.exists() else pd.DataFrame()
            csr_df = pd.read_csv(CSR_FILE) if CSR_FILE.exists() else pd.DataFrame()
            
            # Generate and send email
            html_content = generate_email_html(experts_df, grants_df, events_df, csr_df)
            subject = f"Climate Cardinals Weekly Intelligence - {today.strftime('%B %d, %Y')}"
            
            if send_email(html_content, subject):
                state["last_email_sent"] = today.strftime("%Y-%m-%d")
                state["week_start_date"] = today.strftime("%Y-%m-%d")
                clear_weekly_data()
            
        except Exception as e:
            print(f"❌ Error generating/sending email: {e}")
    
    else:
        # Not Monday, collect daily data
        print(f"\n📥 Collecting data for the week (Day {today.weekday() + 1}/7)")
        
        remaining_queries = DAILY_QUERY_LIMIT - state['queries_used_today']
        if remaining_queries <= 0:
            print("⚠️  Daily query limit reached. Skipping collection.")
            save_state(state)
            return
        
        # Distribute queries across categories
        queries_per_category = remaining_queries // 4
        
        print(f"\n💰 Collecting Grants ({queries_per_category} queries)...")
        grants_data, used = collect_data(ALL_GRANT_KEYWORDS, mode="future", max_queries=queries_per_category)
        new_grants = append_to_csv(GRANTS_FILE, ["Title", "Domain", "Description", "Date Info", "URL"], grants_data)
        state['queries_used_today'] += used
        print(f"   Added {new_grants} new grants")
        
        print(f"\n📅 Collecting Events ({queries_per_category} queries)...")
        events_data, used = collect_data(ALL_EVENT_KEYWORDS, mode="future", max_queries=queries_per_category)
        new_events = append_to_csv(EVENTS_FILE, ["Title", "Domain", "Description", "Date Info", "URL"], events_data)
        state['queries_used_today'] += used
        print(f"   Added {new_events} new events")
        
        print(f"\n📊 Collecting CSR Reports ({queries_per_category} queries)...")
        csr_data, used = collect_data(ALL_CSR_KEYWORDS, mode="past", max_queries=queries_per_category)
        new_csr = append_to_csv(CSR_FILE, ["Title", "Domain", "Description", "Date Info", "URL"], csr_data)
        state['queries_used_today'] += used
        print(f"   Added {new_csr} new reports")
        
        print(f"\n👥 Collecting Experts ({queries_per_category} queries)...")
        experts_data, used = collect_experts(ALL_EXPERT_QUERIES, max_queries=queries_per_category)
        new_experts = append_to_csv(EXPERTS_FILE, ["Name", "Role", "LinkedIn"], experts_data)
        state['queries_used_today'] += used
        print(f"   Added {new_experts} new experts")
        
        print(f"\n📊 Total queries used today: {state['queries_used_today']}/{DAILY_QUERY_LIMIT}")
    
    # Save state
    save_state(state)
    print("\n✅ Daily run complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
