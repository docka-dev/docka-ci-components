# Docka CI Components

Reusable GitLab CI component source for OIDC-first Docka deployments. It exchanges the GitLab job identity for a short-lived token restricted to one Docka app and environment, then deploys the exact `CI_COMMIT_SHA`.

The public GitLab.com consumption mirror is not published yet. The example below becomes valid after that mirror exists; do not reference it before then.

```yaml
include:
  - component: gitlab.com/docka-dev/docka-ci-components/deploy@main
    inputs:
      docka-url: https://api.docka.dev
      app-id: 11111111-1111-4111-8111-111111111111
      environment: production
```

Create the matching GitLab CI trust rule in Docka first. Bind the immutable project and namespace IDs, exact ref, app, environment, and protected-ref requirement.

The component uses GitLab `id_tokens` with audience `https://api.docka.dev/ci`. For systems without conformant OIDC, store an expiring app-restricted Docka token in a masked variable named `DOCKA_TOKEN`. Change `token-variable` if your variable uses another name.

The default Python image provides the standard library client. Override `image` only with a reviewed image that contains Python 3.11 or newer. The component has no package installation step.

Outputs are exposed through the dotenv artifact:

- `DOCKA_DEPLOYMENT_ID`
- `DOCKA_DEPLOYMENT_STATUS`
- `DOCKA_DEPLOYMENT_URL`

The default wait is capped at 240 seconds to stay within the short-lived OIDC exchange token. Set `wait: false` for longer deployments.

## Development

```sh
python test_component.py
```

The GitHub repository is canonical. A GitLab component project on the same GitLab instance is required for component consumption.

Use an immutable release tag once the first public GitLab.com compatibility test is published. `main` is the pre-release integration target.
