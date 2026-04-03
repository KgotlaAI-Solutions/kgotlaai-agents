#!/usr/bin/env python3
"""
Kgotla AI - Content Machine Agent
Automated content generation and posting for LinkedIn, Twitter/X
Daily posts targeting mining, manufacturing, power, heavy industry
"""

import json
import random
from datetime import datetime, timedelta
import os

class ContentMachine:
    def __init__(self, config_path='../shared-config/config.json'):
        self.config = self._load_config(config_path)
        self.posts_generated = []
        
        # Content themes based on Kgotla AI positioning
        self.content_themes = {
            'case_studies': {
                'weight': 0.20,
                'templates': [
                    "Reduced {metric} by {percentage}% for a {industry} client using {technology}. The key? {insight}. DM me if you're facing similar challenges. #{hashtag1} #{hashtag2}",
                    "Last month we helped {company_type} save {amount} annually by automating {process}. Here's how: {brief_explanation}. #{hashtag1}",
                    "Client win: {industry} operation now predicts equipment failures {timeframe} in advance. Downtime down {percentage}%. AI isn't the future—it's the present. #{hashtag1} #{hashtag2}"
                ]
            },
            'industry_insights': {
                'weight': 0.25,
                'templates': [
                    "The {industry} sector in South Africa loses {amount} annually to {problem}. AI-powered {solution} can cut that by {percentage}%. Here's why most companies miss this opportunity... 🧵",
                    "3 ways AI is transforming {industry} in 2025:\n1. {point1}\n2. {point2}\n3. {point3}\n\nWhich one would impact your operation most? #{hashtag1} #{hashtag2}",
                    "I spent {timeframe} analyzing {data_source}. Here's what shocked me about {industry} operations in South Africa:\n\n{insight1}\n{insight2}\n{insight3}\n\nThe data doesn't lie. #{hashtag1}"
                ]
            },
            'thought_leadership': {
                'weight': 0.20,
                'templates': [
                    "Most {industry} companies think AI is expensive. They're wrong.\n\nThe real cost is:\n• {cost1}\n• {cost2}\n• {cost3}\n\nA well-designed AI pilot pays for itself in {timeframe}. Here's the framework I use...",
                    "Why I started Kgotla AI after {experience}:\n\nI saw {problem} happening repeatedly in {industry}. Smart people. Good intentions. But {issue}.\n\nAI isn't magic. It's a tool. And like any tool, it needs the right craftsman. #{hashtag1}",
                    "Unpopular opinion: {controversial_statement}\n\nHere's why: {explanation}\n\nAgree or disagree? Let's discuss. 👇 #{hashtag1} #{hashtag2}"
                ]
            },
            'educational': {
                'weight': 0.20,
                'templates': [
                    "AI 101 for {industry} leaders:\n\n{concept} = {simple_explanation}\n\nReal example: {example}\n\nWhy it matters: {impact}\n\nSave this for your next strategy meeting. #{hashtag1}",
                    "What's the difference between {term1} and {term2}?\n\n{term1}: {definition1}\n{term2}: {definition2}\n\nIn practice: {practical_example}\n\nKnowing this saves you from {mistake}. #{hashtag1} #{hashtag2}",
                    "5 signs your {industry} operation needs AI:\n\n1. {sign1}\n2. {sign2}\n3. {sign3}\n4. {sign4}\n5. {sign5}\n\nIf you checked 3+, let's talk. Link in bio. #{hashtag1}"
                ]
            },
            'personal_brand': {
                'weight': 0.15,
                'templates': [
                    "Behind the scenes at Kgotla AI:\n\n{activity}\n\nBuilding AI solutions for {industry} isn't glamorous. It's {reality}. But when a client calls to say they saved {amount} or prevented {incident}, it's worth every late night. #{hashtag1}",
                    "What I'm reading this week:\n\n📚 {book1} - {why1}\n📚 {book2} - {why2}\n📚 {book3} - {why3}\n\nAny recommendations for {topic}? Drop them below. 👇",
                    "From {past_position} to founding an AI consultancy serving {industry}:\n\nThe biggest lesson? {lesson}\n\nThe hardest part? {challenge}\n\nThe most rewarding? {reward}\n\nTo anyone building something: {advice}. #{hashtag1}"
                ]
            }
        }
        
        # Industry data for content
        self.industry_data = {
            'mining': {
                'problems': ['unplanned downtime', 'safety incidents', 'equipment failures', 'inefficient blasting', 'ore grade variability'],
                'solutions': ['predictive maintenance', 'computer vision safety monitoring', 'autonomous drilling optimization', 'real-time grade control'],
                'metrics': ['downtime', 'safety incidents', 'equipment availability', 'throughput', 'recovery rate'],
                'hashtags': ['MiningInnovation', 'SmartMining', 'MiningAI', 'SouthAfricaMining'],
                'amounts': ['R50 million', 'R100 million', 'R500 million', 'billions']
            },
            'manufacturing': {
                'problems': ['quality defects', 'production bottlenecks', 'inventory mismanagement', 'energy waste', 'supply chain disruptions'],
                'solutions': ['quality prediction', 'demand forecasting', 'energy optimization', 'predictive maintenance', 'supply chain visibility'],
                'metrics': ['defect rate', 'OEE', 'energy consumption', 'inventory turnover', 'on-time delivery'],
                'hashtags': ['Industry40', 'SmartManufacturing', 'ManufacturingAI', 'DigitalTransformation'],
                'amounts': ['R10 million', 'R25 million', 'R75 million', 'hundreds of millions']
            },
            'power': {
                'problems': ['grid instability', 'asset failures', 'demand forecasting errors', 'maintenance costs', 'renewable integration'],
                'solutions': ['grid optimization', 'asset health monitoring', 'demand prediction', 'predictive maintenance', 'energy storage optimization'],
                'metrics': ['SAIDI', 'SAIFI', 'asset availability', 'forecast accuracy', 'operational costs'],
                'hashtags': ['EnergyTransition', 'GridModernization', 'PowerAI', 'RenewableEnergy'],
                'amounts': ['R100 million', 'R500 million', 'R1 billion', 'tens of billions']
            },
            'logistics': {
                'problems': ['route inefficiencies', 'fuel costs', 'delivery delays', 'fleet utilization', 'theft and loss'],
                'solutions': ['route optimization', 'predictive analytics', 'real-time tracking', 'demand forecasting', 'automated dispatch'],
                'metrics': ['fuel efficiency', 'on-time delivery', 'fleet utilization', 'cost per km', 'customer satisfaction'],
                'hashtags': ['SupplyChain', 'LogisticsAI', 'FleetManagement', 'SmartLogistics'],
                'amounts': ['R5 million', 'R20 million', 'R50 million', 'hundreds of millions']
            },
            'heavy_industry': {
                'problems': ['process inefficiencies', 'safety compliance', 'environmental impact', 'equipment reliability', 'skilled labor shortage'],
                'solutions': ['process optimization', 'safety AI', 'emissions monitoring', 'predictive maintenance', 'knowledge capture'],
                'metrics': ['process yield', 'safety incidents', 'emissions', 'uptime', 'training time'],
                'hashtags': ['HeavyIndustry', 'IndustrialAI', 'ProcessOptimization', 'SafetyFirst'],
                'amounts': ['R25 million', 'R100 million', 'R250 million', 'billions']
            }
        }
    
    def _load_config(self, path):
        default_config = {
            'company_name': 'Kgotla AI',
            'founder_name': 'Mahlo Kgotleng',
            'linkedin_url': 'https://www.linkedin.com/in/mahlo-kgotleng-473830194',
            'website': 'kgotlaai.co.za',
            'output_dir': './content_output'
        }
        
        if os.path.exists(path):
            with open(path, 'r') as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def _select_theme(self):
        """Select content theme based on weights"""
        themes = list(self.content_themes.keys())
        weights = [self.content_themes[t]['weight'] for t in themes]
        return random.choices(themes, weights=weights, k=1)[0]
    
    def _select_industry(self):
        """Randomly select industry for content"""
        return random.choice(list(self.industry_data.keys()))
    
    def _generate_case_study_post(self, industry):
        """Generate case study style post"""
        data = self.industry_data[industry]
        template = random.choice(self.content_themes['case_studies']['templates'])
        
        variables = {
            'metric': random.choice(data['metrics']),
            'percentage': random.choice(['25', '30', '35', '40', '45', '50']),
            'industry': industry,
            'technology': random.choice(data['solutions']),
            'insight': random.choice([
                'Starting with clean data beats fancy algorithms',
                'Getting buy-in from operators was harder than building the model',
                'We focused on one use case and scaled from there',
                'The real value was in the insights, not the predictions'
            ]),
            'hashtag1': random.choice(data['hashtags']),
            'hashtag2': random.choice(['AI', 'Innovation', 'SouthAfrica', 'KgotlaAI']),
            'company_type': random.choice(['a major', 'a mid-sized', 'an emerging']),
            'amount': random.choice(['R5M', 'R10M', 'R15M', 'R20M']),
            'process': random.choice(data['solutions']),
            'brief_explanation': random.choice([
                'combining IoT sensors with ML models',
                'automating manual data entry and analysis',
                'predicting failures before they happen'
            ]),
            'timeframe': random.choice(['48 hours', '1 week', '2 weeks', '1 month'])
        }
        
        return template.format(**variables)
    
    def _generate_insight_post(self, industry):
        """Generate industry insight post"""
        data = self.industry_data[industry]
        template = random.choice(self.content_themes['industry_insights']['templates'])
        
        variables = {
            'industry': industry.title(),
            'amount': random.choice(data['amounts']),
            'problem': random.choice(data['problems']),
            'solution': random.choice(data['solutions']),
            'percentage': random.choice(['20', '30', '40', '50', '60']),
            'hashtag1': random.choice(data['hashtags']),
            'hashtag2': random.choice(['DigitalTransformation', 'AI', 'Innovation']),
            'point1': random.choice(data['solutions']),
            'point2': random.choice([s for s in data['solutions'] if s != random.choice(data['solutions'])]),
            'point3': random.choice([s for s in data['solutions'] if s != random.choice(data['solutions'])]),
            'timeframe': random.choice(['6 months', 'the last year', '2024', 'the past quarter']),
            'data_source': random.choice(['EskomSePush data', 'DMR reports', 'industry benchmarks', 'client operations']),
            'insight1': f"• {random.choice(data['problems'])} affects {random.choice(['60%', '70%', '80%'])} of operations",
            'insight2': f"• Companies using {random.choice(data['solutions'])} see {random.choice(['2x', '3x', '4x'])} ROI",
            'insight3': f"• The gap between leaders and laggards is widening"
        }
        
        return template.format(**variables)
    
    def _generate_thought_leadership_post(self, industry):
        """Generate thought leadership post"""
        data = self.industry_data[industry]
        template = random.choice(self.content_themes['thought_leadership']['templates'])
        
        variables = {
            'industry': industry.title(),
            'cost1': random.choice(['missed opportunities', 'competitive disadvantage', 'talent attrition']),
            'cost2': random.choice(['operational inefficiency', 'safety incidents', 'regulatory non-compliance']),
            'cost3': random.choice(['customer churn', 'market share loss', 'innovation stagnation']),
            'timeframe': random.choice(['3 months', '6 months', 'the first year']),
            'experience': random.choice(['10 years in industrial operations', 'consulting for Fortune 500 companies', 'building AI systems']),
            'problem': random.choice(data['problems']),
            'issue': random.choice(['legacy thinking', 'fear of change', 'analysis paralysis']),
            'hashtag1': random.choice(data['hashtags']),
            'controversial_statement': random.choice([
                f"Most {industry} AI projects fail in the first 6 months.",
                f"Your data scientists might be hurting your {industry} operation.",
                f"{industry.title()} doesn't need more AI—it needs better AI implementation."
            ]),
            'explanation': random.choice([
                'Technology is easy. Change management is hard.',
                'Fancy models mean nothing if operators don\'t trust them.',
                'The best AI is invisible—it just makes things work better.'
            ]),
            'hashtag2': random.choice(['ThoughtLeadership', 'AI', 'Innovation'])
        }
        
        return template.format(**variables)
    
    def _generate_educational_post(self, industry):
        """Generate educational post"""
        data = self.industry_data[industry]
        template = random.choice(self.content_themes['educational']['templates'])
        
        concepts = {
            'predictive maintenance': 'using data to fix things BEFORE they break',
            'machine learning': 'teaching computers to learn from examples',
            'computer vision': 'AI that can see and understand images',
            'digital twin': 'a virtual copy of your physical operation'
        }
        
        concept = random.choice(list(concepts.keys()))
        
        variables = {
            'industry': industry.title(),
            'concept': concept,
            'simple_explanation': concepts[concept],
            'example': random.choice([
                f'We used {concept} to reduce {random.choice(data["problems"])} by 40%',
                f'A client saved {random.choice(data["amounts"])} using {concept}'
            ]),
            'impact': random.choice([
                f'Prevents {random.choice(data["problems"])}',
                f'Reduces costs by {random.choice(["20-30%", "30-50%"])}',
                f'Improves {random.choice(data["metrics"])}'
            ]),
            'hashtag1': random.choice(data['hashtags']),
            'term1': random.choice(list(concepts.keys())),
            'term2': random.choice([t for t in concepts.keys() if t != concept]),
            'definition1': 'AI that learns patterns from data',
            'definition2': 'rules-based automation',
            'practical_example': random.choice([
                'ML adapts to new situations; traditional automation follows fixed rules',
                'ML improves over time; traditional systems stay the same'
            ]),
            'mistake': random.choice(['buying the wrong solution', 'wasting budget', 'frustrating your team']),
            'hashtag2': random.choice(['AI101', 'LearnAI', 'TechEducation']),
            'sign1': random.choice(data['problems']),
            'sign2': random.choice([p for p in data['problems'] if p != random.choice(data['problems'])]),
            'sign3': 'Data exists but decisions are gut-based',
            'sign4': 'Competitors are pulling ahead',
            'sign5': 'IT and Operations don\'t collaborate'
        }
        
        return template.format(**variables)
    
    def _generate_personal_post(self, industry):
        """Generate personal brand post"""
        data = self.industry_data[industry]
        template = random.choice(self.content_themes['personal_brand']['templates'])
        
        variables = {
            'activity': random.choice([
                f'Debugging a model for {industry} at 2AM',
                'Client call about scaling their AI pilot',
                f'Reviewing safety data from a {industry} site',
                'Teaching the team about a new technique'
            ]),
            'industry': industry.title(),
            'reality': random.choice(['gritty', 'challenging', 'complex', 'demanding']),
            'amount': random.choice(['R10M', 'their first million', 'hundreds of hours']),
            'incident': random.choice(['a major safety event', 'catastrophic downtime']),
            'hashtag1': random.choice(['EntrepreneurLife', 'BehindTheScenes', 'KgotlaAI']),
            'book1': random.choice(['Prediction Machines', 'AI Superpowers', 'The Second Machine Age']),
            'why1': random.choice(['essential for understanding AI economics', 'great perspective on global AI race']),
            'book2': random.choice(['The Lean Startup', 'Zero to One', 'Good to Great']),
            'why2': random.choice(['building companies in uncertain environments', 'what makes companies truly great']),
            'book3': random.choice(['Thinking in Bets', 'Range', 'Atomic Habits']),
            'why3': random.choice(['decision-making under uncertainty', 'why generalists triumph']),
            'topic': random.choice(['AI strategy', 'industrial innovation', 'building in Africa']),
            'past_position': random.choice(['corporate', 'consulting', 'engineering']),
            'lesson': random.choice([
                'Execution beats strategy',
                'Relationships matter more than credentials',
                'The best technology is useless without adoption'
            ]),
            'challenge': random.choice([
                'proving value without a track record',
                'balancing vision with cash flow',
                'building a team that believes'
            ]),
            'reward': random.choice([
                'seeing clients transform their operations',
                'building something that outlasts me',
                'proving what\'s possible in Africa'
            ]),
            'advice': random.choice([
                'Start before you\'re ready',
                'Focus on solving real problems',
                'Build relationships, not just products'
            ]),
            'hashtag1': random.choice(['FounderJourney', 'AfricanInnovation', 'BuildInPublic'])
        }
        
        return template.format(**variables)
    
    def generate_daily_content(self, num_posts=3):
        """Generate a day's worth of content"""
        print(f"\n{'='*60}")
        print(f"📝 Kgotla AI Content Machine - {datetime.now().strftime('%Y-%m-%d')}")
        print(f"{'='*60}\n")
        
        posts = []
        
        for i in range(num_posts):
            theme = self._select_theme()
            industry = self._select_industry()
            
            if theme == 'case_studies':
                content = self._generate_case_study_post(industry)
            elif theme == 'industry_insights':
                content = self._generate_insight_post(industry)
            elif theme == 'thought_leadership':
                content = self._generate_thought_leadership_post(industry)
            elif theme == 'educational':
                content = self._generate_educational_post(industry)
            else:
                content = self._generate_personal_post(industry)
            
            post = {
                'id': f"post_{datetime.now().strftime('%Y%m%d')}_{i+1}",
                'theme': theme,
                'industry': industry,
                'content': content,
                'platform': 'LinkedIn',
                'scheduled_time': self._suggest_post_time(i),
                'status': 'ready_to_post',
                'created_at': datetime.now().isoformat()
            }
            
            posts.append(post)
            print(f"✅ Post {i+1} ({theme.replace('_', ' ').title()} - {industry.title()})")
            print(f"   {content[:100]}...\n")
        
        # Save posts
        os.makedirs(self.config['output_dir'], exist_ok=True)
        
        # Save as JSON
        json_path = os.path.join(self.config['output_dir'], f"content_{datetime.now().strftime('%Y%m%d')}.json")
        with open(json_path, 'w') as f:
            json.dump(posts, f, indent=2)
        
        # Save as formatted text
        txt_path = os.path.join(self.config['output_dir'], f"content_{datetime.now().strftime('%Y%m%d')}.txt")
        with open(txt_path, 'w') as f:
            for post in posts:
                f.write(f"\n{'='*60}\n")
                f.write(f"POST {post['id']}\n")
                f.write(f"Theme: {post['theme']}\n")
                f.write(f"Industry: {post['industry']}\n")
                f.write(f"Suggested Time: {post['scheduled_time']}\n")
                f.write(f"{'='*60}\n\n")
                f.write(post['content'])
                f.write("\n\n")
        
        print(f"📁 Saved to:")
        print(f"   JSON: {json_path}")
        print(f"   TXT: {txt_path}")
        print(f"\n{'='*60}\n")
        
        return posts
    
    def _suggest_post_time(self, post_index):
        """Suggest optimal posting times"""
        base_times = ['08:00', '12:30', '17:00']
        return base_times[post_index % len(base_times)]
    
    def generate_content_calendar(self, days=30):
        """Generate a full month of content"""
        print(f"Generating {days}-day content calendar...\n")
        
        calendar = []
        for day in range(days):
            date = datetime.now() + timedelta(days=day)
            print(f"Day {day+1}: {date.strftime('%Y-%m-%d')}")
            
            # 3 posts per day
            posts = self.generate_daily_content(num_posts=3)
            calendar.extend(posts)
        
        # Save full calendar
        calendar_path = os.path.join(self.config['output_dir'], 'content_calendar_30days.json')
        with open(calendar_path, 'w') as f:
            json.dump(calendar, f, indent=2)
        
        print(f"\n✅ Full calendar saved: {calendar_path}")
        print(f"   Total posts: {len(calendar)}")
        
        return calendar

if __name__ == '__main__':
    machine = ContentMachine()
    
    # Generate today's content
    posts = machine.generate_daily_content(num_posts=3)
    
    # Uncomment to generate full month
    # machine.generate_content_calendar(days=30)
