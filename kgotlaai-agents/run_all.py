#!/usr/bin/env python3
"""
Kgotla AI - Master Runner
Execute all agents with one command
"""

import sys
import os

# Add all agent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'lead-hunter'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'content-machine'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'website-fix'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'funding-scout'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'team-tracker'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'admin-dashboard'))

def run_all():
    """Run all agents and generate dashboard"""
    print("\n" + "="*70)
    print("🚀 Kgotla AI - 8-Agent System")
    print("="*70 + "\n")
    
    # Import and run each agent
    agents_ran = []
    
    # 1. Lead Hunter
    print("1️⃣  Lead Hunter - Finding prospects...")
    try:
        from lead_hunter import LeadHunter
        hunter = LeadHunter()
        leads, summary = hunter.run_daily_hunt()
        agents_ran.append("✅ Lead Hunter")
    except Exception as e:
        print(f"   Error: {e}")
        agents_ran.append("❌ Lead Hunter")
    
    # 2. Content Machine
    print("\n2️⃣  Content Machine - Creating posts...")
    try:
        from content_machine import ContentMachine
        machine = ContentMachine()
        posts = machine.generate_daily_content(num_posts=3)
        agents_ran.append("✅ Content Machine")
    except Exception as e:
        print(f"   Error: {e}")
        agents_ran.append("❌ Content Machine")
    
    # 3. Website Repair
    print("\n3️⃣  Website Repair - Auditing site...")
    try:
        from website_repair import WebsiteRepair
        repair = WebsiteRepair()
        repair.save_reports()
        agents_ran.append("✅ Website Repair")
    except Exception as e:
        print(f"   Error: {e}")
        agents_ran.append("❌ Website Repair")
    
    # 4. Funding Scout
    print("\n4️⃣  Funding Scout - Finding opportunities...")
    try:
        from funding_scout import FundingScout
        scout = FundingScout()
        scout.save_all()
        agents_ran.append("✅ Funding Scout")
    except Exception as e:
        print(f"   Error: {e}")
        agents_ran.append("❌ Funding Scout")
    
    # 5. Team Tracker
    print("\n5️⃣  Team Tracker - Checking progress...")
    try:
        from team_tracker import TeamTracker
        tracker = TeamTracker()
        tracker.save_all()
        agents_ran.append("✅ Team Tracker")
    except Exception as e:
        print(f"   Error: {e}")
        agents_ran.append("❌ Team Tracker")
    
    # 6. Admin Dashboard
    print("\n6️⃣  Admin Dashboard - Generating overview...")
    try:
        from admin_dashboard import AdminDashboard
        dashboard = AdminDashboard()
        dashboard.run_all_agents()
        dashboard.save_dashboard()
        agents_ran.append("✅ Admin Dashboard")
    except Exception as e:
        print(f"   Error: {e}")
        agents_ran.append("❌ Admin Dashboard")
    
    # Summary
    print("\n" + "="*70)
    print("📊 AGENT STATUS")
    print("="*70)
    for status in agents_ran:
        print(f"   {status}")
    
    print("\n" + "="*70)
    print("✅ All agents complete!")
    print("="*70)
    print("\n📁 Output files created in:")
    print("   • lead-hunter/leads_output/")
    print("   • content-machine/content_output/")
    print("   • website-fix/website_fixes/")
    print("   • funding-scout/funding_output/")
    print("   • team-tracker/team_output/")
    print("   • admin-dashboard/dashboard_output/")
    print("\n📄 Key files to review:")
    print("   • admin-dashboard/dashboard_output/DAILY_DASHBOARD.md")
    print("   • website-fix/website_fixes/WEBSITE_FIX_GUIDE.md")
    print("   • funding-scout/funding_output/APPLICATION_PACKAGE_SEFA.md")
    print("="*70 + "\n")

if __name__ == '__main__':
    run_all()
