"""
Email template generation for Climate Cardinals newsletter
"""

import pandas as pd

def is_valid_data(value):
    if pd.isna(value) or value in ["—", "", "N/A", "None", "#"]:
        return False
    return str(value).strip() != ""

def truncate_text(text, max_length=150):
    if len(str(text)) > max_length:
        return str(text)[:max_length] + "..."
    return str(text)

def generate_expert_card(row):
    name = row.get('Name', 'Unknown')
    role = row.get('Role', '')
    linkedin = row.get('LinkedIn', '')
    
    role_html = f'<div class="expert-role">{role}</div>' if is_valid_data(role) else ''
    linkedin_html = f'''<a href="{linkedin}" class="expert-link">
        <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
        </svg>
        View LinkedIn
    </a>''' if is_valid_data(linkedin) else ''
    
    return f'''<div class="expert-card">
        <div class="expert-header">
            <div class="expert-avatar">👤</div>
            <div class="expert-info">
                <div class="expert-name">{name}</div>
                {role_html}
            </div>
        </div>
        {linkedin_html}
    </div>'''

def generate_opportunity_card(row, card_type="Grant"):
    title = truncate_text(row.get('Title', 'Untitled'), 90)
    description = truncate_text(row.get('Description', ''), 160)
    domain = row.get('Domain', '')
    date_info = row.get('Date Info', '')
    url = row.get('URL', '')
    
    date_html = f'<div class="meta-item"><span class="meta-icon">📅</span>{date_info}</div>' if is_valid_data(date_info) else ''
    domain_html = f'<div class="meta-item"><span class="meta-icon">🌐</span>{domain}</div>' if is_valid_data(domain) else ''
    url_html = f'<a href="{url}" class="card-link">Read Full Article</a>' if is_valid_data(url) else ''
    
    return f'''<div class="opportunity-card">
        <div class="card-header">
            <div class="card-title">{title}</div>
        </div>
        <div class="card-meta">
            {date_html}
            {domain_html}
        </div>
        <div class="card-description">{description}</div>
        {url_html}
    </div>'''

def generate_section_cards(df, card_type, generator_func):
    if df.empty:
        return '''<div class="no-data">
            <div class="no-data-icon">📭</div>
            <div class="no-data-text">No items curated this week</div>
        </div>'''
    
    cards_html = ""
    for _, row in df.iterrows():
        if card_type == "Expert":
            cards_html += generator_func(row)
        else:
            cards_html += generator_func(row, card_type)
    
    return cards_html

