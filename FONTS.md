# Typography System & Font Licensing

This developer portfolio utilizes a carefully engineered typographic hierarchy designed to render with zero latency, zero layout shift, and complete cross-platform fidelity inside GitHub's sanitized SVG environment.

---

## 1. Typographic Hierarchy

### A. Primary Headline & Brand Serif
- **Primary Serif:** `Cinzel` & `Playfair Display`
- **Fallback Chain:** `'Cinzel', 'Playfair Display', 'Cormorant Garamond', 'Georgia', 'Times New Roman', serif`
- **Application:** Display name (*Abu Sufiyan*), monogram badge (*AS*), and section titles.
- **Characteristics:** Elegant neoclassical high-contrast serifs conveying architectural precision and craftsmanship.

### B. Technical & Telemetry Monospace
- **Primary Monospace:** `JetBrains Mono` & `Fira Code`
- **Fallback Chain:** `'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, 'Courier New', monospace`
- **Application:** Terminal commands, metric KPI figures, status badges, tech stack pills, and dates.
- **Characteristics:** Geometric tabular figures optimized for readability in technical displays.

### C. UI & Explanatory Sans-Serif
- **Primary Sans:** `Plus Jakarta Sans` & `Inter`
- **Fallback Chain:** `'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Application:** Subtitles, project descriptions, feature bullets, and category captions.
- **Characteristics:** Neutral, modern grotesque sans-serif providing high legibility on high-DPI displays.

---

## 2. GitHub SVG Compatibility & Font Subsetting

GitHub displays README images through a secure caching proxy (`camo.githubusercontent.com`). To maintain security, the proxy:
1. Strips external CSS imports (`@import url(...)`).
2. Blocks external font file fetching via Content Security Policy (CSP).

To guarantee that your cards look crisp on macOS, Windows, Linux, Android, and iOS without depending on external web fonts, the system uses **native font-family chains** that gracefully map to installed system serifs (`Georgia`, `Playfair Display`, `Palatino`) and monospaces (`SF Mono`, `Consolas`, `Courier New`).

### Optional: Font Subsetting with `pyftsubset`
If you wish to embed an ultra-light WOFF2 font directly as a base64 Data URI inside SVG `<style>` blocks:

```bash
# 1. Install fonttools
pip install fonttools brotli

# 2. Subset glyphs for Abu Sufiyan name and numerals
pyftsubset Cinzel-Bold.ttf \
  --text="ABU SUFIYAN0123456789+-/*:.#[]_ " \
  --flavor=woff2 \
  --output-file=Cinzel-Subset.woff2

# 3. Convert to base64 Data URI
base64 -w 0 Cinzel-Subset.woff2 > Cinzel-Subset.b64
```

---

## 3. Font Licenses

All recommended web fonts are distributed under open-source licenses:

| Font Family | Designer / Foundry | License | Permitted Uses |
| :--- | :--- | :--- | :--- |
| **Cinzel** | Natanael Gama | SIL Open Font License 1.1 | Personal & Commercial Web/SVG |
| **Playfair Display** | Claus Eggers Sørensen | SIL Open Font License 1.1 | Personal & Commercial Web/SVG |
| **Plus Jakarta Sans** | Tokotype | SIL Open Font License 1.1 | Personal & Commercial Web/SVG |
| **JetBrains Mono** | JetBrains | SIL Open Font License 1.1 | Personal & Commercial Web/SVG |
| **Inter** | Rasmus Andersson | SIL Open Font License 1.1 | Personal & Commercial Web/SVG |

The SIL Open Font License allows free use, bundling, and embedding in software and SVG documents.
