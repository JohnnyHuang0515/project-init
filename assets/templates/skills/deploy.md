---
name: deploy
description: Deploy {{PROJECT_NAME}} to {{DEPLOY_TARGET}}. Use when the user asks to deploy, release, ship, or push to production/staging. Covers the full pre-flight check, deployment steps, and post-deploy verification.
---

# Deploy

Workflow for deploying {{PROJECT_NAME}} to {{DEPLOY_TARGET}}.

## Pre-flight checklist

Before deploying anything, verify:

- [ ] All tests pass: `{{TEST_CMD}}`
- [ ] Linter is clean: `{{LINT_CMD}}`
- [ ] Local branch is up to date with `main` (or release branch).
- [ ] No uncommitted changes (`git status` is clean).
- [ ] The change has been reviewed — either a merged PR, or explicit user approval for direct deploys.
- [ ] Required secrets and config are present in the target environment.
- [ ] Any database migrations have been applied (or are included in the deploy).

If **any** of these fail, stop and surface the issue. Don't deploy past a failure.

## Deployment steps

<!-- TODO: Fill in the concrete steps for your setup. Example for a generic setup:

1. Build: `{{BUILD_CMD}}`
2. Tag the release: `git tag -a vX.Y.Z -m "release notes"`
3. Push: `git push && git push --tags`
4. Trigger deploy: `{{DEPLOY_CMD}}`
5. Wait for CI/CD to report success.
-->

## Post-deploy verification

After the deploy completes:

- [ ] Smoke test the main user flow (login, key endpoint, etc.).
- [ ] Check error monitoring (Sentry/Datadog/etc.) for new errors.
- [ ] Check the deployment platform's health indicators.
- [ ] If you deployed a migration, verify the schema is as expected.

If something's wrong, follow the rollback procedure:

<!-- TODO: Document rollback. Example:
- Vercel: `vercel rollback`
- Fly.io: `fly releases list` + `fly deploy --image <previous>`
- Manual: revert the commit and redeploy.
-->

## What to report to the user

When the deploy finishes, report:
1. What was deployed (commit SHA, branch, version tag).
2. What environment it went to.
3. Any warnings from the pre-flight or post-deploy checks.
4. Link to the deploy dashboard if available.

## What not to do

- Don't deploy at the end of the day or before a weekend unless it's an emergency fix.
- Don't deploy with failing tests, even "just this once".
- Don't skip the post-deploy verification — deploys that appear to succeed can still be broken.
- Don't deploy and disappear — stick around to monitor for at least a few minutes.
