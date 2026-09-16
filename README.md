# Cloud Resume

Danish Suffian’s personal portfolio, connecting software engineering with cloud engineering. Phase 1 is a responsive static website with no build step, JavaScript, runtime dependencies, or external font requests.

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
│   └── aws-auth-check.yaml # AWS OIDC authentication check
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

For direct S3 website hosting, enable static website hosting and set the index document to `index.html`. The website objects need public read access, with compatible Block Public Access settings. Use the website endpoint shown in the bucket properties; it supports HTTP only. See the [AWS S3 hosting tutorial](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html) and [website endpoint documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteEndpoints.html).

The planned HTTPS setup uses CloudFront with a private S3 bucket and Origin Access Control. For that approach, leave S3 website hosting disabled, use the regular S3 bucket origin, and set CloudFront's default root object to `index.html`. See [AWS guidance on private S3 origins](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html). Deployment has not been verified. The authentication workflow checks AWS identity only; pushing to GitHub will not yet update S3. Upload changes manually until the CI/CD phase is implemented.

Deferred portfolio ideas are in [FUTURE.md](FUTURE.md); engineering phases and validation remain in [PLAN.md](PLAN.md).

## GitHub Actions and OIDC

Deployment learning is now in progress alongside the static frontend. The selected authentication approach is GitHub OIDC into an IAM deployment role in the production AWS account. GitHub issues an identity token; AWS STS validates it against the role trust policy and exchanges it for temporary AWS credentials. The upload command uses those credentials to access S3.

No long-lived AWS access key needs to be stored or manually rotated in GitHub. Temporary credentials still include an access key ID, secret access key, and session token; they expire and are obtained again when needed. The GitHub identity token and AWS credentials are distinct. Scope the role trust to the intended repository and branch or environment, and scope its permissions to the intended bucket. See [GitHub OIDC guidance](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) and [AWS temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html).

The workflow [`.github/workflows/aws-auth-check.yaml`](.github/workflows/aws-auth-check.yaml) is named **Verify AWS Authentication**. It runs on pushes to `main`, including merges from `dev`, direct pushes, and merges from other branches unless repository controls restrict them.

Its job runs on `ubuntu-latest` with `contents: read` for checkout and `id-token: write` for OIDC. The steps are:

1. **Checkout Code:** fetch the repository using `actions/checkout@v4`.
2. **Configure AWS Credentials:** use `aws-actions/configure-aws-credentials@v6.3.0` to assume the configured `cloud-resume-github-actions` role by its full ARN, with region `ap-southeast-1`.
3. **Verify AWS Caller Identity:** run `aws sts get-caller-identity` to inspect the account and assumed-role identity.

After committing and pushing the workflow, inspect **Verify AWS Authentication** in the GitHub Actions tab. A successful identity check should show the intended production account and an assumed-role ARN for `cloud-resume-github-actions`. No successful run or AWS trust-policy configuration has been independently verified yet. The identity check does not prove S3 permissions or upload any files.

After authentication succeeds, the same file can be renamed to `deploy-s3.yaml`, given a deployment display name, and extended with an S3 upload step. Retain checkout and AWS authentication. If separate workflows or jobs are used instead, the deployment job needs its own files and credentials; it does not inherit another job’s environment.

## Edit content

Update personal copy, links, experience, skills, and projects in `frontend/index.html`. Identity, contact details, and the portrait were supplied by the owner. Experience describes the provided professional background; employer names, dates, and measurable achievements have not been invented. Add those when available.

Cloud Resume is marked in development, CloudOps is planned, and Umrah Travel Platform is a preview with potential capabilities. Add verified project outcomes and repository/demo links when available. Update the footer year when appropriate.

The supplied portrait lives at `frontend/assets/images/danish.webp` and appears beside the About heading in a circular frame (stacked on narrow screens). The header and two-line SVG favicon use “Danish Suffian.”

Style tokens are at the top of `frontend/styles.css`. There are no environment-specific runtime values in this phase. Contact is a direct email link; the site does not submit, store, or track visitor data.

## Review status

The 2026-09-15 source review found no blockers to an initial GitHub publication. HTML nesting, unique IDs, internal links, local assets, image attributes, and SVG XML checks passed. Representative Git ignore rules passed; a credential-pattern scan found no matches, and the supplied WebP contained no EXIF/XMP metadata. This was a source review, not a complete security or browser audit.

The owner approved the circular portrait and About layout. Browser layout, keyboard, zoom, contrast, and print verification remain pending in `PLAN.md`. The initial review preceded Git initialization. Git now contains an initial commit and an origin remote for `DanishSuffian/cloud-resume`; remote publication has not been verified in this review.

## Frontend checks

- Check the page at 320px, 375px, 768px, and desktop widths, including browser zoom at 200%.
- Navigate using Tab and Enter: skip link, navigation, project disclosures, and contact links.
- Confirm section links resolve and email/LinkedIn point to the intended destinations.
- Confirm reduced-motion preferences disable smooth scrolling.
- Check print preview and verify no external assets are needed.

## Roadmap

1. **Current:** polished static portfolio.
2. **AWS hosting:** Route 53 DNS, CloudFront, ACM HTTPS, private S3, and Origin Access Control.
3. **Infrastructure as Code:** Terraform with understandable dev/prod separation.
4. **CI/CD:** GitHub Actions with AWS OIDC, frontend deployment, and cache invalidation.
5. **Backend:** API Gateway, Lambda, and DynamoDB for a small serverless feature.
6. **Observability:** useful CloudWatch dashboards and alarms.

Phase 1 is implemented with browser review still pending. See [the project plan](PLAN.md) for progress and completion criteria, [agent guidance](AGENTS.md) for repository conventions, and [architecture decisions](docs/architecture.md) for technical rationale.
