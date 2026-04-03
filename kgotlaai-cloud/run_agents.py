#!/usr/bin/env python3
"""
Kgotla AI - Cloud Agent Runner
Runs all agents and generates daily outputs
"""

import os
import sys
import json
from datetime import datetime

# Add agents to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

def run_all_agents():
    """Run all agents and collect outputs"""
    print("="*70)
    print("🚀 Kgotla AI - Cloud Agent Runner")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'agents': {}
    }
    
    # Create output directories
    output_base = os.path.join(os.path.dirname(__file__), 'outputs')
    for subdir in ['leads', 'content', 'funding', 'team', 'website']:
        os.makedirs(os.path.join(output_base, subdir), exist_ok=True)
    
    # Run Lead Hunter
    print("1️⃣  Running Lead Hunter...")
    try:
        from lead_hunter import LeadHunter
        hunter = LeadHunter()
        # Modify output dir for cloud
        hunter.config['output_dir'] = os.path.join(output_base, 'leads')
        leads, summary = hunter.run_daily_hunt()
        results['agents']['lead_hunter'] = {
            'status': 'success',
            'leads_generated': len(leads),
            'high_priority': summary.get('high_priority', 0)
        }
        print(f"   ✅ Generated {len(leads)} leads")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results['agents']['lead_hunter'] = {'status': 'error', 'message': str(e)}
    
    # Run Content Machine
    print("\n2️⃣  Running Content Machine...")
    try:
        from content_machine import ContentMachine
        machine = ContentMachine()
        machine.config['output_dir'] = os.path.join(output_base, 'content')
        posts = machine.generate_daily_content(num_posts=3)
        results['agents']['content_machine'] = {
            'status': 'success',
            'posts_generated': len(posts)
        }
        print(f"   ✅ Generated {len(posts)} posts")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results['agents']['content_machine'] = {'status': 'error', 'message': str(e)}
    
    # Run Funding Scout
    print("\n3️⃣  Running Funding Scout...")
    try:
        from funding_scout import FundingScout
        scout = FundingScout()
        scout.config['output_dir'] = os.path.join(output_base, 'funding')
        scout.save_all()
        results['agents']['funding_scout'] = {
            'status': 'success',
            'target': 320100
        }
        print(f"   ✅ Generated funding applications")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results['agents']['funding_scout'] = {'status': 'error', 'message': str(e)}
    
    # Run Team Tracker
    print("\n4️⃣  Running Team Tracker...")
    try:
        from team_tracker import TeamTracker
        tracker = TeamTracker()
        tracker.config['output_dir'] = os.path.join(output_base, 'team')
        tracker.save_all()
        results['agents']['team_tracker'] = {
            'status': 'success'
        }
        print(f"   ✅ Generated team reports")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results['agents']['team_tracker'] = {'status': 'error', 'message': str(e)}
    
    # Run Website Repair
    print("\n5️⃣  Running Website Repair...")
    try:
        from website_repair import WebsiteRepair
        repair = WebsiteRepair()
        repair.config['output_dir'] = os.path.join(output_base, 'website')
        repair.save_reports()
        results['agents']['website_repair'] = {
            'status': 'success'
        }
        print(f"   ✅ Generated website audit")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results['agents']['website_repair'] = {'status': 'error', 'message': str(e)}
    
    # Save results summary
    results_path = os.path.join(output_base, 'results_summary.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate daily report
    generate_daily_report(results)
    
    print("\n" + "="*70)
    print("✅ All Agents Complete")
    print("="*70)
    print(f"\n📁 Outputs saved to: {output_base}")
    print(f"📊 Summary: {results_path}")
    
    return results

def generate_daily_report(results):
    """Generate human-readable daily report"""
    report = f"""# 🎯 Kgotla AI - Daily Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC

---

## 📊 Today's Results

"""
    
    for agent_name, agent_result in results['agents'].items():
        status_icon = '✅' if agent_result['status'] == 'success' else '❌'
        report += f"### {status_icon} {agent_name.replace('_', ' ').title()}\\n"
        if 'leads_generated' in agent_result:
            report += f"- Leads Generated: {agent_result['leads_generated']}\\n"
        if 'posts_generated' in agent_result:
            report += f"- Posts Generated: {agent_result['posts_generated']}\\n"
        if agent_result['status'] == 'error':
            report += f"- Error: {agent_result.get('message', 'Unknown error')}\\n"
        report += "\\n"
    
    report += """---

## 📁 Your Files

### 📧 Leads
- Location: `outputs/leads/`
- CSV files with prospects and draft emails

### 📝 Content  
- Location: `outputs/content/`
- LinkedIn posts ready to copy-paste

### 💰 Funding
- Location: `outputs/funding/`
- Application packages ready to submit

### 👥 Team
- Location: `outputs/team/`
- Progress reports and daily targets

### 🔧 Website
- Location: `outputs/website/`
- Audit reports and fix guides

---

## 🎯 Priority Actions

1. **🔴 CRITICAL:** Fix SSL/HTTPS - Check `outputs/website/WEBSITE_FIX_GUIDE.md`
2. **🟠 HIGH:** Submit funding - Check `outputs/funding/APPLICATION_PACKAGE_SEFA.md`
3. **🟡 HIGH:** Contact leads - Check `outputs/leads/leads_*.csv`
4. **🟢 MEDIUM:** Post content - Check `outputs/content/content_*.txt`

---

*Generated by Kgotla AI Cloud Agents*
"""
    
    with open('DAILY_REPORT.md', 'w') as f:
        f.write(report)
    
    print(f"📄 Daily report generated: DAILY_REPORT.md")

if __name__ == '__main__':
    run_all_agents()
