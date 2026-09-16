# Cloud Resume plan

## Objective

Create a professional portfolio that communicates Danish Suffian’s software and cloud engineering experience, then evolve it incrementally into an application with secure hosting, reproducible infrastructure, automated delivery, and operational visibility.

## Current position

**Active work: Phase 1 frontend verification and Phase 4 GitHub Actions/OIDC learning.** The static implementation exists, and the owner approved the circular portrait and About layout. Browser verification remains before considering Phase 1 complete; additional content enhancements are deferred in `FUTURE.md`. The owner has authored an OIDC authentication-check workflow as the first step toward S3 deployment. Terraform, backend, and observability remain planning only.

Current decision: keep plain HTML/CSS. Revisit React when a concrete interaction benefits from component state, or when learning React becomes an explicit project goal. See `docs/architecture.md` for the reasoning.

## Phase 1 — Static portfolio

### Implemented

- [x] Record deferred portfolio ideas in `FUTURE.md`, expand Git ignore rules, and document which files to publish to S3. GitHub push and AWS deployment remain unverified.
- [x] Create the project directory structure and local preview instructions.
- [x] Build hero, about, experience, technical skills, projects, contact, and footer sections.
- [x] Add responsive CSS, keyboard focus, skip navigation, native project disclosures, reduced-motion support, and print styles.
- [x] Use supplied identity and contact details; distinguish planned project capabilities.
- [x] Check initial HTML nesting, unique IDs, fragment links, and local asset paths.
- [x] Verify the initial page, stylesheet, and favicon return HTTP 200 from a local server.
- [x] Add repository instructions and a phased project plan.
- [x] Replace the terminal-prompt favicon with a two-line “Danish Suffian” wordmark and use the full name in visible branding.
- [x] Move the supplied WebP portrait into frontend assets and integrate it into the About section.
- [x] Redesign About with a circular portrait beside the heading and biography below; add a stacked mobile layout and refresh the stylesheet revision. Browser visual verification remains pending.

### Source review — 2026-09-15

- [x] Verify current HTML nesting, unique IDs, fragment links, local asset paths, image attributes, and SVG XML.
- [x] Check representative ignore rules while retaining all current source files, example configuration, and the Terraform lockfile path.
- [x] Scan text files for common credential patterns: no matches found. Inspect the WebP container: no EXIF/XMP metadata present. These checks do not constitute a full security audit.
- [x] Record the owner’s approval of the circular portrait and About layout.
- [x] Refresh all five Markdown documents to match the implementation and publication boundaries.
- [x] Initialize Git, create the initial commit, and configure the origin remote (observed initial commit `7ba1866` and remote for `DanishSuffian/cloud-resume`).
- [ ] Verify publication to GitHub; local Git state does not establish a successful remote push.

No source-level blocker to initial GitHub publication was found. This does not complete the browser checks or establish a live deployment.

### Remaining

- [ ] Review the favicon draft in a browser tab at small sizes and confirm the visual direction with the owner.
- [ ] Inspect layouts at 320px, 375px, 768px, and desktop widths; resolve overflow or readability issues.
- [ ] Verify keyboard traversal, skip navigation, project disclosures, and visible focus in a browser.
- [ ] Check 200% zoom, reduced-motion behavior, and print preview.
- [ ] Check text and interactive-control contrast and address any failures.
- [ ] Have the owner review existing copy and contact destinations. Optional employer details, achievements, and project stories remain in `FUTURE.md`.
- [ ] Complete a final browser review after any resulting changes.

**Completion criteria:** the owner is happy with the content and design; relevant browser checks pass; no broken internal links or missing assets remain; all project status claims match implemented work.

## Phase 2 — AWS hosting (not started)

Manual S3 website hosting has been discussed; no deployment has been verified. `README.md` explains the upload layout and the difference between direct S3 website hosting and the planned private S3/CloudFront setup.

