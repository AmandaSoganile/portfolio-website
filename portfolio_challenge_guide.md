# Ship Your Portfolio to the Cloud

**A hands-on challenge using Claude Code, AWS, and GitHub — Examples & Inspiration Guide**

---

## The Brief

Transform your portfolio and about-me into a live, interactive, API-first portfolio website running on AWS, fully automated, and fully version-controlled. By the end, someone should be able to type a URL and see you.

| Piece | Requirement |
|-------|-------------|
| Hosting | AWS Lambda (Function URLs); S3 optional for assets |
| Version Control | GitHub repo with `dev` and `prod` branches |
| CI/CD | Push to `prod` auto-deploys to AWS via GitHub Actions |
| Interactivity | At least one interactive feature (your choice) |
| Architecture | API-first: frontend talks to a backend endpoint |

---

## 1 — Who You Are (the About Me Content)

Don't just list your resume. Make it memorable. Think about what makes you interesting at a dinner table, not just in a job interview.

- A timeline of your journey told as a story, not a bullet list
- A "things I nerd out about" section that shows personality
- A "currently learning" ticker that proves you are always growing
- A fun-facts API endpoint that returns a random fact about you every time it's hit
- A short personal mission statement or a quote you live by
- Links to side projects, blog posts, or talks that reflect who you are beyond work

---

## 2 — Interactive Feature Ideas

This is where you differentiate yourself. Pick at least one, but dream big.

- **Visitor counter with a twist** — Instead of just a number, show a map dot for each visitor's region, or translate the count into something fun: "You're visitor 42 — the answer to everything."
- **Personality-driven theme toggle** — Go beyond light/dark. Try "coffee mode," "night owl mode," or "presentation mode" that each reflect your style.
- **Working contact form** — Lambda receives the POST, sends you an email or a notification. End-to-end proof you can wire things together.
- **"What I'm into" widget** — Pull from a real source: what you're listening to, reading, watching, or playing right now.
- **Mini quiz** — "How well do you know me?" Score visitors and store results. A great conversation starter.
- **Live project feed** — Fetch your latest GitHub commits or repos and display them dynamically.

---

## 3 — The `/meta` or `/version` Endpoint

This is your proof of engineering rigor. It's also your calling card to any engineer who inspects your work — make it clean and informative.

At minimum, return:

- Version number (semver)
- Deploy timestamp (ISO 8601)
- Git commit SHA

> **Tip:** Stamp this into your build at deploy time so it's always accurate and never manually updated.

---

## 4 — API Design (Think Before You Build)

Before touching the frontend, sketch out what your Lambda returns. The shape of your API is your architecture decision. JSON responses that your frontend fetches and renders means you're building a real decoupled system, not just hosting a static HTML file.

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/meta` | Version, deploy timestamp, commit SHA |
| GET | `/about` | Your bio as structured JSON |
| GET | `/projects` | List of your work with descriptions and links |
| POST | `/contact` | Accepts name, email, and message |
| GET | `/fun-fact` | Returns a random tidbit about you |

---

## 5 — Frontend Personality

Your site doesn't need to look like every other portfolio template. The constraint is that it talks to your API; the design is entirely yours.

- **Minimal & typographic** — Let your words do the work. Big type, lots of whitespace.
- **Bold & colorful** — Gradients, illustrations, animated transitions.
- **Retro terminal** — Green-on-black, monospace font, blinking cursor.
- **Something unexpected** — A newspaper layout, a video-game HUD, a comic strip.

Even small touches matter: a custom favicon, a loading animation, a scroll interaction, or an Easter egg hidden in the console logs.

---

## 6 — CI/CD and Branch Strategy

When you push to your `prod` branch and watch GitHub Actions deploy it automatically to AWS, that's a real "it's alive" moment.

- Add a lint or test step before deploy so you never ship broken code
- Include the git SHA in your `/meta` response so you can always trace what's live
- Set up a notification (e.g., email or Discord) when a deploy succeeds or fails
- Consider separate environments: `dev` deploys to a test Lambda, `prod` deploys to production

---

## 7 — The "Wow Factor" Extras

If you want to go further and really impress, consider these additions:

- An S3 bucket serving static assets with proper cache headers
- A dark/light mode that remembers preference via a cookie or localStorage
- An analytics endpoint that tracks page views in DynamoDB
- A "view source" button that links directly to your GitHub repo
- Lighthouse performance score above 90
- Open Graph meta tags so your site looks great when shared on social media

---

## 8 — Getting Started Checklist

1. **Fire up Claude Code** — Install it, open a fresh project directory, and run `claude`. It can write files, run commands, and iterate in real time.
2. **Create the GitHub repo via Claude Code** — The GitHub CLI (`gh`) can create repos, branches, protection rules, and Actions workflows.
3. **Store your secrets safely** — AWS credentials need to live somewhere secure. GitHub lets you store sensitive config in repository Secrets.
4. **Design the API first** — Decide what your Lambda returns: JSON, HTML, or both. Your `/meta` route is the perfect starting point.
5. **Provision AWS from Claude Code** — Set your credentials in the environment. Claude Code can scaffold Lambda, write IAM policies, and build deployment scripts.

---

This project is a chance to show not just that you can build and deploy something, but that you have taste, personality, and engineering discipline. The best portfolios make someone smile, then make them want to look under the hood.
