# Cloud Resume

Danish Suffian’s personal portfolio, connecting software engineering with cloud engineering. The responsive static frontend has no build step, JavaScript, runtime dependencies, or external font requests. GitHub Actions now deploys its files to S3 using OIDC; the owner confirmed successful authentication and upload on 2026-09-16.

## Run locally

From this directory:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory frontend
```

Open http://localhost:8000. Stop the server with Ctrl+C. You can also open `frontend/index.html` directly in a browser.

## Structure

```text
cloud-resume/
├── frontend/
│   ├── index.html       # Semantic markup and portfolio content
│   ├── styles.css       # Design tokens, components, responsive and print styles
│   ├── favicon.svg
│   └── assets/images/danish.webp # Portrait used in About
├── backend/            # Reserved for Phase 5
├── infrastructure/     # Reserved for later AWS / Terraform work
├── docs/
│   └── architecture.md
├── .github/workflows/
│   └── deploy-s3.yaml # S3 deployment and CloudFront invalidation
├── .gitignore
├── AGENTS.md           # Guidance for coding agents
├── PLAN.md             # Phase status, tasks, and completion criteria
├── FUTURE.md           # Deferred portfolio improvements
└── README.md
```

## Publishing files

Keep the project source and documentation in GitHub, including `AGENTS.md`, `PLAN.md`, `FUTURE.md`, and `docs/architecture.md`. These record contributor guidance, implementation status, deferred ideas, and design decisions. `.gitignore` excludes local configuration, credentials, generated output, and Terraform working files; example configuration and `.terraform.lock.hcl` remain eligible for version control. Review staged files before committing. Ignore rules do not remove files already tracked by Git and do not filter S3 uploads.

For S3, upload only the **contents of `frontend/`** into the bucket root, preserving these paths:

```text
index.html
styles.css
favicon.svg
assets/images/danish.webp
```

The owner has configured `danishsuffian.cloud` with Route 53 DNS pointing to CloudFront, which accesses the S3 bucket through Origin Access Control (OAC). This is the current hosting setup, confirmed by the owner on 2026-09-16. OAC uses a regular S3 bucket origin rather than the S3 website endpoint. See [AWS guidance on private S3 origins](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html).

HTTPS on `danishsuffian.cloud` is configured, as confirmed by the owner. Pushes to `main` upload the frontend to S3 and then request a CloudFront invalidation for `/*` on distribution `E2MC444L6LW7DX`. The owner confirmed the updated workflow succeeds. Detailed certificate and direct-bucket access checks have not been independently performed.

Deferred portfolio ideas are in [FUTURE.md](FUTURE.md); engineering phases and validation remain in [PLAN.md](PLAN.md).

## GitHub Actions and OIDC

Automated S3 deployment is implemented alongside ongoing frontend verification. The selected authentication approach is GitHub OIDC into an IAM deployment role in the production AWS account. GitHub issues an identity token; AWS STS validates it against the role trust policy and exchanges it for temporary AWS credentials. The upload command uses those credentials to access S3.

No long-lived AWS access key needs to be stored or manually rotated in GitHub. Temporary credentials still include an access key ID, secret access key, and session token; they expire and are obtained again when needed. The GitHub identity token and AWS credentials are distinct. Scope the role trust to the intended repository and branch or environment, and scope its permissions to the intended bucket. See [GitHub OIDC guidance](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) and [AWS temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html).

The workflow [`.github/workflows/deploy-s3.yaml`](.github/workflows/deploy-s3.yaml) is named **Deploy Portfolio**. It runs on pushes to `main`, including merges from `dev`, direct pushes, and merges from other branches unless repository controls restrict them.

Its job runs on `ubuntu-latest` with `contents: read` for checkout and `id-token: write` for OIDC. The steps are:

1. **Checkout Code:** fetch the repository using `actions/checkout@v6`.
2. **Configure AWS Credentials:** use `aws-actions/configure-aws-credentials@v6.3.0` to assume the configured `cloud-resume-github-actions` role by its full ARN, with region `ap-southeast-1`.
3. **Verify AWS Caller Identity:** run `aws sts get-caller-identity` to inspect the account and assumed-role identity.
4. **Deploy Frontend to S3:** run `aws s3 sync frontend/ s3://danishsuffian-resume-s3/` to upload new or changed frontend files to the bucket root.
5. **Invalidate Cloudfront Cache:** run `aws cloudfront create-invalidation --distribution-id E2MC444L6LW7DX --paths "/*"` after the upload.

The workflow has been renamed to `deploy-s3.yaml`, with display name **Deploy Portfolio** and job ID `deploy`. It uses neither `--dryrun` nor `--delete`: uploads are real, and destination-only objects are retained. Automated frontend checks are still planned.

The owner supplied a dry-run log showing the expected four asset paths and then confirmed successful actual upload on 2026-09-16. Authentication succeeded after matching the role trust policy to GitHub’s emitted subject, including immutable organization/repository IDs. The temporary claim-inspection step has been removed. Check the page, stylesheet, favicon, photo, and navigation through `danishsuffian.cloud`; CloudFront with OAC uses the S3 bucket origin, not a public S3 website endpoint.

In GitHub’s Actions tab, inspect **Deploy Portfolio** for the identity, upload, and invalidation results. Creating an invalidation is asynchronous: the workflow submits the request but does not wait for `Completed`. Check completion in CloudFront’s Invalidations tab. Each execution of the step creates a request, including reruns and deployments with no changed files. It does not clear browser caches.

## Edit content

Update personal copy, links, experience, skills, and projects in `frontend/index.html`. Identity, contact details, and the portrait were supplied by the owner. Experience describes the provided professional background; employer names, dates, and measurable achievements have not been invented. Add those when available.

Cloud Resume highlights completed cloud hosting and automated deployment with a simple checklist: green checkmarks for “Done” and orange outlined circles for “Planned.” CloudOps is planned, and Umrah Travel Platform is a preview with potential capabilities. Add verified project outcomes and repository/demo links when available. Update the footer year when appropriate.

The supplied portrait lives at `frontend/assets/images/danish.webp` and appears beside the About heading in a circular frame (stacked on narrow screens). The header and two-line SVG favicon use “Danish Suffian.”

Style tokens are at the top of `frontend/styles.css`. There are no environment-specific runtime values in this phase. Contact is a direct email link; the site does not submit, store, or track visitor data.

## Review status

The 2026-09-15 source review found no blockers to an initial GitHub publication. HTML nesting, unique IDs, internal links, local assets, image attributes, and SVG XML checks passed. Representative Git ignore rules passed; a credential-pattern scan found no matches, and the supplied WebP contained no EXIF/XMP metadata. This was a source review, not a complete security or browser audit.

The owner approved the circular portrait and About layout. Browser layout, keyboard, zoom, contrast, and print verification remain pending in `PLAN.md`. The initial review preceded Git initialization. The repository is now `danishsuffian-labs/cloud-resume`. The owner supplied Actions output and confirmed successful OIDC authentication and S3 upload; this update did not independently access AWS or the live website.

## Frontend checks

- Check the page at 320px, 375px, 768px, and desktop widths, including browser zoom at 200%.
- Navigate using Tab and Enter: skip link, navigation, project disclosures, and contact links.
- Confirm section links resolve and email/LinkedIn point to the intended destinations.
- Confirm reduced-motion preferences disable smooth scrolling.
- Check print preview and verify no external assets are needed.

## Roadmap

1. **Implemented:** static portfolio; browser verification remains.
2. **AWS hosting:** HTTPS, Route 53 domain `danishsuffian.cloud`, CloudFront, and S3 access through OAC are configured (owner confirmation). Detailed hosting checks remain in `PLAN.md`.
3. **Infrastructure as Code:** Terraform with understandable dev/prod separation.
4. **CI/CD:** GitHub Actions with OIDC, S3 upload, and CloudFront invalidation implemented; frontend checks, deployment protections, and rollback remain.
5. **Backend:** API Gateway, Lambda, and DynamoDB for a small serverless feature.
6. **Observability:** useful CloudWatch dashboards and alarms.

Phase 1 is implemented with browser review still pending. See [the project plan](PLAN.md) for progress and completion criteria, [agent guidance](AGENTS.md) for repository conventions, and [architecture decisions](docs/architecture.md) for technical rationale.
