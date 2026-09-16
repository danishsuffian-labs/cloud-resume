# Repository guidance

## Purpose and scope

Build Danish Suffian’s portfolio across software engineering and cloud engineering. Prefer simple, readable solutions and architecture decisions the owner can explain in an interview.

The active scope is **the static frontend plus user-guided GitHub Actions/OIDC learning for S3 deployment**. The owner wants to understand and author the YAML; guide them through it rather than completing the workflow unasked. `PLAN.md` records progress and future work; an unchecked roadmap item is not authorization to implement it. Do not create AWS resources, Terraform, CI/CD workflows, backend services, or analytics unless the user requests that scope. Follow the user's latest explicit direction when the scope changes.

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
- `.github/workflows/deploy-s3.yaml`: **Deploy Portfolio**, triggered by pushes to `main`; checks out code, assumes the configured AWS role using OIDC, and checks caller identity. It then syncs `frontend/` to `danishsuffian-resume-s3` without deletion and requests `/*` invalidation on CloudFront distribution `E2MC444L6LW7DX`. The owner confirmed success; the workflow does not wait for invalidation completion.
- Hosting: owner-confirmed HTTPS and Route 53 domain `danishsuffian.cloud`, CloudFront, and S3 origin access through OAC.
- `backend/` and `infrastructure/`: reserved directories only.
- No package manager, build step, JavaScript, framework, or automated test suite currently exists.

Keep HTML/CSS as the default. Add dependencies or abstractions only to solve a concrete requirement, explaining the tradeoff. React is under consideration, not an approved migration. Small interactions may use plain JavaScript when requested; keep configuration separate from behavior and never put credentials in frontend code.

## Content and design

- Communicate both software engineering and cloud engineering clearly.
- Preserve the clean, warm neutral design, restrained orange accents, and readable typography.
- Use “Danish” or “Danish Suffian” for visible branding. Avoid the `ds` initials mark; the owner identified an unwanted local association. The current favicon uses the full name on two lines. Preserve the owner-approved circular portrait and About layout.
- Use only supplied professional facts. Do not invent employers, dates, certifications, metrics, project outcomes, or links.
- Distinguish implemented capabilities from planned work. Use “Done” and “Planned” in the public project roadmap, with readable text labels alongside status colors. Keep verification tasks in `PLAN.md`.
- Maintain semantic headings, meaningful link text, keyboard access, visible focus, reduced-motion support, and mobile layouts.
- Prefer native HTML controls and local assets. Avoid unnecessary animation, remote fonts, trackers, or a simulated contact form.

## Deployment authentication

Use GitHub OIDC and a dedicated IAM role in the production account for deployment. Keep human access through IAM Identity Center separate. Do not add long-lived AWS keys to the repository or workflow. GitHub’s identity token is exchanged through AWS STS for temporary AWS credentials; it is not sent directly to S3. Do not mark OIDC or deployment verified without a successful run. The identity check verifies authentication, not S3 upload permissions. Retain checkout and authentication in the deployment job, with invalidation after the S3 upload.

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
- Pushes to `main` trigger real S3 uploads and CloudFront invalidations. Treat workflow and frontend changes accordingly; do not push or deploy unless authorized.
- Distinguish owner-confirmed deployment evidence from independently executed browser or AWS checks.
- Update relevant documentation when behavior, structure, or decisions change.
- Mark a checklist item complete only with supporting evidence; distinguish implementation from verification.
- Explain significant changes, validation performed, and unresolved limitations in the handoff.
- Never commit secrets, credentials, state files, or personal information not supplied for publication.
