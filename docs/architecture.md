# Cloud Resume architecture

## Static HTML and CSS

The site is a single document served with a stylesheet, a local WebP portrait, and a local SVG favicon. Content is available immediately and works without JavaScript. Native anchor navigation and `details` disclosures provide the required interactions. A framework or bundler would add maintenance without solving a current requirement.

Reusable CSS classes cover section headings, buttons, tags, cards, and layout containers. Central CSS custom properties define the visual system. Semantic sections keep content readable and easy to update without a templating layer. Consider templates or a static site generator only when multiple pages or repeated content justify them.

## React decision

Keep the current HTML/CSS implementation for Phase 1. This is a content-focused page with native navigation and disclosures; it currently has no complex client-side state. Introducing React now would add dependencies and a development toolchain without addressing an unmet requirement.

A visitor counter or basic contact form can be added with small JavaScript modules when their backend phase begins. Reconsider React for features with substantial shared state, complex filtering, or dashboard interactions, or if the owner explicitly prioritizes learning React. Adding more static content alone is a reason to consider templates, not necessarily a client-side framework.

React can be integrated into a specific part of an existing page without rewriting the whole site; see the [official incremental integration guide](https://react.dev/learn/add-react-to-an-existing-project). If adopted later, preserve the design and existing behavior, identify which UI React owns, and document any change to the build/deployment artifact. This is a recommendation, not a permanent restriction.

## Brand mark

The favicon uses the owner’s full name, “Danish Suffian,” on two lines over the existing dark rounded tile, with an orange second line. It uses a local system font stack. The full name is intentionally retained at the owner’s request, although text is very small at browser-tab sizes; visual review remains pending. Visible wordmarks also use the full name.

The supplied portrait stays unchanged at `frontend/assets/images/danish.webp`. The About section uses a centered reading column: a circular portrait beside the heading, followed by the biography. The owner approved this layout. A warm white border ties the portrait to the existing palette. The image is 180px on desktop and 140px on smaller screens; the heading stacks beneath it at 480px and below. CSS provides the circular presentation without creating a new image asset. Native lazy loading defers the image, and HTML dimensions reserve its aspect ratio.

## Accessibility and responsive behavior

The frontend includes a skip link, descriptive landmarks, hierarchical headings, visible keyboard focus, native disclosure controls, reduced-motion support, and mobile layouts. The decorative project illustration is made with HTML/CSS and hidden from assistive technology. A system font stack avoids third-party requests. Print styles support a simpler paper layout.

## Content integrity

The experience section summarizes supplied areas of work rather than presenting a dated employment history. Future cloud services are labeled as planned. No unprovided metrics, certifications, employers, or project links are claimed. The portfolio describes owner-confirmed automated S3 uploads, CloudFront invalidation, and HTTPS with Route 53/CloudFront/OAC hosting. Its public roadmap uses a checklist with green checkmarks for “Done,” orange outlined circles for “Planned,” and subtle row dividers. Status text remains visible so meaning does not depend on color alone; outstanding verification is tracked in `PLAN.md`, not presented as a public milestone.

## Verification boundary

The 2026-09-15 source review verified HTML nesting, references, image attributes, and SVG XML. The implemented accessibility and responsive features still require browser verification; see [PLAN.md](../PLAN.md) for the outstanding checks. Owner approval of the design does not replace those checks.

## Repository documentation

Markdown documents belong to the source repository: `README.md` explains usage, `AGENTS.md` guides contributors using coding agents, `PLAN.md` tracks delivery and evidence, and `FUTURE.md` holds deferred content ideas. This document records architecture decisions. Keep them versioned with the code so instructions and rationale evolve together.

## Deployment boundary

`frontend/` is the complete static deployment artifact. Upload its contents to the bucket root, placing `index.html` beside `styles.css`, `favicon.svg`, and `assets/`. Repository documentation stays outside that artifact. Backend code and infrastructure can be introduced independently into their reserved directories. The frontend contains no API endpoint, credential, or analytics collector. The workflow in `.github/workflows/deploy-s3.yaml` uploads the frontend to S3. The owner confirmed successful execution; AWS resources and live website access have not been independently inspected.

The owner confirmed HTTPS and Route 53 configuration for `danishsuffian.cloud` pointing to CloudFront, with CloudFront accessing S3 through OAC. DNS resolves the hostname; it does not proxy requests. The request path is browser → CloudFront → S3. Direct-bucket restrictions and certificate configuration still require independent inspection. The stylesheet URL includes a manual revision query for the milestone styling change; this is not an automated versioning strategy and does not replace CloudFront cache handling.

GitHub stores the source; S3 serves uploaded website files. The **Deploy Portfolio** workflow checks identity, uploads the frontend, and requests CloudFront invalidation on pushes to `main`. CloudFront with OAC and the Route 53 domain are now configured according to the owner. Deployment instructions are in [README.md](../README.md), and implementation status is in [PLAN.md](../PLAN.md).

## Deployment authentication: GitHub OIDC

The owner selected OIDC for GitHub Actions to authenticate to AWS. The production account holds the GitHub IAM OIDC provider and the deployment role in the intended design; IAM Identity Center continues to provide human account access. AWS requires the OIDC provider and its trusting role to reside in the same account. See [AWS OIDC provider guidance](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html).

The authentication sequence is:

1. The workflow job requests a GitHub OIDC identity token with `id-token: write`.
2. The AWS credentials action sends that token to AWS STS through `AssumeRoleWithWebIdentity`.
3. AWS validates the token and the role’s trust conditions, then returns temporary AWS credentials.
4. The AWS CLI uses those credentials to perform operations permitted by the role, such as uploading frontend assets to S3.

`id-token: write` permits requesting an identity token; it does not grant S3 write access. The trust policy controls who can assume the role, while the permissions policy controls the allowed AWS operations. Repository checkout also needs its own appropriate GitHub permissions.

This avoids storing long-lived AWS keys in GitHub and their manual rotation. AWS still issues a temporary access key ID, secret access key, and session token with an expiration. New credentials are requested for subsequent sessions. Expiration does not replace scoped trust and permissions. See [GitHub OIDC setup](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) and [AWS STS credential exchange](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html).

## Current workflow and verification

`.github/workflows/deploy-s3.yaml` uses `actions/checkout@v6`, `aws-actions/configure-aws-credentials@v6.3.0`, the configured deployment role, and region `ap-southeast-1`. After `aws sts get-caller-identity`, it runs:

```sh
aws s3 sync frontend/ s3://danishsuffian-resume-s3/
```

This uploads new or changed files to the bucket root. There is no `--delete`, so objects removed from the repository remain in S3 until separately removed. After upload, the workflow requests `/*` invalidation on distribution `E2MC444L6LW7DX`. Automated frontend checks and rollback remain planned.

The authentication issue was resolved by matching the trust policy to the exact subject GitHub emitted:

```text
repo:danishsuffian-labs@329593354/cloud-resume@1371270362:ref:refs/heads/main
```

The audience is `sts.amazonaws.com`. These identifiers are identity metadata, not credentials. Preserve the exact match; do not broaden it to bypass an authentication error. Temporary token-inspection code was removed after diagnosis.

On 2026-09-16 the owner confirmed successful authentication and actual upload, following a dry run showing `index.html`, `styles.css`, `favicon.svg`, and `assets/images/danish.webp` at the expected paths. This records user-confirmed deployment evidence, not an independent AWS audit. Live-site and browser verification remain in [PLAN.md](../PLAN.md).

Checkout and authentication must remain in the deployment job. Separate jobs do not inherit its local files or credentials. The workflow is now `deploy-s3.yaml`, named **Deploy Portfolio**, with job ID `deploy`.

## CloudFront invalidation

After the S3 sync succeeds, the workflow runs:

```sh
aws cloudfront create-invalidation --distribution-id E2MC444L6LW7DX --paths "/*"
```

The GitHub deployment role needs `cloudfront:CreateInvalidation` for `arn:aws:cloudfront::050649355884:distribution/E2MC444L6LW7DX`. The owner confirmed adding the permission and a successful workflow run. This extends the permissions policy; OIDC trust remains unchanged.

The wildcard covers all URL paths, including the HTML, stylesheet, favicon, and photo. It is quoted so the shell passes it literally. Invalidation runs after upload so new origin files are available when CloudFront fetches them. Each executed step submits a new request, even on a rerun or an unchanged sync. Completion is asynchronous; the workflow does not currently wait for propagation. Browser caches are separate. Future work can reduce unnecessary runs and add a completion wait if needed.
