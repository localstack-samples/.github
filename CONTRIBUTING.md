# Contributing to LocalStack Samples

Thanks for helping improve the LocalStack samples. Fixes to existing samples, new samples, and better docs and tests are all welcome.

Everyone taking part is expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Issues

Open issues in the repository of the sample they are about, and search its existing issues first.

- **A sample does not deploy, or its test fails:** use the **Sample bug report** form. Include how you started LocalStack, the LocalStack version, the commands you ran and the error output.
- **You would like a new sample:** use the **Sample request** form and describe the scenario and the services it should cover.
- **LocalStack itself behaves differently from the cloud provider**, for example an API returns the wrong result: report it in [localstack/localstack](https://github.com/localstack/localstack/issues) instead, with the sample as a reproduction.
- **Questions and help:** ask in the [LocalStack Community Slack](https://localstack.cloud/slack).

## Pull requests

1. Fork the repository and create a branch from `main`.
2. Keep the change focused on one sample or one problem.
3. Run the sample against LocalStack and check that its tests pass.
4. Open a pull request and fill in the template. CI deploys and tests the sample against LocalStack, and must pass before merging.

A sample is easy to run and to keep working when it has:

- **A README** that lists the prerequisites and the exact commands to start LocalStack, deploy the sample and try it out.
- **A test** that checks the sample works, not only that it deploys: for example, call the API and assert on the response. Most samples expose it as `make test`.
- **A CI workflow** that runs that test against LocalStack on every pull request. The **LocalStack sample CI** workflow template (Actions → New workflow) is a good starting point. It reads the auth token from the `LOCALSTACK_AUTH_TOKEN` repository secret.
- **Pinned versions** of the tools and dependencies it uses, so it keeps working over time.
- **No real credentials.** LocalStack accepts `test` / `test` as AWS credentials. Never commit an auth token or a cloud account's keys.

## License

By contributing, you agree that your contribution is licensed under the license of the repository you contribute to.
