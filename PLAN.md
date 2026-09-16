# Cloud Resume plan

## Objective

Create a professional portfolio that communicates Danish Suffian’s software and cloud engineering experience, then evolve it incrementally into an application with secure hosting, reproducible infrastructure, automated delivery, and operational visibility.

## Current position

**Active work: frontend/live-site verification and incremental hosting and deployment improvements.** The static implementation exists, and the owner approved the circular portrait and About layout. Browser verification remains before considering Phase 1 complete; additional content enhancements are deferred in `FUTURE.md`. GitHub Actions now uploads the frontend to S3 using OIDC; the owner confirmed successful authentication and deployment on 2026-09-16. Phase 4 delivery began before Terraform, so phase numbers group work rather than enforce execution order. Terraform, backend, and observability remain planning only.

Current decision: keep plain HTML/CSS. Revisit React when a concrete interaction benefits from component state, or when learning React becomes an explicit project goal. See `docs/architecture.md` for the reasoning.

## Phase 1 — Static portfolio

### Implemented

- [x] Update the public project roadmap to a checklist with green “Done” checkmarks and orange “Planned” circles, including owner-confirmed HTTPS, Route 53, CloudFront, OAC, and automated cache invalidation. Keep outstanding verification in this internal plan.
- [x] Record deferred portfolio ideas in `FUTURE.md`, expand Git ignore rules, and document which files to publish to S3. GitHub Actions execution and S3 upload are now confirmed by the owner; live-site verification remains.
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
- [x] Publish the workflow to GitHub: owner-supplied Actions logs and successful run confirmation establish remote execution in `danishsuffian-labs/cloud-resume`.

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

## Phase 2 — AWS hosting (HTTPS, domain, CloudFront, and OAC configured)

The deployment targets `danishsuffian-resume-s3` in `ap-southeast-1`. On 2026-09-16 the owner confirmed successful upload and the Route 53 domain `danishsuffian.cloud` routing to CloudFront, with S3 origin access through OAC. This records owner-confirmed implementation; certificate, cache, and direct-bucket access checks have not been independently performed.

- [x] Configure the production deployment role, bucket destination, and `ap-southeast-1` region in the workflow; successful upload confirmed by the owner.
- [ ] Inspect the custom-domain site and confirm the page and all assets load correctly.
- [x] Configure `danishsuffian.cloud` and Route 53 DNS pointing to CloudFront (owner confirmation).
- [x] Configure CloudFront with S3 origin access through OAC (owner confirmation).
- [x] Integrate HTTPS for `danishsuffian.cloud` (owner confirmation).
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

## Phase 4 — CI/CD (OIDC, S3 deployment, and cache invalidation working)

The workflow `.github/workflows/deploy-s3.yaml`, named **Deploy Portfolio**, runs on pushes to `main`. It checks out code, assumes `cloud-resume-github-actions` through OIDC, verifies the caller identity, syncs `frontend/` to `s3://danishsuffian-resume-s3/`, and requests `/*` invalidation on distribution `E2MC444L6LW7DX`. Direct pushes and merges from branches other than `dev` also trigger it unless repository rules restrict them.

Evidence as of 2026-09-16: the owner supplied the emitted OIDC subject and audience, confirmed authentication after correcting the trust policy, shared a dry-run log for all four frontend assets, and confirmed successful actual upload. The owner subsequently confirmed the renamed workflow works with CloudFront invalidation, and that HTTPS is integrated. No independent AWS inspection or live browser check was performed during this update.

- [x] Place the workflow in `.github/workflows/` and define the push-to-main trigger.
- [x] Add checkout v6, `contents: read`, `id-token: write`, the role ARN, and AWS region.
- [x] Verify OIDC authentication after matching the trust policy to the emitted subject containing immutable IDs (owner confirmation).
- [x] Retain **Verify AWS Caller Identity** and remove temporary OIDC diagnostics.
- [x] Preview the four frontend uploads with `--dryrun`; owner-supplied log shows correct bucket-root paths.
- [x] Remove `--dryrun` and deploy to S3 successfully (owner confirmation).
- [x] Rename the workflow to `deploy-s3.yaml`, display name **Deploy Portfolio**, and job ID `deploy`.
- [ ] Review AWS policy scope against the actual upload needs; the owner reports PutObject, GetObject, ListBucket, and DeleteObject permissions. The workflow does not use `--delete`.
- [ ] Add appropriate frontend checks before deployment.
- [ ] Establish branch/environment protections and a practical rollback procedure.
- [x] Add `cloudfront:CreateInvalidation` permission and the post-upload invalidation step; successful workflow execution confirmed by the owner.
- [ ] Consider waiting for invalidation completion if deployment success should also guarantee CloudFront propagation. The current workflow only submits the request.
- [ ] Add a separate infrastructure workflow when Terraform is ready.

**Completion criteria:** deployment succeeds after appropriate checks, without long-lived AWS credentials in GitHub; protections, cache handling where applicable, and rollback are documented and verified. A successful upload alone does not complete every item in this phase.

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
