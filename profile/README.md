<p align="center">
  <img src="/assets/banner.png" alt="LocalStack: Run Locally, Deploy Globally" />
</p>

<p align="center">
  <a href="https://docs.localstack.cloud"><img alt="Docs" src="https://img.shields.io/badge/docs-localstack.cloud-blue"></a>
  <a href="https://blog.localstack.cloud"><img alt="Blog" src="https://img.shields.io/badge/blog-localstack.cloud-purple"></a>
  <a href="https://localstack.cloud/slack"><img alt="Slack" src="https://img.shields.io/badge/Slack-@localstack-purple.svg"></a>
  <a href="https://www.youtube.com/@localstack"><img alt="YouTube" src="https://img.shields.io/badge/YouTube-@localstack-red.svg"></a>
  <a href="https://www.linkedin.com/company/localstack-cloud"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-@localstack-darkblue.svg"></a>
</p>

## LocalStack Samples

Sample applications that run on [LocalStack](https://localstack.cloud), the local cloud development platform. Each sample deploys a real architecture to the LocalStack emulators for AWS, Snowflake or Azure, on your machine or in CI, with no cloud account. Most samples also include a CI workflow that deploys the app and tests it on every pull request.

## Run a sample

1. Install the [`lstk` CLI](https://docs.localstack.cloud/aws/developer-tools/running-localstack/lstk/) and log in:

   ```bash
   brew install localstack/tap/lstk   # or: npm install -g @localstack/lstk
   lstk login                         # or: export LOCALSTACK_AUTH_TOKEN=<your-token>
   ```

2. Start the emulator the sample needs:

   ```bash
   lstk start                     # AWS
   lstk start --type snowflake    # Snowflake
   lstk start --type azure        # Azure
   ```

3. Clone a sample and follow its README to deploy and test it.

Browse [all repositories](https://github.com/orgs/localstack-samples/repositories), check the [CI status of every sample](https://github.com/localstack-samples/.github/blob/main/STATUS.md), or find samples by service in the [docs](https://docs.localstack.cloud/applications/).

## Contributing

Found a broken sample or want a new one? [Open an issue](https://github.com/localstack-samples/.github/blob/main/CONTRIBUTING.md#issues) in the sample's repository, or read the [contributing guide](https://github.com/localstack-samples/.github/blob/main/CONTRIBUTING.md) to add your own. Everyone taking part is expected to follow our [Code of Conduct](https://github.com/localstack-samples/.github/blob/main/CODE_OF_CONDUCT.md).

Found a bug in LocalStack itself? [Start a discussion](https://github.com/orgs/localstack/discussions) in the LocalStack community. For questions, join the [LocalStack Community Slack](https://localstack.cloud/slack).
