# MLETask
Repo for MLE task

# Setup
This repo makes use of the UV package manager for dependency handling and virtual environments. 

To get started, please install the UV manager running the command below in a cli.
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

## Running Jupyter Notebooks.

Once you have done this, you can run the notebook either in VSCode or via JupyterLabs/Notebooks.

Running in VSCode should work natively for recent versions, but if not you can download the [Jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) from the extensions marketplace.

## Running GitHub Actions Locally.

In order to run github actions locally, we can make use of Docker Engine/Desktop, act and Github Local actions. This accelerates testing by avoiding committing to main and allowing for debugging of cicd locally.