# Phase 1 architecture

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

The experience section summarizes supplied areas of work rather than presenting a dated employment history. Future cloud services are labeled as planned. No metrics, certifications, employers, live deployments, or unprovided project links are claimed.

## Verification boundary

The 2026-09-15 source review verified HTML nesting, references, image attributes, and SVG XML. The implemented accessibility and responsive features still require browser verification; see [PLAN.md](../PLAN.md) for the outstanding checks. Owner approval of the design does not replace those checks.

## Repository documentation

Markdown documents belong to the source repository: `README.md` explains usage, `AGENTS.md` guides contributors using coding agents, `PLAN.md` tracks delivery and evidence, and `FUTURE.md` holds deferred content ideas. This document records architecture decisions. Keep them versioned with the code so instructions and rationale evolve together.

## Future deployment boundary

`frontend/` is the complete static deployment artifact. Upload its contents to the bucket root, placing `index.html` beside `styles.css`, `favicon.svg`, and `assets/`. Repository documentation stays outside that artifact. Backend code and infrastructure can be introduced independently into their reserved directories. No API endpoint, credential, cloud resource, deployment workflow, or analytics collector exists in this phase.

When AWS hosting is introduced, Route 53 will resolve the domain to CloudFront; CloudFront will serve content from private S3 using Origin Access Control. DNS resolves the hostname rather than proxying application requests. HTTPS, cache behavior, response security headers, and deployment permissions will be configured in that phase. The stylesheet URL includes a manual revision query to refresh cached CSS after the portrait sizing change. This is not an automated asset-versioning strategy; do not assume immutable caching.

GitHub stores the source; S3 serves uploaded website files. No deployment workflow connects them yet, so a GitHub push alone does not update S3. Direct S3 website hosting was discussed as a manual first step; the planned HTTPS architecture remains private S3 with CloudFront and OAC. Deployment instructions are in [README.md](../README.md), and implementation status is in [PLAN.md](../PLAN.md).
