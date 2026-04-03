# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal portfolio website for Amanda Songanile. Currently a single-file static site (`index.html`). Flask backend is planned for a later phase.

## Current Stack

- Pure HTML / CSS / JS — no build step, no npm, no bundler
- Google Fonts: Playfair Display (headings) + DM Sans (body), loaded via CDN
- All state is `localStorage` only (likes, comments, theme preference)
- To preview: open `index.html` directly in a browser

## Architecture

Everything lives in `index.html` in three clearly labelled blocks:

| Block | What's in it |
|-------|-------------|
| `<style>` | All CSS — theme variables, layout, animations, components |
| `<body>` | Semantic sections in page order |
| `<script>` | All JS — cursor, progress bar, theme switcher, typewriter, scroll reveal, fun-fact interactions, contact form, toast |

### Theming

Three themes controlled by `data-theme` on `<html>`: `default`, `pink`, `dark`.
All colour values are CSS custom properties on `:root` and overridden per theme selector.
Saved to `localStorage` under key `portfolio-theme`.

### Sections (in DOM order)

1. **Hero** — name, typewriter role, CTA buttons, floating image frame, animated blobs
2. **Fun Fact Strip 1** — two `ff-card` cards (ff1, ff2) with like + comment
3. **About** — two-column grid: image placeholder left, bio + tags right
4. **Get to Know Me** — 6 flip cards, toggled by click
5. **Fun Fact Strip 2** — one card (ff3)
6. **Projects** — 3-column auto-fit grid of `proj-card` components
7. **Fun Fact Strip 3** — two cards (ff4, ff5)
8. **Contact** — centred form + social icon row

### Fun Fact cards

Each card has a unique `id` (`ff1`–`ff5`). Likes and comments are stored in `localStorage` as:
- `liked-{id}` — `'true'` / `'false'`
- `like-count-{id}` — integer string
- `comments-{id}` — JSON array of `{ name, text }`

### Scroll reveal

Elements with class `reveal`, `reveal-l`, or `reveal-r` start hidden and animate in via `IntersectionObserver`. Delay classes `d1`–`d6` stagger siblings.

## Adding Photos

Two placeholders exist for Amanda's photo:

- **Hero frame** (`#hero .hero-img-placeholder`) — replace the `<div>` with `<img src="amanda-cutout.png" alt="Amanda">`. Use a PNG with transparent background.
- **About image** (`#about .about-img-wrap`) — add `<img src="amanda-about.jpg" ...>` inside `.about-img-wrap` with `style="width:100%;height:100%;object-fit:cover;"`.

## Planned: Flask Phase

When migrating to Flask:
- `index.html` moves to `templates/index.html`
- Fun fact comments/likes will POST to Flask endpoints instead of writing to `localStorage`
- Contact form will POST to a Flask route that forwards to Slack via webhook
- Static assets (images, CSS if extracted) go in `static/`

## Content to Replace

All placeholder text in `index.html` is marked with comments or obvious filler. Key spots:
- Typewriter roles array in `<script>` — update with real roles
- About section paragraphs — replace with Amanda's real bio
- Flip card answers — replace with real answers
- Fun fact card text — replace with real facts
- Project cards — add real projects and descriptions
- Social links — replace `href="#"` with real URLs
