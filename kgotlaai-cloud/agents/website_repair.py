#!/usr/bin/env python3
"""
Kgotla AI - Website Repair Agent
Fixes HTTPS issues, broken demos, SSL certificates
Optimizes for conversions and SEO
"""

import json
import os
import re
from datetime import datetime

class WebsiteRepair:
    def __init__(self, config_path='../shared-config/config.json'):
        self.config = self._load_config(config_path)
        self.domain = 'kgotlaai.co.za'
        self.issues_found = []
        self.fixes_applied = []
        
        # Common website issues to check
        self.checklist = {
            'ssl_https': {
                'description': 'SSL certificate and HTTPS enforcement',
                'critical': True,
                'checks': [
                    'HTTPS redirect from HTTP',
                    'SSL certificate validity',
                    'Mixed content (HTTP resources on HTTPS page)',
                    'HSTS header'
                ]
            },
            'broken_links': {
                'description': 'Broken internal and external links',
                'critical': True,
                'checks': [
                    'Demo links functionality',
                    'Navigation menu links',
                    'Footer links',
                    'External partner links'
                ]
            },
            'performance': {
                'description': 'Page load speed and performance',
                'critical': False,
                'checks': [
                    'Image optimization',
                    'JavaScript/CSS minification',
                    'Server response time',
                    'Caching headers'
                ]
            },
            'seo': {
                'description': 'Search engine optimization',
                'critical': False,
                'checks': [
                    'Meta titles and descriptions',
                    'Heading structure (H1, H2, H3)',
                    'XML sitemap',
                    'robots.txt',
                    'Open Graph tags'
                ]
            },
            'mobile': {
                'description': 'Mobile responsiveness',
                'critical': True,
                'checks': [
                    'Viewport meta tag',
                    'Touch-friendly elements',
                    'Mobile menu functionality'
                ]
            },
            'conversion': {
                'description': 'Conversion optimization',
                'critical': True,
                'checks': [
                    'Clear call-to-action buttons',
                    'Contact form functionality',
                    'Trust signals (testimonials, logos)',
                    'Loading states for demos'
                ]
            }
        }
    
    def _load_config(self, path):
        default_config = {
            'domain': 'kgotlaai.co.za',
            'github_repo': 'kgotlaai/website',
            'hosting': ['Host Africa', 'GitHub Pages', 'Vercel', 'Cloudflare'],
            'output_dir': './website_fixes'
        }
        
        if os.path.exists(path):
            with open(path, 'r') as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def generate_ssl_fix_guide(self):
        """Generate step-by-step SSL/HTTPS fix guide"""
        guide = {
            'title': 'Kgotla AI Website SSL/HTTPS Fix Guide',
            'priority': 'CRITICAL',
            'estimated_time': '2-4 hours',
            'steps': []
        }
        
        # Step 1: Cloudflare SSL Configuration
        guide['steps'].append({
            'step': 1,
            'title': 'Configure Cloudflare SSL/TLS',
            'platform': 'Cloudflare',
            'instructions': [
                'Log in to Cloudflare dashboard (dash.cloudflare.com)',
                'Select your domain: kgotlaai.co.za',
                'Go to SSL/TLS → Overview',
                'Set SSL/TLS encryption mode to "Full (strict)"',
                'Enable "Always Use HTTPS" in Edge Certificates',
                'Enable "Automatic HTTPS Rewrites"',
                'Set Minimum TLS Version to 1.2'
            ],
            'verification': 'Visit http://kgotlaai.co.za - should redirect to https://kgotlaai.co.za'
        })
        
        # Step 2: Fix Mixed Content
        guide['steps'].append({
            'step': 2,
            'title': 'Fix Mixed Content Issues',
            'platform': 'GitHub Repository',
            'instructions': [
                'Clone your website repository: git clone https://github.com/kgotlaai/website.git',
                'Search for http:// references: grep -r "http://" . --include="*.html" --include="*.css" --include="*.js"',
                'Replace all http:// with https:// in HTML/CSS/JS files',
                'Check for protocol-relative URLs (//example.com) and ensure they work',
                'Update any external resources (fonts, scripts, images) to use HTTPS'
            ],
            'common_issues': [
                'Google Fonts loading over HTTP',
                'CDN scripts (jQuery, Bootstrap) using HTTP',
                'Images from external sources',
                'API endpoints hardcoded with HTTP'
            ],
            'verification': 'Use Chrome DevTools → Security tab to check for mixed content'
        })
        
        # Step 3: GitHub Pages HTTPS
        guide['steps'].append({
            'step': 3,
            'title': 'Enable HTTPS on GitHub Pages',
            'platform': 'GitHub',
            'instructions': [
                'Go to github.com/kgotlaai/website/settings/pages',
                'Under "GitHub Pages" section',
                'Check "Enforce HTTPS" checkbox',
                'Ensure custom domain is set to kgotlaai.co.za',
                'Wait 5-10 minutes for DNS propagation'
            ],
            'verification': 'GitHub Pages shows "Your site is published at https://kgotlaai.co.za"'
        })
        
        # Step 4: Vercel Configuration
        guide['steps'].append({
            'step': 4,
            'title': 'Configure Vercel SSL',
            'platform': 'Vercel',
            'instructions': [
                'Log in to vercel.com dashboard',
                'Select your Kgotla AI project',
                'Go to Settings → Domains',
                'Verify kgotlaai.co.za is configured',
                'Enable "HTTPS Only" if available',
                'Check that SSL certificate is auto-provisioned'
            ],
            'verification': 'Vercel dashboard shows SSL certificate as "Active"'
        })
        
        # Step 5: DNS Configuration
        guide['steps'].append({
            'step': 5,
            'title': 'Verify DNS Configuration',
            'platform': 'Host Africa / DNS Provider',
            'instructions': [
                'Log in to Host Africa control panel',
                'Check DNS records for kgotlaai.co.za',
                'Ensure A records point to correct IPs:',
                '  - For Cloudflare: Use Cloudflare nameservers',
                '  - For GitHub Pages: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153',
                '  - For Vercel: 76.76.21.21',
                'Ensure CNAME record for www points to @ or appropriate target',
                'Check TTL values (recommend 300 for quick changes)'
            ],
            'verification': 'Run: dig kgotlaai.co.za +short - should show correct IPs'
        })
        
        return guide
    
    def generate_demo_fix_guide(self):
        """Generate guide for fixing broken demos"""
        guide = {
            'title': 'Fix Broken Demo Components',
            'priority': 'HIGH',
            'estimated_time': '3-6 hours',
            'demo_issues': []
        }
        
        # Common demo issues and fixes
        demo_fixes = [
            {
                'issue': 'RAG Chatbot Demo Not Working',
                'symptoms': [
                    'Chat interface loads but no responses',
                    'Error messages in console',
                    'API endpoint returning 404/500'
                ],
                'fixes': [
                    'Check if backend API is running (IBM watsonx, custom server)',
                    'Verify API endpoint URL in frontend code',
                    'Check API key/environment variables',
                    'Test API independently using curl or Postman',
                    'Add error handling and user-friendly error messages',
                    'Consider using a mock/demo mode for static sites'
                ],
                'fallback_solution': 'Replace live demo with recorded video/screenshots until backend is fixed'
            },
            {
                'issue': 'Demo Links Return 404',
                'symptoms': [
                    'Clicking demo button shows 404 page',
                    'Demo page missing from build'
                ],
                'fixes': [
                    'Check if demo HTML/JS files exist in repository',
                    'Verify file paths in navigation links',
                    'Check build process includes demo files',
                    'Ensure case sensitivity matches (Demo.html vs demo.html)'
                ]
            },
            {
                'issue': 'Interactive Elements Not Responding',
                'symptoms': [
                    'Buttons don\'t work',
                    'Forms don\'t submit',
                    'Animations broken'
                ],
                'fixes': [
                    'Check browser console for JavaScript errors',
                    'Verify jQuery/other libraries loaded correctly',
                    'Check for JavaScript file loading over HTTP (mixed content)',
                    'Test in multiple browsers (Chrome, Firefox, Safari)',
                    'Ensure event listeners attached after DOM loads'
                ]
            },
            {
                'issue': 'Slow Loading Demos',
                'symptoms': [
                    'Demo takes >5 seconds to load',
                    'Images/assets loading slowly'
                ],
                'fixes': [
                    'Optimize images (compress, use WebP format)',
                    'Lazy load demo components',
                    'Minify CSS/JS files',
                    'Use CDN for static assets',
                    'Add loading indicators'
                ]
            }
        ]
        
        guide['demo_issues'] = demo_fixes
        
        # Quick fix template
        guide['quick_fix_template'] = """
<!-- Demo Placeholder Template - Use while fixing live demo -->
<div class="demo-container">
    <div class="demo-video">
        <video controls poster="demo-thumbnail.jpg">
            <source src="demo-video.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    <div class="demo-cta">
        <h3>See AI in Action</h3>
        <p>Watch how Kgotla AI solutions transform industrial operations.</p>
        <a href="#contact" class="btn btn-primary">Request Live Demo</a>
    </div>
</div>
"""
        
        return guide
    
    def generate_seo_optimization_guide(self):
        """Generate SEO optimization recommendations"""
        guide = {
            'title': 'SEO Optimization for Kgotla AI',
            'priority': 'MEDIUM',
            'recommendations': []
        }
        
        # Meta tags template
        guide['recommendations'].append({
            'category': 'Meta Tags',
            'template': """<!-- Add to <head> section of every page -->
<title>Kgotla AI | Industrial AI Solutions for Mining & Manufacturing | South Africa</title>
<meta name="description" content="Kgotla AI delivers enterprise AI solutions for mining, manufacturing, and power industries. Predictive maintenance, safety AI, and automation. Based in South Africa, serving SADC region.">
<meta name="keywords" content="AI South Africa, mining AI, manufacturing automation, predictive maintenance, industrial AI, SADC">
<meta name="author" content="Mahlo Kgotleng">
<meta name="robots" content="index, follow">

<!-- Open Graph -->
<meta property="og:title" content="Kgotla AI | Industrial AI Solutions">
<meta property="og:description" content="Enterprise AI for mining, manufacturing, and power industries">
<meta property="og:image" content="https://kgotlaai.co.za/images/og-image.jpg">
<meta property="og:url" content="https://kgotlaai.co.za">
<meta property="og:type" content="website">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Kgotla AI | Industrial AI Solutions">
<meta name="twitter:description" content="Enterprise AI for mining, manufacturing, and power industries">
<meta name="twitter:image" content="https://kgotlaai.co.za/images/twitter-card.jpg">
"""
        })
        
        # Structured data
        guide['recommendations'].append({
            'category': 'Structured Data (Schema.org)',
            'template': """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Kgotla AI",
  "url": "https://kgotlaai.co.za",
  "logo": "https://kgotlaai.co.za/images/logo.png",
  "description": "Enterprise AI solutions for industrial operations",
  "founder": {
    "@type": "Person",
    "name": "Mahlo Kgotleng"
  },
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "ZA"
  },
  "sameAs": [
    "https://www.linkedin.com/in/mahlo-kgotleng-473830194"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "email": "mahlo@kgotlaai.co.za",
    "contactType": "sales"
  }
}
</script>
"""
        })
        
        # robots.txt
        guide['recommendations'].append({
            'category': 'robots.txt',
            'content': """User-agent: *
Allow: /

Sitemap: https://kgotlaai.co.za/sitemap.xml

# Disallow admin areas if any
Disallow: /admin/
Disallow: /private/
"""
        })
        
        # sitemap.xml template
        guide['recommendations'].append({
            'category': 'sitemap.xml',
            'template': """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://kgotlaai.co.za/</loc>
    <lastmod>2025-01-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://kgotlaai.co.za/services</loc>
    <lastmod>2025-01-01</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://kgotlaai.co.za/case-studies</loc>
    <lastmod>2025-01-01</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://kgotlaai.co.za/about</loc>
    <lastmod>2025-01-01</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
  <url>
    <loc>https://kgotlaai.co.za/contact</loc>
    <lastmod>2025-01-01</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>
"""
        })
        
        return guide
    
    def generate_full_audit_report(self):
        """Generate complete website audit and fix report"""
        report = {
            'audit_date': datetime.now().isoformat(),
            'domain': self.domain,
            'critical_issues': [],
            'high_priority': [],
            'medium_priority': [],
            'guides': {}
        }
        
        # Critical Issues
        report['critical_issues'] = [
            {
                'issue': 'HTTP Insecure Warning',
                'impact': 'Clients see security warning, immediate trust loss, high bounce rate',
                'solution': 'Implement SSL/HTTPS using Cloudflare + GitHub Pages/Vercel',
                'guide_reference': 'ssl_fix_guide'
            },
            {
                'issue': 'Broken Demo Components',
                'impact': 'Cannot showcase capabilities, prospects leave without understanding value',
                'solution': 'Fix or replace with video/screenshots + CTA',
                'guide_reference': 'demo_fix_guide'
            }
        ]
        
        # High Priority
        report['high_priority'] = [
            {
                'issue': 'Missing Clear CTAs',
                'impact': 'Visitors don\'t know what action to take',
                'solution': 'Add prominent "Request Demo" and "Contact Us" buttons'
            },
            {
                'issue': 'No Lead Capture',
                'impact': 'Losing potential clients who aren\'t ready to contact',
                'solution': 'Add email signup for newsletter/whitepapers'
            },
            {
                'issue': 'Slow Page Load',
                'impact': 'Poor user experience, lower search rankings',
                'solution': 'Optimize images, minify assets, enable compression'
            }
        ]
        
        # Medium Priority
        report['medium_priority'] = [
            {
                'issue': 'Missing SEO Meta Tags',
                'impact': 'Poor search visibility',
                'solution': 'Add title, description, Open Graph tags'
            },
            {
                'issue': 'No Social Proof',
                'impact': 'Lack of trust signals',
                'solution': 'Add client logos, testimonials, case studies'
            },
            {
                'issue': 'Missing Analytics',
                'impact': 'Cannot track visitor behavior',
                'solution': 'Add Google Analytics 4, LinkedIn Insight Tag'
            }
        ]
        
        # Include all guides
        report['guides']['ssl_fix_guide'] = self.generate_ssl_fix_guide()
        report['guides']['demo_fix_guide'] = self.generate_demo_fix_guide()
        report['guides']['seo_optimization_guide'] = self.generate_seo_optimization_guide()
        
        return report
    
    def save_reports(self):
        """Save all repair guides and audit report"""
        os.makedirs(self.config['output_dir'], exist_ok=True)
        
        # Generate full audit
        audit = self.generate_full_audit_report()
        
        # Save JSON report
        audit_path = os.path.join(self.config['output_dir'], 'website_audit_report.json')
        with open(audit_path, 'w') as f:
            json.dump(audit, f, indent=2)
        
        # Save human-readable report
        report_md = self._generate_markdown_report(audit)
        md_path = os.path.join(self.config['output_dir'], 'WEBSITE_FIX_GUIDE.md')
        with open(md_path, 'w') as f:
            f.write(report_md)
        
        # Save SSL fix script
        ssl_script = self._generate_ssl_fix_script()
        ssl_path = os.path.join(self.config['output_dir'], 'fix_ssl.sh')
        with open(ssl_path, 'w') as f:
            f.write(ssl_script)
        os.chmod(ssl_path, 0o755)
        
        print(f"\n{'='*60}")
        print(f"🔧 Kgotla AI Website Repair - Reports Generated")
        print(f"{'='*60}\n")
        print(f"📁 Files created:")
        print(f"   • {audit_path} - Full audit (JSON)")
        print(f"   • {md_path} - Step-by-step fix guide (Markdown)")
        print(f"   • {ssl_path} - SSL fix automation script\n")
        
        print(f"🚨 CRITICAL ISSUES ({len(audit['critical_issues'])}):")
        for issue in audit['critical_issues']:
            print(f"   ❌ {issue['issue']}")
            print(f"      Impact: {issue['impact']}")
        
        print(f"\n⚠️  HIGH PRIORITY ({len(audit['high_priority'])}):")
        for issue in audit['high_priority']:
            print(f"   ⚠️  {issue['issue']}")
        
        print(f"\n✅ Next Steps:")
        print(f"   1. Read WEBSITE_FIX_GUIDE.md")
        print(f"   2. Start with SSL/HTTPS fix (Critical)")
        print(f"   3. Fix or replace broken demos")
        print(f"   4. Implement SEO recommendations")
        print(f"\n{'='*60}\n")
        
        return audit_path, md_path, ssl_path
    
    def _generate_markdown_report(self, audit):
        """Generate human-readable markdown report"""
        md = f"""# Kgotla AI Website Repair Guide
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Domain:** {self.domain}

---

## 🚨 CRITICAL ISSUES (Fix Immediately)

"""
        for issue in audit['critical_issues']:
            md += f"""### {issue['issue']}
**Impact:** {issue['impact']}

**Solution:** {issue['solution']}

---

"""
        
        # Add SSL fix guide
        ssl_guide = audit['guides']['ssl_fix_guide']
        md += f"""## 🔒 SSL/HTTPS Fix Guide
**Priority:** {ssl_guide['priority']}
**Estimated Time:** {ssl_guide['estimated_time']}

"""
        for step in ssl_guide['steps']:
            md += f"""### Step {step['step']}: {step['title']}
**Platform:** {step['platform']}

**Instructions:**
"""
            for instr in step['instructions']:
                md += f"- {instr}\n"
            
            if 'verification' in step:
                md += f"\n**Verification:** {step['verification']}\n"
            
            md += "\n---\n\n"
        
        # Add demo fix guide
        demo_guide = audit['guides']['demo_fix_guide']
        md += f"""## 🎮 Demo Fix Guide
**Priority:** {demo_guide['priority']}
**Estimated Time:** {demo_guide['estimated_time']}

### Common Demo Issues

"""
        for demo_issue in demo_guide['demo_issues']:
            md += f"""#### {demo_issue['issue']}
**Symptoms:**
"""
            for symptom in demo_issue['symptoms']:
                md += f"- {symptom}\n"
            
            md += "\n**Fixes:**\n"
            for fix in demo_issue['fixes']:
                md += f"- {fix}\n"
            
            if 'fallback_solution' in demo_issue:
                md += f"\n**Fallback:** {demo_issue['fallback_solution']}\n"
            
            md += "\n---\n\n"
        
        # Add SEO guide
        seo_guide = audit['guides']['seo_optimization_guide']
        md += f"""## 📈 SEO Optimization Guide
**Priority:** {seo_guide['priority']}

"""
        for rec in seo_guide['recommendations']:
            md += f"""### {rec['category']}

```html
{rec.get('template', rec.get('content', ''))}
```

---

"""
        
        md += """## ✅ Implementation Checklist

- [ ] Fix SSL/HTTPS (Cloudflare configuration)
- [ ] Fix mixed content issues
- [ ] Enable HTTPS on GitHub Pages
- [ ] Fix or replace broken demos
- [ ] Add meta tags to all pages
- [ ] Create sitemap.xml
- [ ] Create robots.txt
- [ ] Add structured data
- [ ] Optimize images
- [ ] Add Google Analytics
- [ ] Test on mobile devices
- [ ] Verify all links work

---

**Need Help?** Contact: mahlo@kgotlaai.co.za
"""
        
        return md
    
    def _generate_ssl_fix_script(self):
        """Generate bash script for SSL fixes"""
        script = """#!/bin/bash
# Kgotla AI SSL Fix Script
# Run this after updating your repository

echo "🔧 Kgotla AI SSL Fix Script"
echo "============================"

# Check if in git repository
if [ ! -d ".git" ]; then
    echo "❌ Not a git repository. Please run from your website root."
    exit 1
fi

echo ""
echo "Step 1: Finding HTTP references..."
echo "-----------------------------------"

# Find and list all HTTP references
echo "Files with http:// references:"
grep -r "http://" . --include="*.html" --include="*.css" --include="*.js" -l 2>/dev/null | head -20

echo ""
echo "Step 2: Replacing HTTP with HTTPS..."
echo "-------------------------------------"

# Replace http:// with https:// in HTML files
find . -name "*.html" -type f -exec sed -i 's/http:\/\//https:\/\//g' {} +
echo "✅ Updated HTML files"

# Replace in CSS files
find . -name "*.css" -type f -exec sed -i 's/http:\/\//https:\/\//g' {} +
echo "✅ Updated CSS files"

# Replace in JS files
find . -name "*.js" -type f -exec sed -i 's/http:\/\//https:\/\//g' {} +
echo "✅ Updated JS files"

echo ""
echo "Step 3: Checking for remaining HTTP references..."
echo "--------------------------------------------------"

remaining=$(grep -r "http://" . --include="*.html" --include="*.css" --include="*.js" -l 2>/dev/null | wc -l)

if [ "$remaining" -eq 0 ]; then
    echo "✅ No HTTP references found!"
else
    echo "⚠️  Found $remaining files with HTTP references:"
    grep -r "http://" . --include="*.html" --include="*.css" --include="*.js" -l 2>/dev/null
fi

echo ""
echo "Step 4: Git status..."
echo "---------------------"
git status --short

echo ""
echo "Next steps:"
echo "1. Review the changes: git diff"
echo "2. Stage changes: git add ."
echo "3. Commit: git commit -m 'Fix: Update all HTTP to HTTPS'"
echo "4. Push: git push origin main"
echo "5. Wait for deployment (2-5 minutes)"
echo "6. Test: https://kgotlaai.co.za"
echo ""
echo "Done! ✅"
"""
        return script

if __name__ == '__main__':
    repair = WebsiteRepair()
    repair.save_reports()
