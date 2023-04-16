<p>
    <a href="https://www.linkedin.com/in/alexandergbraun" rel="nofollow noreferrer">
        <img src="https://www.gomezaparicio.com/wp-content/uploads/2012/03/linkedin-logo-1-150x150.png"
             alt="linkedin" width="30px" height="30px"
        >
    </a>
    <a href="https://github.com/theNewFlesh" rel="nofollow noreferrer">
        <img src="https://tadeuzagallo.com/GithubPulse/assets/img/app-icon-github.png"
             alt="github" width="30px" height="30px"
        >
    </a>
    <a href="https://pypi.org/user/the-new-flesh" rel="nofollow noreferrer">
        <img src="https://cdn.iconscout.com/icon/free/png-256/python-2-226051.png"
             alt="pypi" width="30px" height="30px"
        >
    </a>
    <a href="http://vimeo.com/user3965452" rel="nofollow noreferrer">
        <img src="https://cdn.iconscout.com/icon/free/png-512/movie-52-151107.png?f=avif&w=512"
             alt="vimeo" width="30px" height="30px"
        >
    </a>
    <a href="http://www.alexgbraun.com" rel="nofollow noreferrer">
        <img src="https://i.ibb.co/fvyMkpM/logo.png"
             alt="alexgbraun" width="30px" height="30px"
        >
    </a>
</p>

<!-- <img id="logo" src="resources/logo.png" style="max-width: 717px"> -->

[![](https://img.shields.io/badge/License-MIT-F77E70?style=for-the-badge)](https://github.com/thenewflesh/openexr-tools/blob/master/LICENSE)
[![](https://img.shields.io/pypi/pyversions/openexr-tools?style=for-the-badge&label=Python&color=A0D17B&logo=python&logoColor=A0D17B)](https://github.com/thenewflesh/openexr-tools/blob/master/docker/config/pyproject.toml)
[![](https://img.shields.io/pypi/v/openexr-tools?style=for-the-badge&label=PyPI&color=5F95DE&logo=pypi&logoColor=5F95DE)](https://pypi.org/project/openexr-tools/)
[![](https://img.shields.io/pypi/dm/openexr-tools?style=for-the-badge&label=Downloads&color=5F95DE)](https://pepy.tech/project/openexr-tools)

# Introduction
Tools for working with OpenEXR image files.

See [documentation](https://thenewflesh.github.io/openexr-tools/) for details.

# Installation
### Python
`pip install openexr-tools`

### Docker
1. Install [docker-desktop](https://docs.docker.com/desktop/)
2. `docker pull thenewflesh/openexr-tools:[version]`

### Docker For Developers
1. Install [docker-desktop](https://docs.docker.com/desktop/)
2. Ensure docker-desktop has at least 4 GB of memory allocated to it.
3. `git clone git@github.com:thenewflesh/openexr-tools.git`
4. `cd openexr-tools`
6. `chmod +x bin/openexr-tools`
7. `bin/openexr-tools start`

The service should take a few minutes to start up.

Run `bin/openexr-tools --help` for more help on the command line tool.

---

# Production CLI

openexr-tools comes with a command line interface defined in command.py.

Its usage pattern is: `openexr-tools COMMAND [ARGS] [FLAGS] [-h --help]`

## Commands

---

### bash-completion
Prints BASH completion code to be written to a _openexr-tools completion file

Usage: `openexr-tools bash-completion`

---

### zsh-completion
Prints ZSH completion code to be written to a _openexr-tools completion file

Usage: `openexr-tools zsh-completion`

---

# Development CLI
bin/openexr-tools is a command line interface (defined in cli.py) that works with
any version of python 2.7 and above, as it has no dependencies.

Its usage pattern is: `bin/openexr-tools COMMAND [-a --args]=ARGS [-h --help] [--dryrun]`

### Commands

| Command              | Description                                                         |
| -------------------- | ------------------------------------------------------------------- |
| build-package        | Build production version of repo for publishing                     |
| build-prod           | Publish pip package of repo to PyPi                                 |
| build-publish        | Run production tests first then publish pip package of repo to PyPi |
| build-test           | Build test version of repo for prod testing                         |
| docker-build         | Build image of openexr-tools                                              |
| docker-build-prod    | Build production image of openexr-tools                                   |
| docker-container     | Display the Docker container id of openexr-tools                          |
| docker-coverage      | Generate coverage report for openexr-tools                                |
| docker-destroy       | Shutdown openexr-tools container and destroy its image                    |
| docker-destroy-prod  | Shutdown openexr-tools production container and destroy its image         |
| docker-image         | Display the Docker image id of openexr-tools                              |
| docker-prod          | Start openexr-tools production container                                  |
| docker-push          | Push openexr-tools production image to Dockerhub                          |
| docker-remove        | Remove openexr-tools Docker image                                         |
| docker-restart       | Restart openexr-tools container                                           |
| docker-start         | Start openexr-tools container                                             |
| docker-stop          | Stop openexr-tools container                                              |
| docs                 | Generate sphinx documentation                                       |
| docs-architecture    | Generate architecture.svg diagram from all import statements        |
| docs-full            | Generate documentation, coverage report, diagram and code           |
| docs-metrics         | Generate code metrics report, plots and tables                      |
| library-add          | Add a given package to a given dependency group                     |
| library-graph-dev    | Graph dependencies in dev environment                               |
| library-graph-prod   | Graph dependencies in prod environment                              |
| library-install-dev  | Install all dependencies into dev environment                       |
| library-install-prod | Install all dependencies into prod environment                      |
| library-list-dev     | List packages in dev environment                                    |
| library-list-prod    | List packages in prod environment                                   |
| library-lock-dev     | Resolve dev.lock file                                               |
| library-lock-prod    | Resolve prod.lock file                                              |
| library-remove       | Remove a given package from a given dependency group                |
| library-search       | Search for pip packages                                             |
| library-sync-dev     | Sync dev environment with packages listed in dev.lock               |
| library-sync-prod    | Sync prod environment with packages listed in prod.lock             |
| library-update       | Update dev dependencies                                             |
| library-update-pdm   | Update PDM                                                          |
| session-app          | Run app                                                             |
| session-lab          | Run jupyter lab server                                              |
| session-python       | Run python session with dev dependencies                            |
| state                | State of openexr-tools                                                    |
| test-coverage        | Generate test coverage report                                       |
| test-dev             | Run all tests                                                       |
| test-fast            | Test all code excepts tests marked with SKIP_SLOWS_TESTS decorator  |
| test-lint            | Run linting and type checking                                       |
| test-prod            | Run tests across all support python versions                        |
| version              | Full resolution of repo: dependencies, linting, tests, docs, etc    |
| version-bump-major   | Bump pyproject major version                                        |
| version-bump-minor   | Bump pyproject minor version                                        |
| version-bump-patch   | Bump pyproject patch version                                        |
| zsh                  | Run ZSH session inside openexr-tools container                            |
| zsh-complete         | Generate oh-my-zsh completions                                      |
| zsh-root             | Run ZSH session as root inside openexr-tools container                    |

### Flags

| Short | Long      | Description                                          |
| ----- | --------- | ---------------------------------------------------- |
| -a    | --args    | Additional arguments, this can generally be ignored  |
| -h    | --help    | Prints command help message to stdout                |
|       | --dryrun  | Prints command that would otherwise be run to stdout |
