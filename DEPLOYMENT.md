# Deployment Guide: Getting Your Site Live

## Step 1: Push to GitHub

```bash
cd personal-website
git init
git add .
git commit -m "Initial commit: personal academic website"

# Create a new repo on GitHub (don't initialize with README)
# Then run:
git remote add origin https://github.com/YOUR-USERNAME/personal-website.git
git branch -M main
git push -u origin main
```

## Step 2: Enable GitHub Pages

1. Go to your repo on GitHub
2. Click **Settings** → **Pages** (in left sidebar)
3. Under "Source":
   - Branch: `main`
   - Folder: `/ (root)`
4. Click **Save**
5. Wait 2-3 minutes, your site will be live at `https://YOUR-USERNAME.github.io/personal-website/`

## Step 3: Configure Your Namecheap Domain

### In Namecheap Dashboard:

1. Go to **Domain List** → Click **Manage** on `sar.ath`
2. Click **Advanced DNS** tab
3. **Delete** any existing A Records or CNAME Records for `@` and `www`
4. **Add these records:**

```
Type: A Record
Host: @
Value: 185.199.108.153
TTL: Automatic

Type: A Record
Host: @
Value: 185.199.109.153
TTL: Automatic

Type: A Record
Host: @
Value: 185.199.110.153
TTL: Automatic

Type: A Record
Host: @
Value: 185.199.111.153
TTL: Automatic

Type: CNAME Record
Host: www
Value: YOUR-USERNAME.github.io.
TTL: Automatic
```

**IMPORTANT:** Replace `YOUR-USERNAME` with your actual GitHub username in the CNAME record.

5. Click **Save All Changes**

## Step 4: Configure Custom Domain in GitHub

1. Back in your repo on GitHub
2. Go to **Settings** → **Pages**
3. Under "Custom domain", enter: `sar.ath`
4. Click **Save**
5. Wait a few minutes for DNS check
6. Check **Enforce HTTPS** (will appear after DNS propagates)

## Step 5: Verify It Works

DNS propagation takes 10-60 minutes. Check status:

```bash
# Check if DNS is propagating
dig sar.ath

# You should see the GitHub Pages IP addresses
```

Visit your site:
- `http://sar.ath` (will redirect to https after HTTPS is enforced)
- `https://www.sar.ath`

## Troubleshooting

### "Domain not yet configured" error
- Wait 15-30 minutes for DNS propagation
- Clear browser cache
- Try incognito/private mode

### HTTPS not working
- Takes up to 24 hours for GitHub to provision SSL certificate
- Make sure DNS has fully propagated first

### 404 error
- Check that `index.html` is in the root directory of your repo
- Verify GitHub Pages is enabled and pointing to `main` branch

## Updating Your Site

Just push changes:

```bash
# Make changes to your files
git add .
git commit -m "Updated blog post"
git push

# Changes appear on sar.ath in 1-2 minutes
```

## Adding New Blog Posts

1. Create new HTML file: `blog/posts/your-new-post.html`
2. Copy the template from `blog/posts/ml-platform-adrs.html`
3. Edit content
4. Update `blog/index.html` to add the post to the list
5. Commit and push

```bash
git add blog/
git commit -m "New post: Your Post Title"
git push
```

## File Structure Quick Reference

```
personal-website/
├── index.html              # Homepage - edit intro, links, recent work
├── blog/
│   ├── index.html         # Blog listing - add new posts here
│   └── posts/
│       └── *.html         # Individual blog posts
├── research/
│   └── publications.html  # Add publications, projects, talks
├── work/
│   └── experience.html    # Update work experience, skills
└── assets/
    ├── css/style.css      # Styling (change colors, fonts, etc.)
    └── cv.pdf            # Upload your PDF resume here
```

## Next Steps

1. Replace placeholder content with your actual info
2. Update GitHub/LinkedIn URLs in `index.html`
3. Add your real CV as `assets/cv.pdf`
4. Write your first real blog post
5. Add your actual publications and projects

Your site is now live at **sar.ath** 🎉
