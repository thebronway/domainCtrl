# domainCtrl Roadmap

*Last updated: 2026-02-27*  
*Current Version: v0.7.3*

## Overview
This document tracks planned improvements, enhancements, and technical debt for domainCtrl. It serves as a living guide for development priorities.

## Release Roadmap

### Release v0.7.0: UI Polish & Frontend Refinements (Feature Release)
**Focus:** Cleaning up the user interface and improving dashboard usability.
* **Filter & Navigation Improvements**
  * **Goal:** Add up/down/reset behavior to the domain filter, and ensure the reset button only appears when actively filtering.
  * **Value:** Makes navigating a large list of domains significantly smoother and more intuitive.
* **Light Mode & Log Tweaks**
  * **Goal:** Improve contrast for light mode buttons and transition logs to a cleaner, plain-text format.
  * **Value:** Enhances readability and makes the dashboard feel more premium and responsive.

### Release v0.7.5: Data Hygiene & Manual Controls (Backend Release)
**Focus:** Ensuring backend stability, preventing storage bloat, and adding manual overrides.
* **Orphan Data Cleanup**
  * **Goal:** Add a confirmation prompt when deleting a domain, and ensure that deleting a domain completely wipes its associated `/certs/` directory, log files, and `app_state` entries.
  * **Value:** Prevents storage bloat and avoids Let's Encrypt rate-limiting issues caused by ghost directories left behind on the host machine.
* **CSS Organization**
  * **Goal:** Refactor and split the monolithic stylesheet into modular, manageable chunks.
  * **Value:** Pays down UI technical debt before adding more complex views.
* **Add AI usage declration**

### Release v0.8.0: Cert Management Updates and Refinements (Feature Release)
* **Force SSL Renewal Button**
  * **Goal:** Add a `--force-renewal` action to the UI for edge cases where a certificate is revoked, corrupted, or needs immediate replacement.
  * **Value:** Gives the user manual override capabilities when Certbot's automatic "skip if not near expiration" logic gets in the way.
* **External Certificate Monitoring**
  * **Goal:** Allow users to add a domain for "Monitoring Only." The app fetches the live SSL certificate from the domain's HTTPS endpoint to track expiration dates without managing the DDNS or renewals.
  * **Value:** Makes the dashboard a single pane of glass for *all* of a user's domains, even those managed by external load balancers like Traefik or Nginx Proxy Manager.
 
### Release v0.8.5: TBD

### Release v0.9.0: The Multi-Provider Shift (Feature Release)
**Focus:** Transitioning from a single global DNS provider to a flexible, per-domain architecture.
* **Per-Domain Provider Configuration**
  * **Goal:** Move `PROVIDER` and API credentials out of global environment variables and into the domain-specific JSON settings. Set the default state to a "Blank Canvas" (None).
  * **Value:** The biggest architectural leap for the app. Allows a user to manage one domain on Route53, and another on Cloudflare, all from the same dashboard.
* **New DNS Providers**
  * **Goal:** Add support for Cloudflare, Azure DNS, and Google Cloud DNS. Update the `Dockerfile` to include the necessary `python3-certbot-dns-*` plugins.
  * **Value:** Massively expands the target audience for the app, as Cloudflare is the most popular DNS provider for self-hosters.

### Release v0.9.5: Security & Project Health (Backend/Tech-Debt Release)
**Focus:** Securing the application for the open web and improving open-source maintainability.
* **Code Hardening & Basic Authentication**
  * **Goal:** Add native Basic Auth or a simple password wrapper to the Flask app, alongside input sanitization and general penetration testing.
  * **Value:** Removes the strict requirement for users to set up a reverse proxy with auth just to use the app safely. 
* **Git Housekeeping**
  * **Goal:** Create a GitHub Wiki for documentation, and set up Issue/Bug Report templates.
  * **Value:** Encourages community contributions and cuts down on repetitive support questions.

### Release v1.0.0: The "Hub" & External Monitoring (Feature Release)
**Focus:** Expanding the app to track external services and receive remote updates.
* **Inbound API Webhooks (Local/Remote Architecture)**
  * **Goal:** Create secure, API-key-protected endpoints. 
  * **Value:** Allows MSPs or others who have multiple sites to manage everything from one master dashbaord.