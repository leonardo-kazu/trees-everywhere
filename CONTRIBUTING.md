# Contributing

- [Contributing](#contributing)
  - [Configuration](#configuration)
  - [Branches](#branches)
  - [Commit Messages](#commit-messages)

It's expected that for contributing to the project, one will have installed the project with all of it's dependencies. To do so, you can follow the [Installation](../README.md#installation) section of the README.md file.

## Configuration

The project uses [pre-commit](https://pre-commit.com/) to run some checks before the commit. To install the pre-commit hooks, you can use the following command:

```bash
poetry run pre-commit install
```

To run the pre-commit checks manually, you can use the following command:

```bash
poetry run pre-commit run --all-files
```

## Branches

The project uses the [Trunk Based Development](https://trunkbaseddevelopment.com/) branching strategy. By doing it so, the project has only two long-lived branches:

- `release`: The main branch of the project. It's the branch where the production code is.
- `dev`: The development branch of the project. It's the branch where the development code is.

> **!IMPORTANT!** This branches should not be directly commited to, and the pre-commit hooks will not allow it.

To contribute to the project, you should create a new branch from the `dev` branch, and then create a pull request to the `dev` branch. After the pull request is approved, it will be merged to the `dev` branch, and then, when the `dev` branch is ready, it will be merged to the `release` branch.

The branch name should be in the following format:

```text
<type>/<branch-description>
```

Where `<type>` is the type of the branch, and `<branch-description>` is a short description of the branch. The following types are allowed:

- `feat`: A new feature for the project.
- `fix`: A fix for a bug in the project.
- `hotfix`: A fix for a bug in the production code.
- `build`: A change in the project dependencies, build process or configuration.
- `docs`: A change in the project documentation.
- `style`: A change in the project style.
- `refactor`: A change in the project code that does not change it's behavior.
- `test`: A change in the project tests.
- `ci`: A change in the project CI/CD.

## Commit Messages

The project uses the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) commit message format. By doing so, the project can use the [Semantic Versioning](https://semver.org/) versioning strategy.

To make commits, please use the following command:

```bash
poetry run cz commit
```

And then follow the instructions to make the commit message.
