# Prefect playground


## Overview

1. This repo is setup as a [uv library](https://docs.astral.sh/uv/concepts/projects/init/#libraries) in src
2. The prefect flows can be found in the flows folder. And some other example in tutorial - which were adapted from the tutorial and will be deleted in the future.
3. The prefect deployment setup is in the [prefect config file](./prefect.yaml).


## Dev Setup
Copy the repo and setup local environment

```bash
# 1. Clone the repo
git clone git@github.com:gee-gendo/test-prefect-deployment.git

# 2. Setup python env with uv (optional, it will be lazy loaded by uv but worth doing)
uv sync

# 3. Setup pre-commit
uv run pre-commit install

# 4. sign-in to prefect cloud
uv run prefect-cloud login
```

More info on prefect-cloud signin in the [Quickstart](https://docs.prefect.io/v3/get-started/quickstart)

## Deploying

Deployement are described by the [prefect config](./prefect.yaml). Tu deploy a new version

```bash
# 1. Push your change and tag the commit
git add ...
git commit -m <my message>
git tag <vX.X.X>
git push; git push --tag

# 2. Edit the git-clone step in the [prefect config](./prefect.yaml) to point to your new tag
...

# Deploy wizard
prefect deploy
```

You can then trigger the flow / deployment on the UI or any other ways

### ⚠️ 🐍 Important python deployment quirk

Prefect requires a "pull" step to install the python dependencies in the worker. This is configured in the [prefect config](./prefect.yaml). The commented example with pip requires the silly "." [pip requirements](./requirements.txt). Alternatively, the uncommented `run_shell_script` runs pip on the project.

⚠️ All the requirements should be in the [pyproject](./pyproject.toml) file!! ⚠️