- [ ] Choose domain, AWS account/region, and deployment environment.
- [ ] Serve private S3 content through CloudFront using Origin Access Control.
- [ ] Configure ACM HTTPS and Route 53 DNS records.
- [ ] Define appropriate HTML/asset caching and response security headers.
- [ ] Verify HTTPS, domain routing, cache behavior, and denied direct public S3 access.
- [ ] Document the architecture, manual setup, costs, and teardown steps.

**Completion criteria:** the portfolio is reachable over HTTPS through CloudFront, the bucket remains private, and deployment/configuration steps are documented.

## Phase 3 — Terraform (not started)

- [ ] Bring hosting resources under Terraform without unintentionally replacing working infrastructure.
- [ ] Manage S3, CloudFront, relevant IAM policies, DNS records, and ACM where practical.
- [ ] Separate dev/prod configuration and state; establish secure state storage and locking.
- [ ] Introduce modules only where they clarify responsibility or remove meaningful repetition.
- [ ] Review plans and document provisioning, updates, recovery, and teardown.

**Completion criteria:** infrastructure can be reproduced from documented Terraform configuration with isolated environment state and reviewed changes.

## Phase 4 — CI/CD (authentication check implemented; execution pending)

The workflow `.github/workflows/aws-auth-check.yaml` is named **Verify AWS Authentication**. It checks out code, assumes the configured `cloud-resume-github-actions` role through OIDC in `ap-southeast-1`, and runs **Verify AWS Caller Identity**. The local file has a full role ARN and triggers on pushes to `main`. As of the 2026-09-16 source inspection, the workflow is untracked locally; no successful Actions run or AWS-side configuration has been verified. It contains no S3 upload step.

- [x] Record the OIDC authentication decision.
- [x] Place `aws-auth-check.yaml` in `.github/workflows/`, set its display name, and define the push-to-main trigger.
- [x] Add checkout, `contents: read`, `id-token: write`, a full role ARN, and AWS region.
- [x] Add the **Verify AWS Caller Identity** step using `aws sts get-caller-identity`.
- [ ] Commit and push the workflow, then verify OIDC role assumption and the expected production identity in Actions logs.
- [ ] Configure the target S3 bucket and required upload permissions.
- [ ] After authentication succeeds, evolve the workflow into `deploy-s3.yaml`, retaining checkout and authentication and adding the frontend upload.
- [ ] Add appropriate frontend checks before deployment.
- [ ] Configure GitHub Actions OIDC with scoped AWS role trust and permissions.
- [ ] Deploy the frontend to S3 and refresh CloudFront content using the chosen caching strategy.
- [ ] Establish environment protections and a practical rollback procedure.
- [ ] Add a separate infrastructure workflow when the Terraform process is ready.

**Completion criteria:** the intended branch deploys successfully after checks, without long-lived AWS credentials in GitHub, and rollback is documented.

## Phase 5 — Serverless backend (not started)

- [ ] Choose one small feature, such as a visitor counter, before designing its API.
- [ ] Implement API Gateway → Lambda → DynamoDB with least-privilege IAM.
- [ ] Define validation, error handling, allowed origins, and appropriate request limits.
- [ ] Keep environment endpoints separate from application logic and credentials out of the browser.
- [ ] Verify API behavior, failure handling, and usable frontend behavior when the API is unavailable.

**Completion criteria:** one feature works end to end with scoped permissions, meaningful checks, and documented failure behavior.

## Phase 6 — Observability (not started)

- [ ] Choose useful service metrics: Lambda errors/duration/throttles, API Gateway traffic/errors, and CloudFront traffic/error rates.
- [ ] Build a focused CloudWatch dashboard and actionable alarms.
- [ ] Set log retention and avoid logging sensitive user data.
- [ ] Document how to investigate failures, test alert delivery, and estimate monitoring costs.

**Completion criteria:** a controlled failure is visible and diagnosable, alerts reach the configured destination, and the operational response is documented.

## Working rules

Keep the active phase and checklist accurate as work progresses. Record major architecture decisions in `docs/architecture.md`. Prefer the smallest useful increment; future features do not justify implementing unused services now.
