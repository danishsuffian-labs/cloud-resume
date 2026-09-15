# Repository guidance

## Purpose and scope

Build Danish Suffian’s portfolio across software engineering and cloud engineering. Prefer simple, readable solutions and architecture decisions the owner can explain in an interview.

The active scope is **Phase 1: the local static frontend**. `PLAN.md` records progress and future work; an unchecked roadmap item is not authorization to implement it. Do not create AWS resources, Terraform, CI/CD workflows, backend services, or analytics unless the user requests that scope. Follow the user's latest explicit direction when the scope changes.

## Before making changes

- Read `README.md`, `PLAN.md`, and `docs/architecture.md`, then inspect the relevant files.
- Check Git status when a repository is available. Preserve unrelated user work and avoid broad rewrites.
- Keep changes within `cloud-resume/` unless the task explicitly includes another directory.
- Make routine, reversible implementation decisions within the requested scope; ask only when a missing decision materially affects the outcome.

## Current implementation

- `frontend/index.html`: semantic markup, portfolio content, and links.
- `frontend/styles.css`: shared design tokens, component classes, responsive behavior, and print styles.
- `frontend/favicon.svg`: two-line “Danish Suffian” SVG wordmark.
- `frontend/assets/images/danish.webp`: supplied portrait, presented in a circular frame beside the About heading.
- `backend/`, `infrastructure/`, and `.github/workflows/`: reserved directories only.
- No package manager, build step, JavaScript, framework, or automated test suite currently exists.

Keep HTML/CSS as the default. Add dependencies or abstractions only to solve a concrete requirement, explaining the tradeoff. React is under consideration, not an approved migration. Small interactions may use plain JavaScript when requested; keep configuration separate from behavior and never put credentials in frontend code.

## Content and design

- Communicate both software engineering and cloud engineering clearly.
- Preserve the clean, warm neutral design, restrained orange accents, and readable typography.
- Use “Danish” or “Danish Suffian” for visible branding. Avoid the `ds` initials mark; the owner identified an unwanted local association. The current favicon uses the full name on two lines. Preserve the owner-approved circular portrait and About layout.
- Use only supplied professional facts. Do not invent employers, dates, certifications, metrics, project outcomes, or links.
- Distinguish implemented capabilities from planned work. Preserve honest project status labels.
- Maintain semantic headings, meaningful link text, keyboard access, visible focus, reduced-motion support, and mobile layouts.
- Prefer native HTML controls and local assets. Avoid unnecessary animation, remote fonts, trackers, or a simulated contact form.

## Validation

Run locally from the project root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory frontend
```

Choose checks proportional to the change. For frontend edits, verify affected markup, fragment links, asset paths, and relevant layout behavior. Where a browser is available, inspect 320px, 375px, 768px, and desktop widths, keyboard navigation, and 200% zoom. Check disclosure controls, reduced motion, and print layout when those areas change.

Do not add a test framework for a simple copy or styling change. Do not report browser, accessibility, or live deployment checks as passed unless they actually ran. Document unavailable checks and remaining issues.

## Documentation and handoff

- Keep setup and publishing instructions in `README.md`, work status and verification evidence in `PLAN.md`, deferred content ideas in `FUTURE.md`, and architecture rationale in `docs/architecture.md`.
- Keep these project documents in version control. Publish only the contents of `frontend/` to S3; `.gitignore` does not filter uploads.
- GitHub pushes do not deploy the site until a deployment workflow is implemented.
- Update relevant documentation when behavior, structure, or decisions change.
- Mark a checklist item complete only with supporting evidence; distinguish implementation from verification.
- Explain significant changes, validation performed, and unresolved limitations in the handoff.
- Never commit secrets, credentials, state files, or personal information not supplied for publication.
