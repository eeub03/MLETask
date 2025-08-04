# MLETask
The purpose of this repo is host the pipeline code for training a claims pipeline xgboost model. The output of which is a model artifact tar ready for use in inference.

# Quickstart.

If you just want to get started as soon as possible you can run `./scripts/setup_repo.sh` in a bash terminal to immediately install UV, Python 3.10 and get the venv created. 
Manual Setup is detailed in the section below.

# Setup
## VSCode Extensions
Before proceeding with setting up of python and the virtual environment, the following extensions and packages are recommended to download as they are in use in this repo:

| Extension    | Type | Note |
| -------- | ------- | ------|
| [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)| Linter/Formatter    |   |
| [Github Actions](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-github-actions)  | Git Integration    |   |
| [GitHub Local Actions](https://marketplace.visualstudio.com/items?itemName=SanjulaGanepola.github-local-actions) | Local CICD     |  Requires [Act](https://github.com/nektos/act) & [Docker](https://www.docker.com/) installed |
| [Error Lens](https://marketplace.visualstudio.com/items?itemName=usernamehw.errorlens)    | Error Highlighting    |    |
| [Git lens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)   | Git Integration    |    |


## [UV Package Manager](https://docs.astral.sh/uv/pip/environments/)
This repo makes use of the UV package manager for dependency handling and virtual environments. 

To get started, please install the UV package manager running the command below in a cli.
### Mac & Linux:
`curl -LsSf https://astral.sh/uv/install.sh | sh`
### Windows
`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`


## Install Python.

If you need to install Python or specifically need 3.10, you can install this `uv` by running:

`uv python install 3.10`

and pinning the version uv uses with

`uv python pin 3.10`

## Virtual Environment and Kernel Setup
Once this has been installed, you can create a virtual environment using the lock file by running:

`uv venv`

This will create a `.venv` directory. To activate this virtual environment in the cli run:

`source .venv/Scripts/activate`

Now, in order to get these packages to work with Jupyter notebook, we need to add it as kernel by running the following:

`ipython kernel install --name ".venv" --user`

### Adding new packages to repo.
To add a new package to repository and start using it immediately you can run the following commands:

`uv add <package_name>` 
then
`uv sync` 
Which will update the venv.

## Running Jupyter Notebooks.

Once you have done this, you can run the notebook either in VSCode or via JupyterLabs/Notebooks.

Running in VSCode should work natively for recent versions, but if not you can download the [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) from the extensions marketplace.

This will then enable the notebooks to be rendered. If you have been following the README up to this point, you should be be able to run the notebook and select the venv as the kernel.

# Running the training Pipeline Script

There is a pipeline script in `src/claims_pipeline/training_pipeline/pipeline.py`. In this pipeline, we perform Data collection, cleaning, training and validation. Then we produce a model artifact, ready for deployment for inference.
This script performs the following steps:
1. Data collection
2. Data preprocessing
3. Model Training
4. Parameter Hyper Tuning
5. Packaging of Model.

To run the script locally, you can use `uv run src/claims_pipeline/training_pipeline/pipeline.py dev`


## CICD
In order to support deployment of the model, Github Actions have been created to start the process of deploying models to development, pre-production and production environments.