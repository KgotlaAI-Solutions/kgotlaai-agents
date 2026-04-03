#!/usr/bin/env python3
"""
Kgotla AI - Admin Dashboard
Central command center for all agents
One-view summary of leads, content, website, funding, team
"""

import json
import os
import sys
from datetime import datetime, timedelta

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lead-hunter'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'content-machine'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'website-fix'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'funding-scout'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'team-tracker'))

class AdminDashboard:
    def __init__(self, config_path='../shared-config/config.json'):
        self.config = self._load_config(config_path)
        self.output_dir = './dashboard_output'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Dashboard data containers
        self.leads_summary = {}
        self.content_summary = {}
        self.website_summary = {}
        self.funding_summary = {}
        self.team_summary = {}
        
        # Key metrics
        self.kpis = {
            'leads_generated_today': 0,
            'leads_this_week': 0,
            'content_posts_scheduled': 0,
            'website_issues_critical': 0,
            'funding_applications_pending': 0,
            'team_avg_progress': 0,
            'pipeline_value': 0
        }
    
    def _load_config(self, path):
        default_config = {
            'company_name': 'Kgotla AI',
            'founder_name': 'Mahlo Kgotleng',
            'email': 'mahlo@kgotlaai.co.za',
            'website': 'kgotlaai.co.za',
            'funding_target': 320100
        }
        
        if os.path.exists(path):
            with open(path, 'r') as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def run_all_agents(self):
        """Execute all agents and collect data"""
        print("\n" + "="*70)
        print("🚀 Kgotla AI - Running All Agents")
        print("="*70 + "\n")
        
        # Run Lead Hunter
        print("▶️  Running Lead Hunter...")
        try:
            from lead_hunter import LeadHunter
            hunter = LeadHunter()
            leads, summary = hunter.run_daily_hunt()
            self.leads_summary = {
                'total_leads': summary['total_leads'],
                'high_priority': summary['high_priority'],
                'by_source': summary['by_source'],
                'by_sector': summary['by_sector']
            }
            self.kpis['leads_generated_today'] = summary['total_leads']
            print(f"   ✅ Generated {summary['total_leads']} leads\n")
        except Exception as e:
            print(f"   ⚠️  Lead Hunter error: {e}\n")
            self.leads_summary = {'error': str(e)}
        
        # Run Content Machine
        print("▶️  Running Content Machine...")
        try:
            from content_machine import ContentMachine
            machine = ContentMachine()
            posts = machine.generate_daily_content(num_posts=3)
            self.content_summary = {
                'posts_generated': len(posts),
                'themes': list(set([p['theme'] for p in posts])),
                'industries': list(set([p['industry'] for p in posts]))
            }
            self.kpis['content_posts_scheduled'] = len(posts)
            print(f"   ✅ Generated {len(posts)} posts\n")
        except Exception as e:
            print(f"   ⚠️  Content Machine error: {e}\n")
            self.content_summary = {'error': str(e)}
        
        # Run Website Repair
        print("▶️  Running Website Repair...")
        try:
            from website_repair import WebsiteRepair
            repair = WebsiteRepair()
            audit = repair.generate_full_audit_report()
            self.website_summary = {
                'critical_issues': len(audit['critical_issues']),
                'high_priority': len(audit['high_priority']),
                'medium_priority': len(audit['medium_priority'])
            }
            self.kpis['website_issues_critical'] = len(audit['critical_issues'])
            print(f"   ✅ Found {len(audit['critical_issues'])} critical issues\n")
        except Exception as e:
            print(f"   ⚠️  Website Repair error: {e}\n")
            self.website_summary = {'error': str(e)}
        
        # Run Funding Scout
        print("▶️  Running Funding Scout...")
        try:
            from funding_scout import FundingScout
            scout = FundingScout()
            pipeline = scout.generate_funding_pipeline()
            total_opportunities = sum(len(v) for v in pipeline.values())
            self.funding_summary = {
                'immediate': len(pipeline['immediate']),
                'short_term': len(pipeline['short_term']),
                'medium_term': len(pipeline['medium_term']),
                'total': total_opportunities,
                'target_amount': self.config['funding_target']
            }
            print(f"   ✅ Found {total_opportunities} funding opportunities\n")
        except Exception as e:
            print(f"   ⚠️  Funding Scout error: {e}\n")
            self.funding_summary = {'error': str(e)}
        
        # Run Team Tracker
        print("▶️  Running Team Tracker...")
        try:
            from team_tracker import TeamTracker
            tracker = TeamTracker()
            progress_reports = tracker.generate_progress_report()
            
            total_progress = 0
            member_count = len(progress_reports)
            for report in progress_reports.values():
                total_progress += report['summary']['progress_percent']
            
            avg_progress = total_progress / member_count if member_count > 0 else 0
            
            self.team_summary = {
                'members': member_count,
                'avg_progress': round(avg_progress, 1),
                'individual': {k: v['summary']['progress_percent'] for k, v in progress_reports.items()}
            }
            self.kpis['team_avg_progress'] = round(avg_progress, 1)
            print(f"   ✅ Team avg progress: {round(avg_progress, 1)}%\n")
        except Exception as e:
            print(f"   ⚠️  Team Tracker error: {e}\n")
            self.team_summary = {'error': str(e)}
        
        print("="*70)
        print("✅ All Agents Complete")
        print("="*70 + "\n")
    
    def generate_dashboard(self):
        """Generate comprehensive dashboard"""
        dashboard = {
            'generated_at': datetime.now().isoformat(),
            'company': self.config['company_name'],
            'kpis': self.kpis,
            'sections': {
                'leads': self.leads_summary,
                'content': self.content_summary,
                'website': self.website_summary,
                'funding': self.funding_summary,
                'team': self.team_summary
            },
            'actions_required': self._generate_action_items(),
            'daily_priorities': self._generate_daily_priorities()
        }
        
        return dashboard
    
    def _generate_action_items(self):
        """Generate list of required actions"""
        actions = []
        
        # Website critical issues
        if self.website_summary.get('critical_issues', 0) > 0:
            actions.append({
                'priority': 'CRITICAL',
                'category': 'Website',
                'action': 'Fix SSL/HTTPS issue immediately',
                'impact': 'Clients see security warning - losing trust',
                'time_estimate': '2 hours'
            })
        
        # Funding
        if self.funding_summary.get('immediate', 0) > 0:
            actions.append({
                'priority': 'HIGH',
                'category': 'Funding',
                'action': f"Apply to {self.funding_summary['immediate']} immediate funding opportunities",
                'impact': 'Secure runway for next 6 months',
                'time_estimate': '4 hours'
            })
        
        # Leads
        if self.kpis['leads_generated_today'] > 0:
            actions.append({
                'priority': 'HIGH',
                'category': 'Sales',
                'action': f"Contact {self.leads_summary.get('high_priority', 0)} high-priority leads",
                'impact': 'Convert leads to meetings',
                'time_estimate': '2 hours'
            })
        
        # Content
        if self.kpis['content_posts_scheduled'] > 0:
            actions.append({
                'priority': 'MEDIUM',
                'category': 'Marketing',
                'action': 'Post today\'s content to LinkedIn',
                'impact': 'Build brand visibility',
                'time_estimate': '30 minutes'
            })
        
        # Team
        if self.kpis['team_avg_progress'] < 30:
            actions.append({
                'priority': 'MEDIUM',
                'category': 'Team',
                'action': 'Check in with team on IBM progress',
                'impact': 'Ensure certification timeline met',
                'time_estimate': '30 minutes'
            })
        
        return sorted(actions, key=lambda x: {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}.get(x['priority'], 4))
    
    def _generate_daily_priorities(self):
        """Generate daily priority list"""
        return [
            {
                'time': '08:00',
                'task': 'Review dashboard and overnight leads',
                'duration': '15 min'
            },
            {
                'time': '08:15',
                'task': 'Post LinkedIn content (morning)',
                'duration': '15 min'
            },
            {
                'time': '09:00',
                'task': 'Team standup - IBM progress check',
                'duration': '15 min'
            },
            {
                'time': '09:30',
                'task': 'Contact high-priority leads',
                'duration': '1 hour'
            },
            {
                'time': '11:00',
                'task': 'Work on funding applications',
                'duration': '2 hours'
            },
            {
                'time': '14:00',
                'task': 'Client calls/meetings',
                'duration': '2 hours'
            },
            {
                'time': '16:00',
                'task': 'Post LinkedIn content (afternoon)',
                'duration': '15 min'
            },
            {
                'time': '16:30',
                'task': 'Review and plan tomorrow',
                'duration': '30 min'
            },
            {
                'time': '17:00',
                'task': 'Post LinkedIn content (evening)',
                'duration': '15 min'
            }
        ]
    
    def generate_markdown_dashboard(self):
        """Generate human-readable markdown dashboard"""
        dashboard = self.generate_dashboard()
        
        md = f"""# 🎯 Kgotla AI - Daily Command Dashboard
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📊 KEY METRICS

| Metric | Value | Status |
|--------|-------|--------|
| Leads Today | {self.kpis['leads_generated_today']} | {'✅' if self.kpis['leads_generated_today'] >= 20 else '⚠️'} |
| Content Scheduled | {self.kpis['content_posts_scheduled']} posts | ✅ |
| Website Issues | {self.kpis['website_issues_critical']} critical | {'🚨' if self.kpis['website_issues_critical'] > 0 else '✅'} |
| Team Progress | {self.kpis['team_avg_progress']}% avg | {'✅' if self.kpis['team_avg_progress'] >= 25 else '⚠️'} |

---

## 🚨 ACTIONS REQUIRED

"""
        
        for action in dashboard['actions_required']:
            md += f"""### {action['priority']}: {action['action']}
- **Category:** {action['category']}
- **Impact:** {action['impact']}
- **Time:** {action['time_estimate']}

"""
        
        md += f"""---

## 📈 LEADS SUMMARY

- **Total Generated:** {self.leads_summary.get('total_leads', 0)}
- **High Priority:** {self.leads_summary.get('high_priority', 0)}
- **Medium Priority:** {self.leads_summary.get('high_priority', 0)}

**By Source:**
"""
        
        for source, count in self.leads_summary.get('by_source', {}).items():
            md += f"- {source}: {count}\n"
        
        md += f"""
**By Sector:**
"""
        
        for sector, count in self.leads_summary.get('by_sector', {}).items():
            md += f"- {sector}: {count}\n"
        
        md += f"""
---

## 📝 CONTENT SUMMARY

- **Posts Generated:** {self.content_summary.get('posts_generated', 0)}
- **Themes:** {', '.join(self.content_summary.get('themes', []))}
- **Industries:** {', '.join(self.content_summary.get('industries', []))}

---

## 🔧 WEBSITE STATUS

- **Critical Issues:** {self.website_summary.get('critical_issues', 0)}
- **High Priority:** {self.website_summary.get('high_priority', 0)}
- **Medium Priority:** {self.website_summary.get('medium_priority', 0)}

**Next Actions:**
- [ ] Fix SSL/HTTPS configuration
- [ ] Repair broken demo components
- [ ] Implement SEO optimizations

---

## 💰 FUNDING PIPELINE

- **Immediate (Apply Now):** {self.funding_summary.get('immediate', 0)} opportunities
- **Short-term (1 month):** {self.funding_summary.get('short_term', 0)} opportunities
- **Medium-term (3 months):** {self.funding_summary.get('medium_term', 0)} opportunities
- **Target Amount:** R{self.funding_summary.get('target_amount', 0):,}

**Top Priorities:**
1. sefa Direct Lending (fastest approval)
2. SEDA Business Support (free services)
3. NEF iMbewu Fund (equity/debt)

---

## 👥 TEAM PROGRESS

- **Team Size:** {self.team_summary.get('members', 0)}
- **Average Progress:** {self.team_summary.get('avg_progress', 0)}%

**Individual Progress:**
"""
        
        for member, progress in self.team_summary.get('individual', {}).items():
            md += f"- {member.title()}: {progress}%\n"
        
        md += f"""
---

## 📅 DAILY SCHEDULE

"""
        
        for item in dashboard['daily_priorities']:
            md += f"**{item['time']}** - {item['task']} ({item['duration']})\n\n"
        
        md += f"""---

## ✅ END OF DAY CHECKLIST

- [ ] All leads contacted
- [ ] Content posted (3x)
- [ ] Funding applications submitted
- [ ] Team check-ins completed
- [ ] Tomorrow planned
- [ ] Dashboard reviewed

---

**Quick Links:**
- Website: https://kgotlaai.co.za
- LinkedIn: {self.config.get('linkedin_url', 'N/A')}
- Email: {self.config['email']}

**Next Dashboard Update:** Tomorrow 08:00
"""
        
        return md
    
    def save_dashboard(self):
        """Save dashboard in multiple formats"""
        # Generate dashboard data
        dashboard = self.generate_dashboard()
        
        # Save JSON
        json_path = os.path.join(self.output_dir, f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(json_path, 'w') as f:
            json.dump(dashboard, f, indent=2)
        
        # Save Markdown
        md = self.generate_markdown_dashboard()
        md_path = os.path.join(self.output_dir, 'DAILY_DASHBOARD.md')
        with open(md_path, 'w') as f:
            f.write(md)
        
        # Save latest summary
        summary_path = os.path.join(self.output_dir, 'latest_summary.json')
        with open(summary_path, 'w') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'kpis': self.kpis,
                'actions_count': len(dashboard['actions_required']),
                'critical_actions': len([a for a in dashboard['actions_required'] if a['priority'] == 'CRITICAL'])
            }, f, indent=2)
        
        print(f"\n{'='*70}")
        print(f"📊 Kgotla AI Admin Dashboard - Generated")
        print(f"{'='*70}\n")
        
        print(f"📁 Dashboard Files:")
        print(f"   • {json_path} (Full data)")
        print(f"   • {md_path} (Human-readable)")
        print(f"   • {summary_path} (Quick summary)\n")
        
        print(f"🎯 TODAY'S PRIORITIES:")
        for i, action in enumerate(dashboard['actions_required'][:5], 1):
            print(f"   {i}. [{action['priority']}] {action['action']}")
        
        print(f"\n{'='*70}\n")
        
        return json_path, md_path
    
    def print_quick_view(self):
        """Print quick terminal view"""
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                    Kgotla AI - DAILY DASHBOARD                   ║
║                      {datetime.now().strftime('%Y-%m-%d %H:%M')}                      ║
╠══════════════════════════════════════════════════════════════════╣
║  📊 KEY METRICS                                                  ║
║  ─────────────────────────────────────────────────────────────   ║
║  Leads Today:        {self.kpis['leads_generated_today']:>4}                                     ║
║  Content Posts:      {self.kpis['content_posts_scheduled']:>4}                                     ║
║  Website Issues:     {self.kpis['website_issues_critical']:>4} critical                          ║
║  Team Progress:      {self.kpis['team_avg_progress']:>4}% avg                              ║
╠══════════════════════════════════════════════════════════════════╣
║  🚨 TOP ACTIONS                                                  ║
║  ─────────────────────────────────────────────────────────────   ║
""")
        
        for i, action in enumerate(self._generate_action_items()[:3], 1):
            priority_icon = {'CRITICAL': '🚨', 'HIGH': '⚠️', 'MEDIUM': 'ℹ️'}.get(action['priority'], '•')
            print(f"║  {priority_icon} {action['action'][:50]:<50}   ║")
        
        print(f"""║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  💰 FUNDING: {self.funding_summary.get('immediate', 0)} immediate | {self.funding_summary.get('short_term', 0)} short-term          ║
║  👥 TEAM: {self.team_summary.get('members', 0)} members | {self.team_summary.get('avg_progress', 0)}% avg progress              ║
╚══════════════════════════════════════════════════════════════════╝
""")

def main():
    """Main execution"""
    dashboard = AdminDashboard()
    
    # Run all agents
    dashboard.run_all_agents()
    
    # Generate and save dashboard
    dashboard.save_dashboard()
    
    # Print quick view
    dashboard.print_quick_view()
    
    print("\n✅ Dashboard complete! Check DAILY_DASHBOARD.md for full details.\n")

if __name__ == '__main__':
    main()
