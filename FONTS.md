# Monospace Font Options for Your Site

## Current Setup: JetBrains Mono
**Already configured** - Modern, clean, excellent for technical content.

## Quick Font Swaps

Just replace the `@import` line and `font-family` in `assets/css/style.css`:

### Option 1: JetBrains Mono (Current - Recommended)
```css
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');

body {
    font-family: 'JetBrains Mono', monospace;
}
```
**Vibe:** Modern, technical, clean. Created by JetBrains specifically for code.
**Best for:** Systems engineers, infrastructure folks, developers

---

### Option 2: IBM Plex Mono
```css
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&display=swap');

body {
    font-family: 'IBM Plex Mono', monospace;
}
```
**Vibe:** Corporate-tech, slightly more formal
**Best for:** Enterprise/professional feel

---

### Option 3: Roboto Mono
```css
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;600;700&display=swap');

body {
    font-family: 'Roboto Mono', monospace;
}
```
**Vibe:** Google Material Design, very readable
**Best for:** Clean, minimalist aesthetic

---

### Option 4: Source Code Pro
```css
@import url('https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@400;500;600;700;900&display=swap');

body {
    font-family: 'Source Code Pro', monospace;
}
```
**Vibe:** Adobe-designed, compact, professional
**Best for:** Dense technical content

---

### Option 5: Fira Code (Has ligatures!)
```css
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&display=swap');

body {
    font-family: 'Fira Code', monospace;
}
```
**Vibe:** Modern, includes programming ligatures (→, >=, etc.)
**Best for:** Showing off technical chops

---

### Option 6: Space Mono
```css
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');

body {
    font-family: 'Space Mono', monospace;
}
```
**Vibe:** Quirky, distinctive, retro-futuristic
**Best for:** Standing out, personality

---

### Option 7: System Monospace (No import needed)
```css
/* Remove the @import line */

body {
    font-family: 'SF Mono', Menlo, Monaco, Consolas, 'Courier New', monospace;
}
```
**Vibe:** Uses system fonts - SF Mono on Mac, Consolas on Windows
**Best for:** Fast loading, native feel

---

## My Recommendation for You

**Stick with JetBrains Mono** (already set up). Here's why:

1. **Systems engineer credibility** - It's what developers actually use
2. **Excellent readability** - Designed for long-form reading, not just code
3. **Modern but professional** - Not trendy, not boring
4. **Complete weight range** - From light to extra bold
5. **Free & open source** - No licensing issues

Perfect for someone positioning for NVIDIA/Meta-level infrastructure roles.

---

## How to Change

1. Open `assets/css/style.css`
2. Replace the `@import` line at the top
3. Replace the `font-family` in the `body` section
4. Save, commit, push

```bash
git add assets/css/style.css
git commit -m "Updated to [Font Name]"
git push
```

Changes are live in ~1 minute.

---

## Mix & Match Option

Want mono for headers but something else for body text?

```css
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@700;800&family=Inter:wght@400;500&display=swap');

body {
    font-family: 'Inter', sans-serif;  /* Clean reading */
}

h1, h2, h3, h4, h5, h6, .nav-brand {
    font-family: 'JetBrains Mono', monospace;  /* Technical headers */
}
```

This gives you mono personality in headers while keeping body text easier to read for long-form content.
