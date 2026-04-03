#!/usr/bin/env python3
"""
Kgotla AI - Funding Scout Agent
Monitors ED/SD funding opportunities, auto-fills applications
Tracks application status and manages fundraising pipeline
"""

import json
import os
from datetime import datetime, timedelta

class FundingScout:
    def __init__(self, config_path='../shared-config/config.json'):
        self.config = self._load_config(config_path)
        self.applications = []
        self.opportunities = []
        
        # ED/SD Funding sources in South Africa
        self.funding_sources = {
            'government': {
                'sefa': {
                    'name': 'Small Enterprise Finance Agency (sefa)',
                    'website': 'https://www.sefa.org.za',
                    'programs': [
                        {'name': 'Direct Lending', 'amount': 'Up to R5 million', 'type': 'loan'},
                        {'name': 'Wholesale Lending', 'amount': 'Up to R15 million', 'type': 'loan'},
                        {'name': 'Credit Guarantee', 'amount': 'Various', 'type': 'guarantee'}
                    ],
                    'eligibility': ['SMME', 'Black-owned', 'Operational track record'],
                    'documents': ['Business plan', 'Financial statements', 'B-BBEE certificate', 'Company registration']
                },
                'seda': {
                    'name': 'Small Enterprise Development Agency (SEDA)',
                    'website': 'https://www.seda.org.za',
                    'programs': [
                        {'name': 'Business Support', 'amount': 'Free services', 'type': 'support'},
                        {'name': 'Incubation', 'amount': 'Program-based', 'type': 'program'}
                    ],
                    'eligibility': ['SMME', 'Early stage or established'],
                    'documents': ['Business registration', 'Business plan']
                },
                'nef': {
                    'name': 'National Empowerment Fund (NEF)',
                    'website': 'https://www.nefcorp.co.za',
                    'programs': [
                        {'name': 'iMbewu Fund', 'amount': 'R250k - R10 million', 'type': 'equity/debt'},
                        {'name': 'uMnotho Fund', 'amount': 'R2 - R75 million', 'type': 'equity/debt'},
                        {'name': 'Rural & Community Development', 'amount': 'Various', 'type': 'grant/loan'}
                    ],
                    'eligibility': ['Black-owned (100%)', 'B-BBEE Level 1-3', 'Operational business'],
                    'documents': ['B-BBEE certificate', 'Business plan', 'Financials', 'Shareholder agreements']
                },
                'idc': {
                    'name': 'Industrial Development Corporation (IDC)',
                    'website': 'https://www.idc.co.za',
                    'programs': [
                        {'name': 'Gro-E Youth Scheme', 'amount': 'Up to R1 million', 'type': 'loan'},
                        {'name': 'Development Funds', 'amount': 'Various', 'type': 'equity/debt'},
                        {'name': 'Sector Specific', 'amount': 'Project-based', 'type': 'mixed'}
                    ],
                    'eligibility': ['Manufacturing/Industrial focus', 'Job creation', 'Economic impact'],
                    'documents': ['Feasibility study', 'Business plan', 'Financial projections', 'Environmental assessments']
                },
                'dtic_grants': {
                    'name': 'DTIC Incentives & Grants',
                    'website': 'https://www.thedtic.gov.za',
                    'programs': [
                        {'name': 'Black Industrialists Scheme', 'amount': 'Up to R50 million', 'type': 'grant/loan'},
                        {'name': 'Enterprise Investment Programme', 'amount': 'Various', 'type': 'grant'},
                        {'name': 'Manufacturing Competitiveness', 'amount': 'Project-based', 'type': 'grant'}
                    ],
                    'eligibility': ['Manufacturing focus', 'B-BBEE compliance', 'Export potential'],
                    'documents': ['Detailed business plan', 'Financial statements', 'Tax clearance', 'B-BBEE certificate']
                }
            },
            'private_sector': {
                'anglo_american_zimele': {
                    'name': 'Anglo American Zimele',
                    'website': 'https://www.angloamerican.com',
                    'programs': [
                        {'name': 'Enterprise Development', 'amount': 'Various', 'type': 'funding/support'},
                        {'name': 'Supplier Development', 'amount': 'Contract-based', 'type': 'procurement'}
                    ],
                    'eligibility': ['Mining sector alignment', 'B-BBEE compliant', 'Operational track record'],
                    'documents': ['Company profile', 'Financials', 'B-BBEE certificate', 'Mining sector experience']
                },
                'sasol_siyakha': {
                    'name': 'Sasol Siyakha',
                    'website': 'https://www.sasol.com',
                    'programs': [
                        {'name': 'Supplier Development', 'amount': 'Various', 'type': 'funding/support'},
                        {'name': 'Enterprise Development', 'amount': 'Grant/Loan', 'type': 'mixed'}
                    ],
                    'eligibility': ['Energy/chemical sector', 'B-BBEE compliant'],
                    'documents': ['Business plan', 'B-BBEE certificate', 'Sector alignment proof']
                },
                'absa_enterprise': {
                    'name': 'ABSA Enterprise Development',
                    'website': 'https://www.absa.co.za',
                    'programs': [
                        {'name': 'Enterprise Supplier Development', 'amount': 'Various', 'type': 'funding'},
                        {'name': 'Business Loan', 'amount': 'Up to R50 million', 'type': 'loan'}
                    ],
                    'eligibility': ['B-BBEE compliant', 'Trading history', 'Banking relationship'],
                    'documents': ['Business plan', 'Financial statements', 'B-BBEE certificate']
                },
                'nedbank_enterprise': {
                    'name': 'Nedbank Enterprise Development',
                    'website': 'https://www.nedbank.co.za',
                    'programs': [
                        {'name': 'Enterprise Development Funding', 'amount': 'Various', 'type': 'mixed'},
                        {'name': 'Business Lending', 'amount': 'Up to R50 million', 'type': 'loan'}
                    ],
                    'eligibility': ['B-BBEE compliant', 'Sustainable business model'],
                    'documents': ['Business plan', 'Financials', 'B-BBEE certificate']
                },
                'standard_bank': {
                    'name': 'Standard Bank Enterprise Development',
                    'website': 'https://www.standardbank.co.za',
                    'programs': [
                        {'name': 'Enterprise Development', 'amount': 'Various', 'type': 'funding'},
                        {'name': 'Business Lending', 'amount': 'Up to R50 million', 'type': 'loan'}
                    ],
                    'eligibility': ['B-BBEE compliant', 'Operational business'],
                    'documents': ['Business plan', 'Financial statements', 'B-BBEE certificate']
                }
            },
            'venture_capital': {
                '4di_capital': {
                    'name': '4Di Capital',
                    'website': 'https://www.4dicapital.com',
                    'focus': 'Early-stage tech startups',
                    'investment_range': 'R1 - R10 million',
                    'eligibility': ['Tech-enabled', 'Scalable', 'Strong team']
                },
                'knife_capital': {
                    'name': 'Knife Capital',
                    'website': 'https://www.knifecapital.co.za',
                    'focus': 'Growth-stage tech companies',
                    'investment_range': 'R5 - R50 million',
                    'eligibility': ['Revenue-generating', 'Growth trajectory', 'Exit potential']
                },
                'havaic': {
                    'name': 'HAVAÍC',
                    'website': 'https://www.havaic.com',
                    'focus': 'Tech and innovation',
                    'investment_range': 'R2 - R20 million',
                    'eligibility': ['Innovative tech', 'Strong founding team', 'Market traction']
                },
                'jozi_angels': {
                    'name': 'Jozi Angels',
                    'website': 'https://www.joziangels.com',
                    'focus': 'Early-stage startups',
                    'investment_range': 'R500k - R5 million',
                    'eligibility': ['Early stage', 'Strong team', 'Market validation']
                }
            }
        }
        
        # Application templates
        self.application_templates = {
            'executive_summary': """
Kgotla AI (Pty) Ltd - Enterprise Development Application

EXECUTIVE SUMMARY
=================

Company: Kgotla AI
Founder: Mahlo Kgotleng
Registration: In progress (Pty Ltd)
Website: https://kgotlaai.co.za
Email: mahlo@kgotlaai.co.za
LinkedIn: https://www.linkedin.com/in/mahlo-kgotleng-473830194

BUSINESS OVERVIEW
-----------------
Kgotla AI is an applied artificial intelligence consultancy specializing in 
enterprise-grade AI solutions for heavy industrial sectors—mining, manufacturing, 
power generation, and logistics. We deliver predictive maintenance, safety 
monitoring, process optimization, and intelligent automation.

Our mission is to bring world-class AI capabilities to African industrial 
operations, improving safety, efficiency, and profitability.

TARGET MARKET
-------------
• Mining: Anglo American, Sibanye-Stillwater, Exxaro, South32
• Manufacturing: ArcelorMittal, Tiger Brands, Sappi
• Power: Eskom, municipal utilities
• Logistics: Transnet, Imperial Logistics
• Geography: South Africa, SADC region, expanding Africa-wide

COMPETITIVE ADVANTAGE
---------------------
1. IBM Partner Plus Registered - watsonx ecosystem expertise
2. AWS Cloud training in progress
3. Industrial domain expertise combined with AI technical capability
4. Hybrid-cloud, tool-independent architecture approach
5. B-BBEE Level 1 potential (100% black-owned)

TRACTION & PIPELINE
-------------------
• Active contract negotiation with Grupo Flores da Vila (Angola)
• IBM distributor partnership through Pinnacle Micro
• Kgutlo Tharo Skills Development partnership
• 4-person technical team in IBM certification program

FUNDING REQUIREMENT
-------------------
Amount Sought: R320,100
Use of Funds:
  - Capex: Equipment, infrastructure (R150,000)
  - Opex: Operations, team, marketing (R170,100)

Equity Offered: 50%
B-BBEE Status: 100% Black-owned, Level 1 potential

CONTACT
-------
Mahlo Kgotleng
Founder & Director
mahlo@kgotlaai.co.za
https://kgotlaai.co.za
""",
            'business_plan_sections': {
                'problem_statement': """
PROBLEM STATEMENT
=================

South African industrial sectors face critical challenges:

1. UNPLANNED DOWNTIME costs mining operations R50+ million annually per site
2. SAFETY INCIDENTS result in fatalities, regulatory penalties, and production halts
3. INEFFICIENT PROCESSES waste 20-30% of operational capacity
4. SKILLED LABOR SHORTAGE limits operational optimization
5. LEGACY SYSTEMS prevent digital transformation

Current solutions are either:
- Too expensive (international consultancies charging premium rates)
- Too generic (off-the-shelf software not designed for industrial use)
- Too slow (traditional consulting engagements taking 12-18 months)

Kgotla AI addresses this gap with tailored, affordable, rapid-deployment AI solutions.
""",
                'solution': """
SOLUTION
========

Kgotla AI delivers end-to-end AI solutions for industrial operations:

1. PREDICTIVE MAINTENANCE
   - Machine learning models predict equipment failures 48-168 hours in advance
   - Reduces unplanned downtime by 30-50%
   - Integrates with existing SCADA/IoT systems

2. SAFETY AI & COMPUTER VISION
   - Real-time monitoring of PPE compliance, restricted zones, unsafe behavior
   - Automated alerts and incident reporting
   - Reduces safety incidents by 40%+

3. PROCESS OPTIMIZATION
   - AI-driven recommendations for production parameters
   - Energy optimization and waste reduction
   - Quality prediction and control

4. INTELLIGENT AUTOMATION
   - RPA for repetitive administrative tasks
   - Document processing and data extraction
   - Compliance reporting automation

DELIVERY MODEL
--------------
• Hybrid-cloud architecture (IBM watsonx + AWS)
• Tool-independent approach (not locked to single vendor)
• Pilot-first methodology (prove value in 3 months, then scale)
• Knowledge transfer and training included
""",
                'market_analysis': """
MARKET ANALYSIS
===============

TOTAL ADDRESSABLE MARKET (TAM)
------------------------------
South African industrial AI market: R2.5 billion annually
SADC region: R8 billion annually

SERVICEABLE ADDRESSABLE MARKET (SAM)
------------------------------------
Mining, manufacturing, power, logistics in SA: R800 million

SERVICEABLE OBTAINABLE MARKET (SOM)
-----------------------------------
Realistic 5-year target: R50 million (6% of SAM)

MARKET TRENDS
-------------
• Mining companies mandated to increase local procurement
• B-BBEE requirements driving supplier diversity
• Industry 4.0 adoption accelerating post-COVID
• ESG compliance requiring better monitoring and reporting
• Skills shortage creating demand for AI-augmented operations

COMPETITIVE LANDSCAPE
---------------------
Direct competitors: Limited in SA industrial AI space
- International firms (Accenture, Deloitte) - expensive, slow
- Local IT companies - lack industrial domain expertise
- Startups - lack enterprise credibility and support

Kgotla AI advantage: Industrial expertise + AI capability + Local presence
""",
                'financial_projections': """
FINANCIAL PROJECTIONS
=====================

YEAR 1 (2025)
-------------
Revenue Target: R1,500,000
- Q1: R200,000 (pilot projects)
- Q2: R400,000 (contract wins)
- Q3: R450,000 (scaling)
- Q4: R450,000 (recurring + new)

Expenses: R1,800,000
Net: (R300,000) - Investment year

YEAR 2 (2026)
-------------
Revenue Target: R4,000,000
Expenses: R3,200,000
Net Profit: R800,000 (20% margin)

YEAR 3 (2027)
-------------
Revenue Target: R8,000,000
Expenses: R5,600,000
Net Profit: R2,400,000 (30% margin)

YEAR 4 (2028)
-------------
Revenue Target: R15,000,000
Expenses: R9,750,000
Net Profit: R5,250,000 (35% margin)

YEAR 5 (2029)
-------------
Revenue Target: R25,000,000
Expenses: R15,000,000
Net Profit: R10,000,000 (40% margin)

KEY ASSUMPTIONS
---------------
• 3 major contract wins per year from Year 2
• Average contract value: R1.5M (growing to R3M)
• Team growth: 4 → 8 → 15 → 25 → 40 people
• Recurring revenue: 30% of total by Year 3
""",
                'use_of_funds': """
USE OF FUNDS: R320,100
======================

CAPITAL EXPENDITURE (R150,000)
------------------------------
• Development equipment (laptops, servers): R80,000
• Cloud infrastructure setup: R30,000
• Software licenses (development tools): R20,000
• Office equipment: R20,000

OPERATIONAL EXPENDITURE (R170,100)
----------------------------------
• Salaries (4 team members, 6 months): R120,000
• Marketing and sales: R20,000
• Legal and compliance: R15,000
• Travel and client meetings: R10,000
• Insurance and admin: R5,100

MILESTONES (6 months)
---------------------
Month 1-2: Team onboarding, IBM/AWS certification completion
Month 3-4: First paying client, demo environment live
Month 5-6: Second client, R500K+ revenue, funding round complete

EXPECTED RETURN
---------------
Year 1 ROI: Break-even
Year 2 ROI: 150%
Year 3 ROI: 400%
5-year valuation target: R50-100 million
"""
            }
        }
    
    def _load_config(self, path):
        default_config = {
            'company_name': 'Kgotla AI',
            'founder_name': 'Mahlo Kgotleng',
            'email': 'mahlo@kgotlaai.co.za',
            'funding_target': 320100,
            'equity_offered': 50,
            'output_dir': './funding_output'
        }
        
        if os.path.exists(path):
            with open(path, 'r') as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def generate_funding_pipeline(self):
        """Generate prioritized funding pipeline"""
        pipeline = {
            'immediate': [],  # Apply within 2 weeks
            'short_term': [],  # Apply within 1 month
            'medium_term': []  # Apply within 3 months
        }
        
        # Immediate opportunities (fastest to decision)
        pipeline['immediate'] = [
            {
                'source': 'sefa',
                'program': 'Direct Lending',
                'amount': 'R5 million max',
                'timeline': '4-8 weeks',
                'priority': 'HIGH',
                'action': 'Prepare business plan and apply online',
                'url': 'https://www.sefa.org.za/apply-for-funding'
            },
            {
                'source': 'seda',
                'program': 'Business Support + Incubation',
                'amount': 'Free services',
                'timeline': '2-4 weeks',
                'priority': 'HIGH',
                'action': 'Register at local SEDA branch',
                'url': 'https://www.seda.org.za/contact-us'
            },
            {
                'source': 'nef',
                'program': 'iMbewu Fund',
                'amount': 'R250k - R10 million',
                'timeline': '6-12 weeks',
                'priority': 'HIGH',
                'action': 'Prepare comprehensive application with B-BBEE cert',
                'url': 'https://www.nefcorp.co.za/funding-solutions'
            }
        ]
        
        # Short-term opportunities
        pipeline['short_term'] = [
            {
                'source': 'idc',
                'program': 'Gro-E Youth Scheme',
                'amount': 'Up to R1 million',
                'timeline': '8-12 weeks',
                'priority': 'MEDIUM',
                'action': 'Complete feasibility study',
                'url': 'https://www.idc.co.za/funding'
            },
            {
                'source': 'dtic_grants',
                'program': 'Black Industrialists Scheme',
                'amount': 'Up to R50 million',
                'timeline': '3-6 months',
                'priority': 'MEDIUM',
                'action': 'Engage DTIC business officer',
                'url': 'https://www.thedtic.gov.za/financial-and-non-financial-support/'
            },
            {
                'source': 'anglo_american_zimele',
                'program': 'Enterprise Development',
                'amount': 'Various',
                'timeline': '2-3 months',
                'priority': 'MEDIUM',
                'action': 'Submit supplier application',
                'url': 'https://www.angloamerican.com/suppliers'
            }
        ]
        
        # Medium-term opportunities
        pipeline['medium_term'] = [
            {
                'source': '4di_capital',
                'program': 'Early-stage Investment',
                'amount': 'R1-10 million',
                'timeline': '3-6 months',
                'priority': 'MEDIUM',
                'action': 'Prepare pitch deck, reach out to partners',
                'url': 'https://www.4dicapital.com/apply'
            },
            {
                'source': 'jozi_angels',
                'program': 'Angel Investment',
                'amount': 'R500k-5 million',
                'timeline': '2-4 months',
                'priority': 'MEDIUM',
                'action': 'Apply online, prepare for pitch',
                'url': 'https://www.joziangels.com/apply'
            },
            {
                'source': 'private_banks',
                'program': 'Enterprise Development',
                'amount': 'Various',
                'timeline': '1-3 months',
                'priority': 'LOW',
                'action': 'Approach relationship managers',
                'url': 'Contact ABSA, Nedbank, Standard Bank'
            }
        ]
        
        return pipeline
    
    def generate_application_package(self, target_source='sefa'):
        """Generate complete application package for a funding source"""
        package = {
            'target': target_source,
            'generated_at': datetime.now().isoformat(),
            'documents': {}
        }
        
        # Executive Summary
        package['documents']['executive_summary'] = self.application_templates['executive_summary']
        
        # Business Plan Sections
        for section, content in self.application_templates['business_plan_sections'].items():
            package['documents'][f'business_plan_{section}'] = content
        
        # Checklist for this specific source
        if target_source in self.funding_sources.get('government', {}):
            source_info = self.funding_sources['government'][target_source]
        elif target_source in self.funding_sources.get('private_sector', {}):
            source_info = self.funding_sources['private_sector'][target_source]
        else:
            source_info = {'documents': ['Business plan', 'Financial statements', 'B-BBEE certificate']}
        
        package['required_documents'] = source_info.get('documents', [])
        package['eligibility'] = source_info.get('eligibility', [])
        package['programs'] = source_info.get('programs', [])
        
        # Application checklist
        package['checklist'] = [
            '☐ Company registration documents (CIPC)',
            '☐ B-BBEE certificate or sworn affidavit',
            '☐ Tax clearance certificate (SARS)',
            '☐ Business plan (use generated template)',
            '☐ Financial statements (if available) or projections',
            '☐ Founder ID and proof of address',
            '☐ Bank statements (3-6 months)',
            '☐ Quotations for use of funds',
            '☐ Contracts/LOIs from potential clients',
            '☐ Partner/vendor agreements (IBM, etc.)',
            '☐ Team CVs and certifications',
            '☐ Website/screenshots of work'
        ]
        
        return package
    
    def track_application(self, source, program, amount_requested, date_submitted, status='submitted'):
        """Track a funding application"""
        application = {
            'id': f"APP-{datetime.now().strftime('%Y%m%d')}-{len(self.applications)+1:03d}",
            'source': source,
            'program': program,
            'amount_requested': amount_requested,
            'date_submitted': date_submitted,
            'status': status,
            'last_updated': datetime.now().isoformat(),
            'follow_up_dates': self._calculate_follow_ups(date_submitted),
            'notes': ''
        }
        
        self.applications.append(application)
        return application
    
    def _calculate_follow_ups(self, date_submitted):
        """Calculate follow-up dates"""
        submitted = datetime.strptime(date_submitted, '%Y-%m-%d')
        return {
            'first_follow_up': (submitted + timedelta(days=14)).strftime('%Y-%m-%d'),
            'second_follow_up': (submitted + timedelta(days=30)).strftime('%Y-%m-%d'),
            'escalation': (submitted + timedelta(days=45)).strftime('%Y-%m-%d')
        }
    
    def get_follow_up_reminders(self):
        """Get applications needing follow-up"""
        today = datetime.now()
        reminders = []
        
        for app in self.applications:
            if app['status'] in ['submitted', 'under_review']:
                follow_ups = app.get('follow_up_dates', {})
                
                for follow_up_type, date_str in follow_ups.items():
                    follow_up_date = datetime.strptime(date_str, '%Y-%m-%d')
                    days_until = (follow_up_date - today).days
                    
                    if 0 <= days_until <= 3:
                        reminders.append({
                            'application_id': app['id'],
                            'source': app['source'],
                            'program': app['program'],
                            'follow_up_type': follow_up_type,
                            'due_date': date_str,
                            'days_until': days_until
                        })
        
        return reminders
    
    def save_all(self):
        """Save all funding data"""
        os.makedirs(self.config['output_dir'], exist_ok=True)
        
        # Save funding pipeline
        pipeline = self.generate_funding_pipeline()
        pipeline_path = os.path.join(self.config['output_dir'], 'funding_pipeline.json')
        with open(pipeline_path, 'w') as f:
            json.dump(pipeline, f, indent=2)
        
        # Save application package for sefa (as example)
        package = self.generate_application_package('sefa')
        package_path = os.path.join(self.config['output_dir'], 'application_package_sefa.json')
        with open(package_path, 'w') as f:
            json.dump(package, f, indent=2)
        
        # Save application package as markdown
        md_content = self._generate_application_markdown(package)
        md_path = os.path.join(self.config['output_dir'], 'APPLICATION_PACKAGE_SEFA.md')
        with open(md_path, 'w') as f:
            f.write(md_content)
        
        # Save funding sources reference
        sources_path = os.path.join(self.config['output_dir'], 'funding_sources_reference.json')
        with open(sources_path, 'w') as f:
            json.dump(self.funding_sources, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"💰 Kgotla AI Funding Scout - Reports Generated")
        print(f"{'='*60}\n")
        
        print(f"📁 Files created:")
        print(f"   • {pipeline_path}")
        print(f"   • {package_path}")
        print(f"   • {md_path}")
        print(f"   • {sources_path}\n")
        
        print(f"🎯 FUNDING PIPELINE:")
        print(f"   Immediate (Apply now): {len(pipeline['immediate'])} opportunities")
        print(f"   Short-term (1 month): {len(pipeline['short_term'])} opportunities")
        print(f"   Medium-term (3 months): {len(pipeline['medium_term'])} opportunities\n")
        
        print(f"✅ NEXT ACTIONS:")
        print(f"   1. Review APPLICATION_PACKAGE_SEFA.md")
        print(f"   2. Gather required documents")
        print(f"   3. Apply to sefa Direct Lending (fastest)")
        print(f"   4. Register with local SEDA branch")
        print(f"   5. Prepare NEF iMbewu application\n")
        
        print(f"📊 TARGET: R{self.config['funding_target']:,.0f}")
        print(f"   Equity offered: {self.config['equity_offered']}%")
        print(f"\n{'='*60}\n")
        
        return pipeline_path, package_path, md_path
    
    def _generate_application_markdown(self, package):
        """Generate markdown application package"""
        md = f"""# Kgotla AI - Funding Application Package
**Target:** {package['target'].upper()}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📋 DOCUMENT CHECKLIST

"""
        for item in package['checklist']:
            md += f"{item}\n"
        
        md += f"""
---

## 🎯 ELIGIBILITY REQUIREMENTS

"""
        for req in package['eligibility']:
            md += f"- {req}\n"
        
        md += f"""
---

## 💼 AVAILABLE PROGRAMS

"""
        for program in package['programs']:
            md += f"""### {program['name']}
- **Amount:** {program['amount']}
- **Type:** {program['type']}

"""
        
        md += f"""---

## 📄 EXECUTIVE SUMMARY

{package['documents']['executive_summary']}

---

## 📑 BUSINESS PLAN

"""
        for section, content in package['documents'].items():
            if section.startswith('business_plan_'):
                section_name = section.replace('business_plan_', '').replace('_', ' ').title()
                md += f"""### {section_name}

{content}

---

"""
        
        md += """## ✅ SUBMISSION CHECKLIST

Before submitting:
- [ ] All required documents gathered
- [ ] Business plan reviewed and proofread
- [ ] Financial projections realistic
- [ ] Supporting documents attached
- [ ] Application form completed fully
- [ ] Copies made for your records

---

**Contact:** mahlo@kgotlaai.co.za
"""
        
        return md

if __name__ == '__main__':
    scout = FundingScout()
    scout.save_all()
