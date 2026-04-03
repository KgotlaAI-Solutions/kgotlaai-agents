#!/usr/bin/env python3
"""
Kgotla AI - Lead Hunter Agent
Automated lead generation for industrial AI consultancy
Targets: Mining, Manufacturing, Power, Government, Logistics, Heavy Industry
Regions: South Africa, SADC, expanding outward
"""

import json
import time
import random
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote_plus
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class LeadHunter:
    def __init__(self, config_path='../shared-config/config.json'):
        self.config = self._load_config(config_path)
        self.leads_db = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Industry-specific decision makers
        self.decision_makers = {
            'mining': ['CTO', 'Head of Innovation', 'Digital Transformation Lead', 'Mine Manager', 'Operations Director', 'Technical Services Manager'],
            'manufacturing': ['Plant Manager', 'Operations Manager', 'IT Director', 'Industry 4.0 Lead', 'Production Manager'],
            'power': ['Engineering Manager', 'Grid Operations Director', 'Digital Strategy Lead', 'Asset Manager'],
            'government': ['CIO', 'Head of IT', 'Digital Transformation Director', 'Systems Administrator'],
            'logistics': ['Supply Chain Director', 'Operations Manager', 'Fleet Manager', 'Technology Lead'],
            'heavy_industry': ['General Manager', 'Technical Director', 'Innovation Lead', 'Process Engineer']
        }
        
        # Target companies by sector (starter list)
        self.target_companies = {
            'mining': [
                'Anglo American', 'Sibanye-Stillwater', 'Harmony Gold', 'Gold Fields', 
                'Impala Platinum', 'Northam Platinum', 'Exxaro', 'South32', 'Kumba Iron Ore',
                'African Rainbow Minerals', 'Royal Bafokeng Platinum', 'Tharisa', 'Jubilee Metals'
            ],
            'manufacturing': [
                'ArcelorMittal', 'Pepkor', 'Tiger Brands', 'Pioneer Foods', 'Distell',
                'Sappi', 'Mondi', 'Nampak', 'Barloworld', 'Invicta Holdings'
            ],
            'power': [
                'Eskom', 'City Power', 'Ethekwini Electricity', 'Cape Town Electricity',
                'Johannesburg Water', 'Rand Water', 'Transnet Pipelines'
            ],
            'logistics': [
                'Transnet', 'Imperial Logistics', 'Barloworld Logistics', 'Super Group',
                'Cargo Carriers', 'Unitrans', 'Value Logistics'
            ],
            'heavy_industry': [
                'Sasol', 'PetroSA', 'Engen', 'Shell SA', 'BP Southern Africa',
                'TotalEnergies', 'Aveng', 'Murray & Roberts', 'Stefanutti Stocks'
            ]
        }
        
        # Job keywords that indicate AI/automation needs
        self.job_keywords = [
            'automation', 'artificial intelligence', 'machine learning', 'AI', 'digital transformation',
            'predictive maintenance', ' Industry 4.0', 'IoT', 'data analytics', 'process optimization',
            'intelligent systems', 'cognitive computing', 'RPA', 'robotic process automation',
            'computer vision', 'natural language processing', 'operational technology'
        ]
    
    def _load_config(self, path):
        """Load configuration or create default"""
        default_config = {
            'email': 'mahlo@kgotlaai.co.za',
            'linkedin_url': 'https://www.linkedin.com/in/mahlo-kgotleng-473830194',
            'company_name': 'Kgotla AI',
            'sender_name': 'Mahlo Kgotleng',
            'output_dir': './leads_output',
            'daily_lead_target': 50,
            'follow_up_days': [3, 7, 14]
        }
        
        if os.path.exists(path):
            with open(path, 'r') as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def scrape_linkedin_jobs(self, keywords=None, location='South Africa'):
        """Scrape LinkedIn for relevant job postings"""
        if keywords is None:
            keywords = self.job_keywords[:5]  # Use top 5 keywords
        
        leads = []
        
        for keyword in keywords:
            try:
                search_url = f"https://www.linkedin.com/jobs/search?keywords={quote_plus(keyword)}&location={quote_plus(location)}"
                response = self.session.get(search_url, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    job_cards = soup.find_all('div', class_='base-card')
                    
                    for card in job_cards[:10]:  # Limit to 10 per keyword
                        try:
                            title = card.find('h3', class_='base-search-card__title')
                            company = card.find('h4', class_='base-search-card__subtitle')
                            location_elem = card.find('span', class_='job-search-card__location')
                            
                            if title and company:
                                lead = {
                                    'source': 'LinkedIn Jobs',
                                    'job_title': title.text.strip(),
                                    'company': company.text.strip(),
                                    'location': location_elem.text.strip() if location_elem else location,
                                    'keyword_matched': keyword,
                                    'date_found': datetime.now().isoformat(),
                                    'status': 'new',
                                    'priority': self._calculate_priority(company.text.strip(), keyword),
                                    'search_url': search_url
                                }
                                leads.append(lead)
                        except Exception as e:
                            continue
                            
                time.sleep(random.uniform(2, 4))  # Be respectful
                
            except Exception as e:
                print(f"Error scraping LinkedIn for {keyword}: {e}")
                continue
        
        return leads
    
    def search_government_tenders(self):
        """Search for government IT/AI tenders"""
        tenders = []
        
        # ETenders South Africa
        try:
            etenders_url = "https://etenders.gov.za/Home/opportunities?id=1"
            response = self.session.get(etenders_url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                tender_rows = soup.find_all('tr', class_=['table-row-odd', 'table-row-even'])
                
                for row in tender_rows[:15]:
                    try:
                        cells = row.find_all('td')
                        if len(cells) >= 4:
                            description = cells[2].text.strip().lower()
                            
                            # Check if relevant to AI/automation
                            if any(kw in description for kw in ['software', 'technology', 'automation', 'digital', 'system', 'IT', 'artificial intelligence']):
                                tender = {
                                    'source': 'ETenders SA',
                                    'tender_number': cells[0].text.strip(),
                                    'department': cells[1].text.strip(),
                                    'description': cells[2].text.strip(),
                                    'closing_date': cells[3].text.strip(),
                                    'date_found': datetime.now().isoformat(),
                                    'status': 'new',
                                    'priority': 'high' if any(x in description for x in ['automation', 'artificial intelligence', 'AI']) else 'medium',
                                    'url': 'https://etenders.gov.za'
                                }
                                tenders.append(tender)
                    except:
                        continue
        except Exception as e:
            print(f"Error scraping ETenders: {e}")
        
        return tenders
    
    def generate_company_leads(self):
        """Generate leads from target company list"""
        leads = []
        
        for sector, companies in self.target_companies.items():
            for company in companies:
                # Create multiple lead variations per company
                for role in self.decision_makers.get(sector, self.decision_makers['heavy_industry'])[:3]:
                    lead = {
                        'source': 'Target Company List',
                        'company': company,
                        'sector': sector,
                        'target_role': role,
                        'linkedin_search': f"https://www.linkedin.com/search/results/people/?keywords={quote_plus(company + ' ' + role)}&origin=GLOBAL_SEARCH_HEADER",
                        'date_found': datetime.now().isoformat(),
                        'status': 'new',
                        'priority': 'high',
                        'notes': f"Direct outreach to {role} at {company}"
                    }
                    leads.append(lead)
        
        return leads
    
    def _calculate_priority(self, company_name, keyword):
        """Calculate lead priority based on company and keyword"""
        high_value_keywords = ['artificial intelligence', 'AI', 'automation', 'predictive maintenance', 'digital transformation']
        
        if any(hv in keyword.lower() for hv in high_value_keywords):
            return 'high'
        elif any(target in company_name.lower() for target in [x.lower() for sublist in self.target_companies.values() for x in sublist]):
            return 'high'
        else:
            return 'medium'
    
    def draft_cold_email(self, lead):
        """Draft personalized cold email for a lead"""
        company = lead.get('company', 'your organization')
        sector = lead.get('sector', 'industry')
        role = lead.get('target_role', 'there')
        
        # Sector-specific pain points
        pain_points = {
            'mining': 'unplanned equipment downtime and safety incidents costing millions',
            'manufacturing': 'production inefficiencies and quality control challenges',
            'power': 'grid instability and asset management complexity',
            'government': 'legacy systems and service delivery bottlenecks',
            'logistics': 'supply chain visibility and fleet optimization',
            'heavy_industry': 'operational complexity and safety compliance'
        }
        
        pain = pain_points.get(sector, 'operational challenges and inefficiencies')
        
        email_template = f"""Subject: {company} - AI Solutions for {sector.title()} Operations

Hi {role},

I noticed {company} is actively investing in {lead.get('keyword_matched', 'technology and innovation')}.

I'm Mahlo Kgotleng, founder of Kgotla AI. We specialize in AI-driven solutions for {sector} operations—specifically addressing {pain}.

Recent wins:
• Reduced equipment downtime by 35% for a mining client using predictive maintenance AI
• Automated compliance reporting saving 200+ hours/month for a power utility
• Built intelligent safety monitoring reducing incidents by 40%

I'd love to explore how we can deliver similar results for {company}. 

Worth a 15-minute call this week?

Best,
Mahlo Kgotleng
Founder, Kgotla AI
{self.config['linkedin_url']}
P.S. We're currently offering 50% equity partnerships for Enterprise Development—happy to share details.
"""
        
        return email_template
    
    def save_leads(self, leads, filename=None):
        """Save leads to CSV and JSON"""
        if filename is None:
            filename = f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        os.makedirs(self.config['output_dir'], exist_ok=True)
        
        # Save as JSON
        json_path = os.path.join(self.config['output_dir'], f"{filename}.json")
        with open(json_path, 'w') as f:
            json.dump(leads, f, indent=2)
        
        # Save as CSV
        csv_path = os.path.join(self.config['output_dir'], f"{filename}.csv")
        df = pd.DataFrame(leads)
        df.to_csv(csv_path, index=False)
        
        print(f"Saved {len(leads)} leads to:")
        print(f"  JSON: {json_path}")
        print(f"  CSV: {csv_path}")
        
        return json_path, csv_path
    
    def run_daily_hunt(self):
        """Execute complete daily lead generation"""
        print(f"\n{'='*60}")
        print(f"🎯 Kgotla AI Lead Hunter - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}\n")
        
        all_leads = []
        
        # 1. Scrape LinkedIn Jobs
        print("🔍 Hunting LinkedIn Jobs...")
        linkedin_leads = self.scrape_linkedin_jobs()
        all_leads.extend(linkedin_leads)
        print(f"   Found {len(linkedin_leads)} leads from LinkedIn\n")
        
        # 2. Search Government Tenders
        print("📋 Checking Government Tenders...")
        tender_leads = self.search_government_tenders()
        all_leads.extend(tender_leads)
        print(f"   Found {len(tender_leads)} relevant tenders\n")
        
        # 3. Generate Target Company Leads
        print("🏢 Building Target Company List...")
        company_leads = self.generate_company_leads()
        all_leads.extend(company_leads)
        print(f"   Generated {len(company_leads)} company targets\n")
        
        # 4. Draft emails for high-priority leads
        print("✉️  Drafting outreach emails...")
        high_priority = [l for l in all_leads if l.get('priority') == 'high'][:20]
        for lead in high_priority:
            lead['draft_email'] = self.draft_cold_email(lead)
        print(f"   Drafted {len(high_priority)} personalized emails\n")
        
        # 5. Save everything
        json_path, csv_path = self.save_leads(all_leads)
        
        # 6. Generate summary report
        summary = {
            'date': datetime.now().isoformat(),
            'total_leads': len(all_leads),
            'high_priority': len([l for l in all_leads if l.get('priority') == 'high']),
            'medium_priority': len([l for l in all_leads if l.get('priority') == 'medium']),
            'by_source': {},
            'by_sector': {}
        }
        
        for lead in all_leads:
            source = lead.get('source', 'Unknown')
            sector = lead.get('sector', 'Unknown')
            summary['by_source'][source] = summary['by_source'].get(source, 0) + 1
            summary['by_sector'][sector] = summary['by_sector'].get(sector, 0) + 1
        
        # Save summary
        summary_path = os.path.join(self.config['output_dir'], 'daily_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📊 DAILY SUMMARY:")
        print(f"   Total Leads: {summary['total_leads']}")
        print(f"   High Priority: {summary['high_priority']}")
        print(f"   Medium Priority: {summary['medium_priority']}")
        print(f"\n   By Source:")
        for source, count in summary['by_source'].items():
            print(f"     - {source}: {count}")
        print(f"\n{'='*60}\n")
        
        return all_leads, summary

if __name__ == '__main__':
    hunter = LeadHunter()
    leads, summary = hunter.run_daily_hunt()
