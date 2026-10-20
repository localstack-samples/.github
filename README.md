# .github

Organization-wide defaults for [localstack-samples](https://github.com/localstack-samples).

| Path | What it does |
|---|---|
| [`profile/README.md`](profile/README.md) | The profile shown on [github.com/localstack-samples](https://github.com/localstack-samples). |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), [`CONTRIBUTING.md`](CONTRIBUTING.md) | Shown in every repository that does not have its own. |
| [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/), [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) | The default issue forms and pull request template. A repository with its own `.github/ISSUE_TEMPLATE` folder or pull request template uses those instead. |
| [`workflow-templates/`](workflow-templates/) | The **LocalStack sample CI** workflow, offered in every repository under **Actions → New workflow**. |
| [`STATUS.md`](STATUS.md) | CI status of every public, unarchived repository, regenerated weekly (or on demand) by the [`status.yml`](.github/workflows/status.yml) workflow from [`scripts/generate_status.py`](scripts/generate_status.py). Exceptions to its rules go in [`status.toml`](status.toml). |
| [`assets/`](assets/) | Images used by the profile. |
