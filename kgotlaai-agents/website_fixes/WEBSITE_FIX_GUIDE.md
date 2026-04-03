# Kgotla AI Website Repair Guide
**Generated:** 2026-04-04 02:30
**Domain:** kgotlaai.co.za

---

## 🚨 CRITICAL ISSUES (Fix Immediately)

### HTTP Insecure Warning
**Impact:** Clients see security warning, immediate trust loss, high bounce rate

**Solution:** Implement SSL/HTTPS using Cloudflare + GitHub Pages/Vercel

---

### Broken Demo Components
**Impact:** Cannot showcase capabilities, prospects leave without understanding value

**Solution:** Fix or replace with video/screenshots + CTA

---

## 🔒 SSL/HTTPS Fix Guide
**Priority:** CRITICAL
**Estimated Time:** 2-4 hours

### Step 1: Configure Cloudflare SSL/TLS
**Platform:** Cloudflare

**Instructions:**
- Log in to Cloudflare dashboard (dash.cloudflare.com)
- Select your domain: kgotlaai.co.za
- Go to SSL/TLS → Overview
- Set SSL/TLS encryption mode to "Full (strict)"
- Enable "Always Use HTTPS" in Edge Certificates
- Enable "Automatic HTTPS Rewrites"
- Set Minimum TLS Version to 1.2

**Verification:** Visit http://kgotlaai.co.za - should redirect to https://kgotlaai.co.za

---

### Step 2: Fix Mixed Content Issues
**Platform:** GitHub Repository

**Instructions:**
- Clone your website repository: git clone https://github.com/kgotlaai/website.git
- Search for http:// references: grep -r "http://" . --include="*.html" --include="*.css" --include="*.js"
- Replace all http:// with https:// in HTML/CSS/JS files
- Check for protocol-relative URLs (//example.com) and ensure they work
- Update any external resources (fonts, scripts, images) to use HTTPS

**Verification:** Use Chrome DevTools → Security tab to check for mixed content

---

### Step 3: Enable HTTPS on GitHub Pages
**Platform:** GitHub

**Instructions:**
- Go to github.com/kgotlaai/website/settings/pages
- Under "GitHub Pages" section
- Check "Enforce HTTPS" checkbox
- Ensure custom domain is set to kgotlaai.co.za
- Wait 5-10 minutes for DNS propagation

**Verification:** GitHub Pages shows "Your site is published at https://kgotlaai.co.za"

---

### Step 4: Configure Vercel SSL
**Platform:** Vercel

**Instructions:**
- Log in to vercel.com dashboard
- Select your Kgotla AI project
- Go to Settings → Domains
- Verify kgotlaai.co.za is configured
- Enable "HTTPS Only" if available
- Check that SSL certificate is auto-provisioned

**Verification:** Vercel dashboard shows SSL certificate as "Active"

---

### Step 5: Verify DNS Configuration
**Platform:** Host Africa / DNS Provider

**Instructions:**
- Log in to Host Africa control panel
- Check DNS records for kgotlaai.co.za
- Ensure A records point to correct IPs:
-   - For Cloudflare: Use Cloudflare nameservers
-   - For GitHub Pages: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
-   - For Vercel: 76.76.21.21
- Ensure CNAME record for www points to @ or appropriate target
- Check TTL values (recommend 300 for quick changes)

**Verification:** Run: dig kgotlaai.co.za +short - should show correct IPs

---

## 🎮 Demo Fix Guide
**Priority:** HIGH
**Estimated Time:** 3-6 hours

### Common Demo Issues

#### RAG Chatbot Demo Not Working
**Symptoms:**
- Chat interface loads but no responses
- Error messages in console
- API endpoint returning 404/500

**Fixes:**
- Check if backend API is running (IBM watsonx, custom server)
- Verify API endpoint URL in frontend code
- Check API key/environment variables
- Test API independently using curl or Postman
- Add error handling and user-friendly error messages
- Consider using a mock/demo mode for static sites

**Fallback:** Replace live demo with recorded video/screenshots until backend is fixed

---

#### Demo Links Return 404
**Symptoms:**
- Clicking demo button shows 404 page
- Demo page missing from build

**Fixes:**
- Check if demo HTML/JS files exist in repository
- Verify file paths in navigation links
- Check build process includes demo files
- Ensure case sensitivity matches (Demo.html vs demo.html)

---

#### Interactive Elements Not Responding
**Symptoms:**
- Buttons don't work
- Forms don't submit
- Animations broken

**Fixes:**
- Check browser console for JavaScript errors
- Verify jQuery/other libraries loaded correctly
- Check for JavaScript file loading over HTTP (mixed content)
- Test in multiple browsers (Chrome, Firefox, Safari)
- Ensure event listeners attached after DOM loads

---

#### Slow Loading Demos
**Symptoms:**
- Demo takes >5 seconds to load
- Images/assets loading slowly

**Fixes:**
- Optimize images (compress, use WebP format)
- Lazy load demo components
- Minify CSS/JS files
- Use CDN for static assets
- Add loading indicators

---

## 📈 SEO Optimization Guide
**Priority:** MEDIUM

### Meta Tags

```html
<!-- Add to <head> section of every page -->
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

```

---

### Structured Data (Schema.org)

```html
<script type="application/ld+json">
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

```

---

### robots.txt

```html
User-agent: *
Allow: /

Sitemap: https://kgotlaai.co.za/sitemap.xml

# Disallow admin areas if any
Disallow: /admin/
Disallow: /private/

```

---

### sitemap.xml

```html
<?xml version="1.0" encoding="UTF-8"?>
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

```

---

## ✅ Implementation Checklist

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
