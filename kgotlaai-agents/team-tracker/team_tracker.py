#!/usr/bin/env python3
"""
Kgotla AI - Team Tracker Agent
Monitors IBM portal progress, sends daily targets
Generates reports for team members
"""

import json
import os
from datetime import datetime, timedelta

class TeamTracker:
    def __init__(self, config_path='../shared-config/config.json'):
        self.config = self._load_config(config_path)
        
        # Team members
        self.team_members = {
            'thando': {
                'name': 'Thando',
                'email': '',  # To be filled
                'role': 'AI Developer',
                'ibm_portal': 'https://skillsbuild.org/',
                'current_path': 'IBM AI Practitioner',
                'courses_completed': [],
                'courses_in_progress': [],
                'daily_target_hours': 2,
                'start_date': '2025-01-01'
            },
            'samkelo': {
                'name': 'Samkelo',
                'email': '',  # To be filled
                'role': 'AI Developer',
                'ibm_portal': 'https://skillsbuild.org/',
                'current_path': 'IBM AI Practitioner',
                'courses_completed': [],
                'courses_in_progress': [],
                'daily_target_hours': 2,
                'start_date': '2025-01-01'
            },
            'lorraine': {
                'name': 'Lorraine',
                'email': '',  # To be filled
                'role': 'AI Developer',
                'ibm_portal': 'https://skillsbuild.org/',
                'current_path': 'IBM AI Practitioner',
                'courses_completed': [],
                'courses_in_progress': [],
                'daily_target_hours': 2,
                'start_date': '2025-01-01'
            }
        }
        
        # IBM AI Practitioner path courses
        self.ibm_ai_practitioner_path = {
            'name': 'IBM AI Practitioner',
            'total_courses': 9,
            'courses': [
                {
                    'id': 'ai_fundamentals',
                    'name': 'IBM AI Fundamentals',
                    'duration_hours': 8,
                    'badge': 'IBM AI Fundamentals',
                    'prerequisites': [],
                    'order': 1
                },
                {
                    'id': 'generative_ai',
                    'name': 'Generative AI Fundamentals',
                    'duration_hours': 4,
                    'badge': 'Generative AI Fundamentals',
                    'prerequisites': ['ai_fundamentals'],
                    'order': 2
                },
                {
                    'id': 'watsonx_ai',
                    'name': 'IBM watsonx AI Fundamentals',
                    'duration_hours': 6,
                    'badge': 'IBM watsonx AI Fundamentals',
                    'prerequisites': ['ai_fundamentals'],
                    'order': 3
                },
                {
                    'id': 'prompt_engineering',
                    'name': 'Prompt Engineering Fundamentals',
                    'duration_hours': 4,
                    'badge': 'Prompt Engineering Fundamentals',
                    'prerequisites': ['generative_ai'],
                    'order': 4
                },
                {
                    'id': 'ai_ethics',
                    'name': 'AI Ethics Fundamentals',
                    'duration_hours': 3,
                    'badge': 'AI Ethics Fundamentals',
                    'prerequisites': ['ai_fundamentals'],
                    'order': 5
                },
                {
                    'id': 'machine_learning',
                    'name': 'Machine Learning Fundamentals',
                    'duration_hours': 8,
                    'badge': 'Machine Learning Fundamentals',
                    'prerequisites': ['ai_fundamentals'],
                    'order': 6
                },
                {
                    'id': 'deep_learning',
                    'name': 'Deep Learning Fundamentals',
                    'duration_hours': 6,
                    'badge': 'Deep Learning Fundamentals',
                    'prerequisites': ['machine_learning'],
                    'order': 7
                },
                {
                    'id': 'nlp',
                    'name': 'Natural Language Processing Fundamentals',
                    'duration_hours': 5,
                    'badge': 'NLP Fundamentals',
                    'prerequisites': ['machine_learning'],
                    'order': 8
                },
                {
                    'id': 'ai_practitioner_capstone',
                    'name': 'IBM AI Practitioner Capstone',
                    'duration_hours': 10,
                    'badge': 'IBM AI Practitioner',
                    'prerequisites': ['generative_ai', 'watsonx_ai', 'prompt_engineering', 'machine_learning'],
                    'order': 9
                }
            ]
        }
        
        # AWS Cloud Practitioner path
        self.aws_cloud_practitioner_path = {
            'name': 'AWS Cloud Practitioner',
            'total_courses': 6,
            'courses': [
                {'id': 'cloud_essentials', 'name': 'AWS Cloud Essentials', 'duration_hours': 6, 'order': 1},
                {'id': 'cloud_foundations', 'name': 'AWS Cloud Foundations', 'duration_hours': 10, 'order': 2},
                {'id': 'cloud_architecture', 'name': 'AWS Cloud Architecture', 'duration_hours': 8, 'order': 3},
                {'id': 'cloud_security', 'name': 'AWS Cloud Security', 'duration_hours': 6, 'order': 4},
                {'id': 'cloud_billing', 'name': 'AWS Billing and Cost Management', 'duration_hours': 4, 'order': 5},
                {'id': 'cloud_practitioner_exam', 'name': 'AWS Cloud Practitioner Exam Prep', 'duration_hours': 6, 'order': 6}
            ]
        }
    
    def _load_config(self, path):
        default_config = {
            'output_dir': './team_output',
            'daily_standup_time': '09:00',
            'weekly_report_day': 'Friday'
        }
        
        if os.path.exists(path):
            with open(path, 'r') as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def set_team_emails(self, emails):
        """Set email addresses for team members"""
        for member_id, email in emails.items():
            if member_id in self.team_members:
                self.team_members[member_id]['email'] = email
    
    def generate_daily_targets(self):
        """Generate daily learning targets for each team member"""
        daily_targets = {}
        
        for member_id, member in self.team_members.items():
            # Determine next course to work on
            next_course = self._get_next_course(member)
            
            if next_course:
                target = {
                    'member_name': member['name'],
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'target_course': next_course['name'],
                    'target_hours': member['daily_target_hours'],
                    'target_modules': self._estimate_modules(next_course['duration_hours'], member['daily_target_hours']),
                    'actions': [
                        f"Log in to IBM SkillsBuild: {member['ibm_portal']}",
                        f"Continue/Start: {next_course['name']}",
                        f"Complete at least {member['daily_target_hours']} hours",
                        'Take notes on key concepts',
                        'Complete all quizzes/assessments'
                    ],
                    'resources': [
                        'IBM SkillsBuild platform',
                        'Course discussion forum',
                        'Team Slack/Discord for questions'
                    ],
                    'check_in': f"End of day: Update progress in team tracker"
                }
                
                daily_targets[member_id] = target
        
        return daily_targets
    
    def _get_next_course(self, member):
        """Determine the next course for a team member"""
        completed = member.get('courses_completed', [])
        in_progress = member.get('courses_in_progress', [])
        
        # If something is in progress, continue that
        if in_progress:
            course_id = in_progress[0]
            for course in self.ibm_ai_practitioner_path['courses']:
                if course['id'] == course_id:
                    return course
        
        # Otherwise, find the next uncompleted course
        for course in sorted(self.ibm_ai_practitioner_path['courses'], key=lambda x: x['order']):
            if course['id'] not in completed:
                # Check prerequisites
                prereqs_met = all(prereq in completed for prereq in course['prerequisites'])
                if prereqs_met:
                    return course
        
        return None
    
    def _estimate_modules(self, course_hours, daily_hours):
        """Estimate number of modules to complete"""
        # Assume average module is 30-45 minutes
        modules_per_hour = 1.5
        total_modules = int(course_hours * modules_per_hour)
        daily_modules = int(daily_hours * modules_per_hour)
        
        return {
            'total_in_course': total_modules,
            'target_today': daily_modules
        }
    
    def update_progress(self, member_id, course_id, status, progress_percent=0):
        """Update a team member's course progress"""
        if member_id not in self.team_members:
            return False
        
        member = self.team_members[member_id]
        
        if status == 'completed':
            if course_id in member['courses_in_progress']:
                member['courses_in_progress'].remove(course_id)
            if course_id not in member['courses_completed']:
                member['courses_completed'].append(course_id)
        elif status == 'in_progress':
            if course_id not in member['courses_in_progress']:
                member['courses_in_progress'].append(course_id)
        
        member['last_updated'] = datetime.now().isoformat()
        
        return True
    
    def generate_progress_report(self, member_id=None):
        """Generate progress report for one or all team members"""
        if member_id:
            members = {member_id: self.team_members[member_id]} if member_id in self.team_members else {}
        else:
            members = self.team_members
        
        reports = {}
        
        for m_id, member in members.items():
            completed = len(member.get('courses_completed', []))
            in_progress = len(member.get('courses_in_progress', []))
            total_courses = self.ibm_ai_practitioner_path['total_courses']
            
            progress_percent = (completed / total_courses) * 100 if total_courses > 0 else 0
            
            # Calculate estimated completion
            remaining_courses = total_courses - completed
            estimated_days = remaining_courses * 5  # Assume 5 days per course on average
            estimated_completion = datetime.now() + timedelta(days=estimated_days)
            
            report = {
                'member_name': member['name'],
                'report_date': datetime.now().strftime('%Y-%m-%d'),
                'path': member['current_path'],
                'summary': {
                    'courses_completed': completed,
                    'courses_in_progress': in_progress,
                    'total_courses': total_courses,
                    'progress_percent': round(progress_percent, 1),
                    'estimated_completion': estimated_completion.strftime('%Y-%m-%d')
                },
                'completed_courses': member.get('courses_completed', []),
                'in_progress_courses': member.get('courses_in_progress', []),
                'next_courses': self._get_upcoming_courses(member),
                'recommendations': self._generate_recommendations(member)
            }
            
            reports[m_id] = report
        
        return reports
    
    def _get_upcoming_courses(self, member):
        """Get list of upcoming courses for a member"""
        completed = member.get('courses_completed', [])
        upcoming = []
        
        for course in sorted(self.ibm_ai_practitioner_path['courses'], key=lambda x: x['order']):
            if course['id'] not in completed:
                prereqs_met = all(prereq in completed for prereq in course['prerequisites'])
                if prereqs_met:
                    upcoming.append({
                        'id': course['id'],
                        'name': course['name'],
                        'duration_hours': course['duration_hours'],
                        'badge': course.get('badge', ''),
                        'prerequisites_met': prereqs_met
                    })
        
        return upcoming[:3]  # Return next 3 courses
    
    def _generate_recommendations(self, member):
        """Generate personalized recommendations"""
        recommendations = []
        
        completed = len(member.get('courses_completed', []))
        in_progress = len(member.get('courses_in_progress', []))
        
        if completed == 0 and in_progress == 0:
            recommendations.append("Start with IBM AI Fundamentals immediately")
        elif in_progress > 1:
            recommendations.append("Focus on completing one course at a time for better retention")
        elif completed >= 5:
            recommendations.append("Consider starting AWS Cloud Practitioner path in parallel")
        
        # Check pace
        start_date = datetime.strptime(member['start_date'], '%Y-%m-%d')
        days_active = (datetime.now() - start_date).days
        expected_courses = days_active / 7  # Assume 1 course per week
        
        if completed < expected_courses - 1:
            recommendations.append("Current pace is behind target. Increase daily study time to 3 hours")
        elif completed > expected_courses + 1:
            recommendations.append("Excellent pace! Consider taking on additional responsibilities")
        
        return recommendations
    
    def generate_standup_notes(self):
        """Generate standup meeting notes template"""
        standup = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'meeting_type': 'Daily Standup',
            'template': {
                'yesterday': 'What did you complete yesterday?',
                'today': 'What will you work on today?',
                'blockers': 'Any blockers or help needed?'
            },
            'team_updates': {}
        }
        
        for member_id, member in self.team_members.items():
            next_course = self._get_next_course(member)
            standup['team_updates'][member_id] = {
                'name': member['name'],
                'current_focus': next_course['name'] if next_course else 'Path Complete!',
                'suggested_update': f"Working on {next_course['name'] if next_course else 'reviewing completed material'}"
            }
        
        return standup
    
    def generate_weekly_summary(self):
        """Generate weekly summary for founder"""
        weekly = {
            'week_ending': datetime.now().strftime('%Y-%m-%d'),
            'team_overview': {},
            'achievements': [],
            'concerns': [],
            'actions_for_founder': []
        }
        
        total_completed = 0
        total_target = len(self.team_members) * self.ibm_ai_practitioner_path['total_courses']
        
        for member_id, member in self.team_members.items():
            completed = len(member.get('courses_completed', []))
            total_completed += completed
            
            weekly['team_overview'][member_id] = {
                'name': member['name'],
                'courses_completed': completed,
                'progress_percent': round((completed / self.ibm_ai_practitioner_path['total_courses']) * 100, 1),
                'status': 'on_track' if completed >= 2 else 'needs_support'
            }
            
            if completed >= 2:
                weekly['achievements'].append(f"{member['name']} completed {completed} courses")
            else:
                weekly['concerns'].append(f"{member['name']} may need additional support")
        
        weekly['overall_progress'] = round((total_completed / total_target) * 100, 1)
        
        weekly['actions_for_founder'] = [
            'Review individual progress with each team member',
            'Identify and address any blockers',
            'Celebrate wins and milestones',
            'Adjust targets if needed'
        ]
        
        return weekly
    
    def save_all(self):
        """Save all team tracking data"""
        os.makedirs(self.config['output_dir'], exist_ok=True)
        
        # Save team data
        team_path = os.path.join(self.config['output_dir'], 'team_data.json')
        with open(team_path, 'w') as f:
            json.dump(self.team_members, f, indent=2)
        
        # Save daily targets
        daily_targets = self.generate_daily_targets()
        targets_path = os.path.join(self.config['output_dir'], f"daily_targets_{datetime.now().strftime('%Y%m%d')}.json")
        with open(targets_path, 'w') as f:
            json.dump(daily_targets, f, indent=2)
        
        # Save progress reports
        progress_reports = self.generate_progress_report()
        progress_path = os.path.join(self.config['output_dir'], 'progress_reports.json')
        with open(progress_path, 'w') as f:
            json.dump(progress_reports, f, indent=2)
        
        # Save standup notes
        standup = self.generate_standup_notes()
        standup_path = os.path.join(self.config['output_dir'], f"standup_{datetime.now().strftime('%Y%m%d')}.json")
        with open(standup_path, 'w') as f:
            json.dump(standup, f, indent=2)
        
        # Save weekly summary
        weekly = self.generate_weekly_summary()
        weekly_path = os.path.join(self.config['output_dir'], f"weekly_summary_{datetime.now().strftime('%Y%m%d')}.json")
        with open(weekly_path, 'w') as f:
            json.dump(weekly, f, indent=2)
        
        # Generate markdown report
        md_report = self._generate_markdown_report(progress_reports, daily_targets)
        md_path = os.path.join(self.config['output_dir'], 'TEAM_PROGRESS_REPORT.md')
        with open(md_path, 'w') as f:
            f.write(md_report)
        
        print(f"\n{'='*60}")
        print(f"👥 Kgotla AI Team Tracker - Reports Generated")
        print(f"{'='*60}\n")
        
        print(f"📁 Files created:")
        print(f"   • {team_path}")
        print(f"   • {targets_path}")
        print(f"   • {progress_path}")
        print(f"   • {standup_path}")
        print(f"   • {weekly_path}")
        print(f"   • {md_path}\n")
        
        print(f"📊 TEAM PROGRESS OVERVIEW:")
        for member_id, report in progress_reports.items():
            summary = report['summary']
            print(f"   {report['member_name']}: {summary['courses_completed']}/{summary['total_courses']} courses ({summary['progress_percent']}%)")
        
        print(f"\n✅ DAILY TARGETS SENT:")
        for member_id, target in daily_targets.items():
            print(f"   {target['member_name']}: {target['target_course']} ({target['target_hours']} hours)")
        
        print(f"\n{'='*60}\n")
        
        return team_path, targets_path, progress_path, md_path
    
    def _generate_markdown_report(self, progress_reports, daily_targets):
        """Generate markdown progress report"""
        md = f"""# Kgotla AI Team Progress Report
**Report Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📊 Individual Progress

"""
        
        for member_id, report in progress_reports.items():
            summary = report['summary']
            md += f"""### {report['member_name']}
- **Path:** {report['path']}
- **Progress:** {summary['courses_completed']}/{summary['total_courses']} courses ({summary['progress_percent']}%)
- **Estimated Completion:** {summary['estimated_completion']}

**Completed Courses:**
"""
            for course in report['completed_courses']:
                md += f"- ✅ {course}\n"
            
            md += f"\n**In Progress:**\n"
            for course in report['in_progress_courses']:
                md += f"- 🔄 {course}\n"
            
            md += f"\n**Next Up:**\n"
            for course in report['next_courses']:
                md += f"- 📚 {course['name']} ({course['duration_hours']} hours)\n"
            
            md += f"\n**Recommendations:**\n"
            for rec in report['recommendations']:
                md += f"- 💡 {rec}\n"
            
            md += "\n---\n\n"
        
        md += f"""## 🎯 Today's Targets ({datetime.now().strftime('%Y-%m-%d')})

"""
        
        for member_id, target in daily_targets.items():
            md += f"""### {target['member_name']}
- **Course:** {target['target_course']}
- **Target Hours:** {target['target_hours']}
- **Target Modules:** {target['target_modules']['target_today']}

**Actions:**
"""
            for action in target['actions']:
                md += f"- {action}\n"
            
            md += "\n"
        
        md += """---

## 📋 Standup Template

**Yesterday:**
- What did you complete?

**Today:**
- What will you work on?

**Blockers:**
- Any challenges or help needed?

---

**Next Review:** """ + (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d') + """
"""
        
        return md

if __name__ == '__main__':
    tracker = TeamTracker()
    
    # Example: Set team emails when provided
    # tracker.set_team_emails({
    #     'thando': 'thando@kgotlaai.co.za',
    #     'samkelo': 'samkelo@kgotlaai.co.za',
    #     'lorraine': 'lorraine@kgotlaai.co.za'
    # })
    
    # Example: Update progress
    # tracker.update_progress('thando', 'ai_fundamentals', 'completed')
    # tracker.update_progress('samkelo', 'ai_fundamentals', 'in_progress')
    
    tracker.save_all()
