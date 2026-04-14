# Sarath's Personal Academic Website

Professional portfolio site for PhD applications, publications, and technical blog.

## Quick Start

```bash
# 1. Clone this repo
git clone <your-repo-url>
cd personal-website

# 2. Install dependencies (if using Hugo - recommended)
# Download Hugo from https://github.com/gohugoio/hugo/releases

# 3. Run locally
hugo server -D  # or python -m http.server 8000 for basic HTML

# 4. Deploy
git push origin main  # Auto-deploys to GitHub Pages
```

## Structure

```
personal-website/
├── index.html              # Homepage with intro
├── blog/                   # Blog posts (markdown → HTML)
│   ├── index.html         # Blog listing
│   └── posts/             # Individual posts
├── research/               # Publications & research
│   ├── publications.html  # Publication list
│   └── projects.html      # Research projects
├── work/                   # Professional experience
│   └── experience.html    # Resume/CV content
├── assets/
│   ├── css/
│   ├── js/
│   └── papers/            # PDF uploads
└── README.md
```

## Adding Content

### New Blog Post
1. Create `blog/posts/your-post-name.html`
2. Add to `blog/index.html` listing
3. Commit and push

### Update Publications
1. Edit `research/publications.html`
2. Add PDF to `assets/papers/`
3. Commit and push

## Domain Setup (Namecheap)

**DNS Records to add in Namecheap:**

```
Type: A Record
Host: @
Value: 185.199.108.153

Type: A Record
Host: @
Value: 185.199.109.153

Type: A Record
Host: @
Value: 185.199.110.153

Type: A Record
Host: @
Value: 185.199.111.153

Type: CNAME
Host: www
Value: <your-github-username>.github.io
```

**In GitHub repo:**
- Settings → Pages → Custom domain: `sar.ath`
- Check "Enforce HTTPS"

## Deployment

### GitHub Pages Setup
1. Push code to GitHub
2. Settings → Pages
3. Source: Deploy from branch `main`
4. Root directory: `/`
5. Add custom domain: `sar.ath`

## Maintenance

- **Blog post**: Just add a new HTML file, update index
- **Publication**: Edit publications.html, add PDF
- **No database needed** - Everything is static files
- **Fast**: Loads instantly for recruiters/professors
- **SEO friendly**: Clean URLs, proper meta tags

## Future Additions

- `/teaching/` - TA work, tutorials
- `/talks/` - Conference presentations
- `/cv/` - Downloadable CV
- `/contact/` - Contact form (via Formspree)
