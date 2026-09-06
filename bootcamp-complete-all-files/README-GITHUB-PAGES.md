# Deploying to GitHub Pages

This interactive bootcamp guide can be hosted on GitHub Pages for free!

## Quick Setup

### 1. Create a GitHub Repository

```bash
# Go to github.com/srimaan/neuron-guide (or similar)
# Create a new repository called "bootcamp-guide" (or your preferred name)
```

### 2. Clone the Repository

```bash
git clone https://github.com/srimaan/bootcamp-guide.git
cd bootcamp-guide
```

### 3. Add All HTML Files

Copy all the HTML files from this output folder into your repository:

```bash
# From /mnt/user-data/outputs/
# Copy:
# - index.html
# - 01-prompt-engineering.html
# - 02-agent-frameworks.html
# - 05-eight-patterns.html
# - (and all other chapter files)
```

### 4. Create `.gitignore` (Optional)

```bash
cat > .gitignore << 'EOF'
*.py
*.md
*.docx
.DS_Store
EOF
```

### 5. Commit and Push

```bash
git add .
git commit -m "Add Production AI Architect Bootcamp chapters"
git push origin main
```

### 6. Enable GitHub Pages

1. Go to Repository Settings
2. Scroll to "GitHub Pages" section
3. Select "main" branch as source
4. Save

### 7. Access Your Site

Your bootcamp will be available at:
```
https://srimaan.github.io/bootcamp-guide/
```

(Replace `srimaan` with your GitHub username and `bootcamp-guide` with your repo name)

---

## File Structure

Recommended organization:

```
bootcamp-guide/
├── index.html                    (Landing page)
├── 01-prompt-engineering.html    (Chapter 1)
├── 02-agent-frameworks.html      (Chapter 2)
├── 05-eight-patterns.html        (Chapter 5)
├── 07-v1-simple-mvp.html         (Chapter 7)
├── ... (all other chapters)
└── README.md                     (Project overview)
```

---

## Customization

### Change Styling

Edit the `<style>` section in any HTML file to customize colors:

```html
<style>
    body {
        background: #f5f5f5;  /* Change background */
        color: #333;          /* Change text color */
    }
    h1 {
        color: #667eea;       /* Change heading color */
    }
</style>
```

### Add More Chapters

Use `index.html` as a template:

```html
<div class="chapter-card">
    <a href="03-your-chapter.html">
        <div class="chapter-num">Chapter 3</div>
        <div class="chapter-title">Your Chapter Title</div>
        <div class="chapter-desc">Description of what this chapter covers.</div>
    </a>
</div>
```

### Update Navigation

Each chapter has navigation buttons. Update links as needed:

```html
<div class="nav-buttons">
    <a href="index.html" class="btn btn-secondary">← Back</a>
    <a href="next-chapter.html" class="btn btn-primary">Next →</a>
</div>
```

---

## Domain (Optional)

To use a custom domain:

1. Go to Domain Registrar (GoDaddy, Namecheap, etc.)
2. Add GitHub's nameservers
3. In GitHub Pages settings, add your custom domain
4. Create `CNAME` file in repo with your domain name

---

## Maintenance

### Update Chapters

Simply edit the HTML files and push:

```bash
git add chapter-file.html
git commit -m "Update chapter content"
git push origin main
```

### Add New Chapters

1. Create new HTML file (e.g., `15-mcp-integration.html`)
2. Add to `index.html` chapter list
3. Push to GitHub

---

## Tips

✅ Keep index.html updated with all chapters
✅ Test locally before pushing: `python -m http.server`
✅ Use consistent styling across all chapters
✅ Include code examples for clarity
✅ Link between chapters for easy navigation
✅ Consider creating a sitemap for SEO

---

## Example: Local Testing

Before pushing to GitHub, test locally:

```bash
cd /mnt/user-data/outputs/
python -m http.server 8000
```

Then visit: `http://localhost:8000/index.html`

---

## File List

All files ready to deploy:

```
✅ index.html
✅ 01-prompt-engineering.html
✅ 02-agent-frameworks.html
✅ 05-eight-patterns.html
✅ 07-v1-simple-mvp.html
✅ 11-v5-production.html
✅ 12-error-handling.html
✅ 13-testing-qa.html
✅ 14-monitoring.html
... (add more as created)
```

---

## Next Steps

1. Create GitHub repo
2. Clone locally
3. Copy HTML files
4. Push to GitHub
5. Enable GitHub Pages
6. Share your bootcamp guide!

**Your bootcamp is now live and accessible globally!** 🚀

