# Sofía Abud — Portfolio

Professional portfolio website for **Sofía Abud**, a Mexican cinematographer, photographer, and composer based in Toronto. The site showcases her work across multiple disciplines, featuring a minimalist, cinematic design with dynamic elements.

🔗 **Live Site:** [sofiaabud.com](https://sofiaabud.com)

## 🎨 Design & Aesthetics

- **Typography:** Features the elegant **Gambetta** serif font for a premium, editorial feel.
- **Dynamic Colors:** An accent color is randomly selected on each page load, applying a unique personality to navigation and titles.
- **Interactive Experience:** 
  - Custom hover effects on the cinematography grid.
  - Smooth scroll-reveal animations using Intersection Observer.
  - High-performance Lightbox/Zoom system for all project stills.

## 🚀 Technical Stack

- **Frontend:** Semantic HTML5, Vanilla JavaScript (ES6+), and Modern CSS.
- **Image System:** Dual-resolution WebP system for high performance and low data usage (Standard vs. High-Res variants).
- **Responsive Design:** Fully optimized for mobile, tablet, and desktop viewing.

## 📁 Project Structure

```text
├── assets/
│   ├── font/           # Web fonts (Gambetta)
│   ├── img/            # Optimized images (std/high variants)
│   └── music/          # Audio portfolio assets
├── css/                # Modular stylesheets (grid, layout, projects, etc.)
├── js/                 # Unified main.js for site interactivity
├── projects/           # Cinematography individual project pages
├── index.html          # Cinematography Home
├── photography.html    # Photography Gallery
├── music.html          # Music & Sound Design
└── about.html          # Artist Bio & Contact
```

## Image preparation — Chicomecoatl and The Barn

- Matching filenames live under `assets/img/{std,high}/photography/chicomecoatl/CH1.webp`–`CH7.webp` and `assets/img/{std,high}/cinematography/TB/TB1.webp`–`TB17.webp`. Image 1 is each project's supplied cover.
- `high` preserves the original pixel dimensions, with WebP quality 95. `std` generally uses WebP quality 82; CH2 uses quality 95, matching the documented `high` setting, and is resized directly from `high`. Standard images use approximately half the original width and height, with rounding to whole pixels where needed. Both variants retain embedded colour profiles when present.
- The Barn uses 4096 × 2160 for `high` and 2048 × 1080 for `std`. Chicomecoatl has mixed original dimensions; CH1 (2227 × 1782) retains its dimensions in `std`. CH2 uses 2783 × 3411 for `high` and 1392 × 1706 for `std`, approximately half the width and height with rounding to whole pixels and no cropping.
- WebP conversion preserves the full image framing without cropping, stretching or enlarging. The galleries show natural aspect ratios. Chicomecoatl's photography card uses a centred 4:3 crop to trim a little from the top and bottom; both new project cards use the site's standard hover zoom.
- The Barn's gallery order is dungeon and other interiors (TB1–TB6, TB16–TB17), blue control room (TB7–TB9), then greens and exteriors (TB10–TB15), with no empty cells between groups. The cinematography card shows one still from each group (TB1, TB7, TB15).

## ✉️ Contact

- **Website:** [sofiaabud.com](https://sofiaabud.com)
- **Email:** sofiaabud@gmail.com
- **Instagram:** [@sof_abud](https://www.instagram.com/sof_abud/)

---
© 2026 Sofía Abud. Built with 🤍 and performance in mind.
