#!/usr/bin/env python3
"""
Quick test script to verify your setup
"""

import os
import sys

print("=" * 70)
print("🌍 CLIMATE CARDINALS - SETUP VERIFICATION")
print("=" * 70)

# Check Python version
print(f"\n✓ Python version: {sys.version}")

# Check dependencies
missing_deps = []
try:
    import requests
    print("✓ requests installed")
except ImportError:
    missing_deps.append("requests")
    print("✗ requests NOT installed")

try:
    import pandas
    print("✓ pandas installed")
except ImportError:
    missing_deps.append("pandas")
    print("✗ pandas NOT installed")

try:
    from bs4 import BeautifulSoup
    print("✓ beautifulsoup4 installed")
except ImportError:
    missing_deps.append("beautifulsoup4")
    print("✗ beautifulsoup4 NOT installed")

try:
    from dateutil import parser
    print("✓ python-dateutil installed")
except ImportError:
    missing_deps.append("python-dateutil")
    print("✗ python-dateutil NOT installed")

if missing_deps:
    print(f"\n⚠️  Missing dependencies: {', '.join(missing_deps)}")
    print("Run: pip install -r requirements.txt")
else:
    print("\n✓ All dependencies installed!")

# Check environment variables
print("\n" + "=" * 70)
print("ENVIRONMENT VARIABLES")
print("=" * 70)

required_vars = {
    "RAPIDAPI_KEY": "RapidAPI Key for Real-Time Web Search",
    "SENDER_EMAIL": "Email to send from",
    "SENDER_PASSWORD": "Email app password",
    "RECIPIENT_EMAILS": "Email recipients (comma-separated)"
}

missing_vars = []
for var, description in required_vars.items():
    value = os.getenv(var)
    if value:
        # Mask sensitive values
        if "PASSWORD" in var or "KEY" in var:
            masked = value[:4] + "*" * (len(value) - 8) + value[-4:] if len(value) > 8 else "****"
            print(f"✓ {var}: {masked}")
        else:
            print(f"✓ {var}: {value}")
    else:
        missing_vars.append(var)
        print(f"✗ {var}: NOT SET ({description})")

if missing_vars:
    print(f"\n⚠️  Missing environment variables!")
    print("\nSet them using:")
    print("  export VARIABLE_NAME=value")
    print("\nOr create .env file:")
    print("  cp .env.example .env")
    print("  # Edit .env with your values")
else:
    print("\n✓ All environment variables configured!")

# Test RapidAPI connection
print("\n" + "=" * 70)
print("RAPIDAPI CONNECTION TEST")
print("=" * 70)

if not missing_vars and not missing_deps:
    try:
        import requests
        rapidapi_key = os.getenv("RAPIDAPI_KEY")
        
        url = "https://real-time-web-search.p.rapidapi.com/search"
        headers = {
            "x-rapidapi-key": rapidapi_key,
            "x-rapidapi-host": "real-time-web-search.p.rapidapi.com"
        }
        params = {
            "q": "climate change",
            "num": "3",
            "start": "0",
            "gl": "us",
            "hl": "en"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            print("✓ RapidAPI connection successful!")
            data = response.json()
            results = data.get("data", [])
            if results:
                print(f"✓ Search working - found {len(results)} results")
                print(f"\nSample result:")
                print(f"  Title: {results[0].get('title', 'N/A')[:60]}...")
                print(f"  URL: {results[0].get('url', 'N/A')[:60]}...")
            else:
                print("⚠️  No results returned - but API is working")
        elif response.status_code == 429:
            print(f"⚠️  Rate limit exceeded (429) - API key is valid but quota used")
            print(f"   System will automatically fallback to DuckDuckGo")
        elif response.status_code == 403:
            print(f"✗ API authentication failed (403)")
            print(f"   Check your RAPIDAPI_KEY is correct")
            print(f"   Make sure you're subscribed to Real-Time Web Search API")
        else:
            print(f"✗ API error: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
    except Exception as e:
        print(f"✗ API test failed: {e}")
else:
    print("⚠️  Skipping API test - dependencies or environment variables missing")

# Test DuckDuckGo fallback
print("\n" + "=" * 70)
print("DUCKDUCKGO FALLBACK TEST")
print("=" * 70)

if not missing_deps:
    try:
        import requests
        from bs4 import BeautifulSoup
        from urllib.parse import quote_plus
        
        url = f"https://html.duckduckgo.com/html/?q={quote_plus('climate grants')}"
        headers_ddg = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.get(url, headers=headers_ddg, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select(".result")[:3]
        
        if results:
            print(f"✓ DuckDuckGo fallback working - found {len(results)} results")
            print("✓ Backup search system operational")
        else:
            print("⚠️  DuckDuckGo returned no results - may need different parsing")
            print("   This is OK - primary API is RapidAPI")
            
    except Exception as e:
        print(f"⚠️  DuckDuckGo test failed: {e}")
        print("   This is OK if RapidAPI is working")
else:
    print("⚠️  Skipping DuckDuckGo test - dependencies missing")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if not missing_deps and not missing_vars:
    print("\n✅ SETUP COMPLETE!")
    print("\nYou're ready to run the newsletter:")
    print("  python automated_newsletter.py")
    print("\nOr deploy to GitHub Actions:")
    print("  1. Push code to GitHub")
    print("  2. Add secrets in Settings → Secrets → Actions:")
    print("     - RAPIDAPI_KEY")
    print("     - SENDER_EMAIL")
    print("     - SENDER_PASSWORD")
    print("     - RECIPIENT_EMAILS")
    print("  3. Enable workflows in Actions tab")
    print("\nFor detailed instructions, see DEPLOYMENT_GUIDE.md")
else:
    print("\n⚠️  SETUP INCOMPLETE")
    if missing_deps:
        print(f"\n1. Install missing dependencies:")
        print(f"   pip install -r requirements.txt")
    if missing_vars:
        print(f"\n2. Configure environment variables:")
        print(f"   See RAPIDAPI_SETUP.md for getting your API key")
        print(f"   cp .env.example .env")
        print(f"   # Edit .env file with your credentials")

print("\n" + "=" * 70)