def generate_email_html(experts_df, grants_df, events_df, csr_df):
    """Generate premium magazine-style newsletter email."""
    today_str = pd.Timestamp.today().strftime("%B %d, %Y")
    week_num = pd.Timestamp.today().isocalendar()[1]
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Climate Cardinals Weekly Intelligence</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --forest-dark: #0a2f1f;
            --forest-medium: #1a5538;
            --forest-light: #2d7555;
            --earth-brown: #8b7355;
            --cream: #faf8f5;
            --warm-white: #ffffff;
            --sage: #9caf88;
            --terracotta: #c77355;
            --gold: #d4a574;
            --mist: #e8ece9;
            --shadow: rgba(10, 47, 31, 0.08);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(180deg, var(--mist) 0%, var(--cream) 100%);
            margin: 0;
            padding: 50px 20px;
            line-height: 1.75;
            color: var(--forest-dark);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        .container {{
            max-width: 720px;
            margin: 0 auto;
            background: var(--warm-white);
            box-shadow: 
                0 2px 4px rgba(0, 0, 0, 0.02),
                0 4px 8px rgba(0, 0, 0, 0.03),
                0 8px 16px rgba(0, 0, 0, 0.04),
                0 24px 48px rgba(0, 0, 0, 0.06);
            position: relative;
        }}
        
        .container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(90deg, 
                var(--forest-dark) 0%, 
                var(--forest-medium) 25%, 
                var(--sage) 50%, 
                var(--terracotta) 75%, 
                var(--gold) 100%);
        }}
        
        .masthead {{
            padding: 60px 50px 50px;
            background: 
                linear-gradient(135deg, rgba(156, 175, 136, 0.03) 0%, transparent 100%),
                var(--warm-white);
            border-bottom: 1px solid rgba(10, 47, 31, 0.08);
            position: relative;
        }}
        
        .masthead::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 50px;
            right: 50px;
            height: 1px;
            background: linear-gradient(90deg, 
                transparent 0%, 
                var(--forest-medium) 50%, 
                transparent 100%);
        }}
        
        .issue-label {{
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--forest-medium);
            margin-bottom: 16px;
            opacity: 0.7;
        }}
        
        .masthead-title {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 52px;
            font-weight: 900;
            line-height: 1.1;
            color: var(--forest-dark);
            margin: 0 0 16px 0;
            letter-spacing: -1.5px;
        }}
        
        .masthead-subtitle {{
            font-size: 18px;
            font-weight: 300;
            color: var(--forest-medium);
            margin: 0 0 24px 0;
            line-height: 1.5;
            font-style: italic;
        }}
        
        .date-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 20px;
            border-top: 1px solid var(--mist);
        }}
        
        .date-text {{
            font-size: 13px;
            font-weight: 500;
            color: var(--earth-brown);
            letter-spacing: 0.5px;
        }}
        
        .issue-number {{
            font-size: 12px;
            font-weight: 600;
            color: var(--forest-medium);
            background: var(--mist);
            padding: 6px 14px;
            border-radius: 20px;
            letter-spacing: 0.5px;
        }}
        
        .editorial {{
            padding: 50px;
            background: linear-gradient(135deg, var(--mist) 0%, rgba(250, 248, 245, 0.5) 100%);
            border-bottom: 3px double var(--mist);
        }}
        
        .editorial-header {{
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--terracotta);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .editorial-header::before {{
            content: '';
            width: 30px;
            height: 2px;
            background: var(--terracotta);
        }}
        
        .editorial-text {{
            font-size: 16px;
            line-height: 1.8;
            color: var(--forest-dark);
            font-weight: 400;
        }}
        
        .section {{
            padding: 60px 50px;
            border-bottom: 1px solid var(--mist);
            position: relative;
        }}
        
        .section:last-of-type {{
            border-bottom: none;
        }}
        
        .section-header {{
            margin-bottom: 40px;
            position: relative;
        }}
        
        .section-kicker {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            color: var(--forest-medium);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section-divider {{
            width: 40px;
            height: 2px;
            background: linear-gradient(90deg, var(--forest-medium) 0%, transparent 100%);
        }}
        
        .section-title {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 36px;
            font-weight: 700;
            line-height: 1.2;
            color: var(--forest-dark);
            margin: 0 0 8px 0;
            letter-spacing: -0.5px;
        }}
        
        .section-description {{
            font-size: 15px;
            color: var(--forest-medium);
            font-weight: 400;
            line-height: 1.6;
            max-width: 560px;
        }}
        
        .item-count {{
            position: absolute;
            top: -10px;
            right: 0;
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 72px;
            font-weight: 900;
            color: var(--mist);
            line-height: 1;
            pointer-events: none;
            user-select: none;
        }}
        
        .expert-card {{
            background: linear-gradient(135deg, rgba(156, 175, 136, 0.04) 0%, transparent 100%);
            border: 1px solid rgba(156, 175, 136, 0.15);
            border-left: 4px solid var(--sage);
            padding: 28px;
            margin-bottom: 20px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }}
        
        .expert-card:hover {{
            transform: translateX(4px);
            border-left-color: var(--forest-medium);
            background: linear-gradient(135deg, rgba(156, 175, 136, 0.08) 0%, transparent 100%);
            box-shadow: -4px 0 0 0 var(--forest-medium), 0 4px 12px var(--shadow);
        }}
        
        .expert-card:last-child {{
            margin-bottom: 0;
        }}
        
        .expert-header {{
            display: flex;
            gap: 20px;
            margin-bottom: 16px;
            align-items: flex-start;
        }}
        
        .expert-avatar {{
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, var(--sage) 0%, var(--forest-medium) 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            flex-shrink: 0;
            box-shadow: 0 4px 12px rgba(156, 175, 136, 0.2);
            border: 3px solid var(--warm-white);
        }}
        
        .expert-info {{
            flex: 1;
            padding-top: 4px;
        }}
        
        .expert-name {{
            font-size: 20px;
            font-weight: 700;
            color: var(--forest-dark);
            margin: 0 0 6px 0;
            letter-spacing: -0.3px;
            line-height: 1.3;
        }}
        
        .expert-role {{
            font-size: 14px;
            color: var(--forest-medium);
            font-weight: 500;
            line-height: 1.5;
        }}
        
        .expert-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--forest-medium);
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            padding: 10px 18px;
            background: var(--warm-white);
            border: 1px solid rgba(156, 175, 136, 0.3);
            border-radius: 6px;
            transition: all 0.3s ease;
            letter-spacing: 0.3px;
        }}
        
        .expert-link:hover {{
            background: var(--sage);
            color: var(--warm-white);
            border-color: var(--sage);
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(156, 175, 136, 0.25);
        }}
        
        .expert-link svg {{
            width: 14px;
            height: 14px;
        }}
        
        .opportunity-card {{
            background: var(--warm-white);
            border: 1px solid var(--mist);
            padding: 32px;
            margin-bottom: 24px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .opportunity-card::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: linear-gradient(180deg, var(--forest-dark) 0%, var(--terracotta) 100%);
            transform: scaleY(0);
            transform-origin: top;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .opportunity-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px var(--shadow);
            border-color: rgba(10, 47, 31, 0.15);
        }}
        
        .opportunity-card:hover::before {{
            transform: scaleY(1);
        }}
        
        .opportunity-card:last-child {{
            margin-bottom: 0;
        }}
        
        .card-header {{
            margin-bottom: 16px;
        }}
        
        .card-title {{
            font-size: 20px;
            font-weight: 700;
            color: var(--forest-dark);
            margin: 0 0 14px 0;
            line-height: 1.4;
            letter-spacing: -0.3px;
        }}
        
        .card-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--mist);
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: var(--earth-brown);
            font-weight: 500;
        }}
        
        .meta-icon {{
            font-size: 16px;
            opacity: 0.8;
        }}
        
        .card-description {{
            font-size: 15px;
            color: var(--forest-medium);
            line-height: 1.7;
            margin-bottom: 20px;
        }}
        
        .card-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--warm-white);
            background: var(--forest-dark);
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            padding: 11px 22px;
            border-radius: 6px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            letter-spacing: 0.5px;
        }}
        
        .card-link:hover {{
            background: var(--forest-medium);
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(10, 47, 31, 0.2);
        }}
        
        .card-link::after {{
            content: '→';
            font-size: 16px;
            transition: transform 0.3s ease;
        }}
        
        .card-link:hover::after {{
            transform: translateX(3px);
        }}
        
        .no-data {{
            text-align: center;
            padding: 60px 40px;
            background: linear-gradient(135deg, var(--mist) 0%, rgba(250, 248, 245, 0.3) 100%);
            border: 2px dashed rgba(156, 175, 136, 0.3);
            border-radius: 8px;
        }}
        
        .no-data-icon {{
            font-size: 48px;
            margin-bottom: 16px;
            opacity: 0.4;
        }}
        
        .no-data-text {{
            font-size: 15px;
            color: var(--earth-brown);
            font-style: italic;
        }}
        
        .footer {{
            padding: 60px 50px;
            background: linear-gradient(135deg, var(--forest-dark) 0%, var(--forest-medium) 100%);
            color: var(--warm-white);
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .footer::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg width="60" height="60" xmlns="http://www.w3.org/2000/svg"><circle cx="30" cy="30" r="25" fill="none" stroke="rgba(255,255,255,0.02)" stroke-width="1"/></svg>');
            opacity: 0.5;
        }}
        
        .footer-content {{
            position: relative;
            z-index: 1;
        }}
        
        .footer-logo {{
            font-size: 42px;
            margin-bottom: 20px;
            filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.2));
        }}
        
        .footer-title {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 10px 0;
            letter-spacing: -0.5px;
        }}
        
        .footer-tagline {{
            font-size: 14px;
            opacity: 0.8;
            margin: 0 0 24px 0;
            font-weight: 300;
            letter-spacing: 0.5px;
        }}
        
        .footer-divider {{
            width: 60px;
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, var(--gold) 50%, transparent 100%);
            margin: 24px auto;
        }}
        
        .footer-info {{
            font-size: 12px;
            opacity: 0.6;
            margin-top: 16px;
            font-weight: 400;
        }}
        
        @media (max-width: 640px) {{
            body {{
                padding: 20px 10px;
            }}
            
            .masthead {{
                padding: 40px 30px 35px;
            }}
            
            .masthead-title {{
                font-size: 38px;
            }}
            
            .section {{
                padding: 40px 30px;
            }}
            
            .section-title {{
                font-size: 28px;
            }}
            
            .item-count {{
                font-size: 48px;
                opacity: 0.5;
            }}
            
            .editorial {{
                padding: 35px 30px;
            }}
            
            .opportunity-card, .expert-card {{
                padding: 24px;
            }}
            
            .footer {{
                padding: 45px 30px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="masthead">
            <div class="issue-label">Weekly Intelligence • Issue #{week_num}</div>
            <h1 class="masthead-title">Climate Cardinals</h1>
            <p class="masthead-subtitle">Curated opportunities for climate action leaders</p>
            <div class="date-bar">
                <div class="date-text">📅 {today_str}</div>
                <div class="issue-number">Week {week_num}</div>
            </div>
        </div>
        
        <div class="editorial">
            <div class="editorial-header">This Week's Focus</div>
            <p class="editorial-text">This week's intelligence brings you {len(grants_df)} new funding opportunities, {len(events_df)} upcoming climate events, {len(experts_df)} expert connections, and {len(csr_df)} fresh sustainability reports. Each opportunity has been carefully curated to help you make meaningful climate impact.</p>
        </div>
        
        <div class="section">
            <div class="item-count">{len(experts_df):02d}</div>
            <div class="section-header">
                <div class="section-kicker">
                    <div class="section-divider"></div>
                    Network & Connect
                </div>
                <h2 class="section-title">Climate Experts</h2>
                <p class="section-description">Influential leaders and decision-makers in the climate space actively seeking partnerships and collaboration.</p>
            </div>
            {generate_section_cards(experts_df, "Expert", generate_expert_card)}
        </div>
        
        <div class="section">
            <div class="item-count">{len(grants_df):02d}</div>
            <div class="section-header">
                <div class="section-kicker">
                    <div class="section-divider"></div>
                    Funding Opportunities
                </div>
                <h2 class="section-title">Grants & Funding</h2>
                <p class="section-description">Active grant programs and funding opportunities to accelerate your climate initiatives.</p>
            </div>
            {generate_section_cards(grants_df, "Grant", generate_opportunity_card)}
        </div>
        
        <div class="section">
            <div class="item-count">{len(events_df):02d}</div>
            <div class="section-header">
                <div class="section-kicker">
                    <div class="section-divider"></div>
                    Upcoming Events
                </div>
                <h2 class="section-title">Events & Conferences</h2>
                <p class="section-description">Premier gatherings where climate leaders convene to share insights and forge partnerships.</p>
            </div>
            {generate_section_cards(events_df, "Event", generate_opportunity_card)}
        </div>
        
        <div class="section">
            <div class="item-count">{len(csr_df):02d}</div>
            <div class="section-header">
                <div class="section-kicker">
                    <div class="section-divider"></div>
                    Intelligence Reports
                </div>
                <h2 class="section-title">ESG & Sustainability Reports</h2>
                <p class="section-description">Latest corporate sustainability disclosures and environmental impact assessments.</p>
            </div>
            {generate_section_cards(csr_df, "CSR", generate_opportunity_card)}
        </div>
        
        <div class="footer">
            <div class="footer-content">
                <div class="footer-logo">🌍</div>
                <h3 class="footer-title">Climate Cardinals</h3>
                <p class="footer-tagline">Empowering the next generation of climate leaders</p>
                <div class="footer-divider"></div>
                <p class="footer-info">© 2026 Climate Cardinals • Weekly Intelligence Report</p>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    return html_content
