## Problem Case
In this repo, we have been tasked with converting a Jupyter Notebook to a production ready pipeline. This pipeline needs to be:
- Robust and Tested Regularly.
- Model to be updated Regularly (Data comes in daily, so this Daily is probably the minimum).
- Inference Ran as batch jobs when data comes in.

## Key Design Decisions
This repo has been designed to use the following tools:
- Functional Style Programming
    - This repo has mostly been written in functional style, with some sprinkle of OOP for specific use cases such as the logger.
    - The reason for choosing Functional was that there was not much use for techniques such as Encapsulation and Stateful handling while code readability and maintainability was prioritised.
    - There are however some functions that could make better use of encapsulation, see `model_evaluation.py`
- UV
    - Package and Virtual Env Manager.
    - Written in rust and extremely fast.
    - pyproject.toml and .lock file allows for consistent development experience across team by enforcing specific packages and versions are installed into the virtual environment and pipeline.
    - It is however relatively new so lacks some features more mature package managers may have.
- Pytest
    - Test Suite.
    - More feature rich than the built in unit test suite that python offers.
    - Lots of Plugins allow for further features
        - Example of pytest-xdist allowing for parallelising of tests across cores via one flag `pytest -n auto`
    - Widely used in the tech world, so most devs are familar with this suite.
    - Doesn't support Behavourial Driven Development as much as other frameworks.
- Github Actions.
    - CICD Deployment.
    - Very easy to learn and pickup. 
    - Actions very modular and customisable.
- Pandera
    - Data Validation
    - Allows for easy validation of Pandas Dataframes.
    - Only useful for validating data after preprocessing and data in Pandas Dataframe form.
- Ruff
    - Linter and Formatter
    - Combines aspects of Flake8 linter and Black Formatter.
    - Real time formatting and linting due to being written in Rust.
    - Out of the box severity levels too limiting, so requires some tweaking.
    - Keeps coding standards more consistent.
- Pytype
    - Type Checker for type hints and returns.
    - Allows for checking that we are passing the correct types to functions.
    - Extremely slow, so will slow down CICD pipeline significantly if steps are not parallised.
- Config Files
    - Environment variables storage.
    - Kept as code so highly visible.
    - Stored in yml for readability.
    - Can be validated with schema files.
    - Easy to manage, maintain and modify for different environments.
- Pipeline.py
    - Main file for running pipeline code.
    - Split up steps into their own functions for readability and maintainability.
    - Same reason for splitting out the different steps into their own directories and modules.
        - This means there is less risk of changing main script code when only needing to change one step.
    - Easily convertible to cloud solutions.
        - We can wrap cloud specific pipeline solutions around our functions. E.G. Sagemaker Pipelines steps take in python functions as arguments.
    - The main disadvantage to this approach is that it takes a lot of developer effort to setup.
- Data, Training and Model pipelines.
    - These were split up this way as it is good to decouple use cases in ML Pipelines for maintainabiltiy reasons.
    - This can be overkill for small use cases where we are not reusing aspects of our data pipeline or don't need to run data pipelines separately from training.
    - By doing this, it allows for reusability of our query and data cleaning functions in our inference and training pipelines.
    - This also separates those uses cases, as we may want to run our training pipelines several times without performing live inference on prod data.


## Approach
My approach to this problem was iterative in nature. 
Firstly, setup a developer environment using UV and Github. Then installing packages to get the notebook to run, running and reading the notebook to gain understanding. 
Then, prepare the repo to handle different environments and also install packages to help with development such as pytype, Flake8 and black (now using ruff instead), pytest. 
Then, using Test Driven Development approach with the first part of the pipeline. Data collection, develop the data collection script.
Repeat this, without TDD for the rest of the notebook due to time constraints.
Once this was done, getting a simple CICD process setup with github actions by and also getting it to work locally for testing. 
Then after testing the individual notebook scripts, the next task was to develop the main pipeline script to join them together to work as python scripts.
Then Refactoring to reduce code duplication, improve readability and maintainability. Also Schema Validation to help ensure data integrity.
The main advantage of this approach is that it allowed me to firstly get the notebook working in script form, before doing any refactoring which allowed me to focus on getting it working first, then making it more robust and production ready. 
One of the refactors later on was splitting the main pipeline script up, since it was a training script. So the Data collection and cleaning was taken out.

## Assumptions and Limitations
### Assumptions:
- Users of this Repo are Data Scientists and ML Engineers.
- This if the first productionised use case. So we are writing some functions to be reusable for future use cases/models and also developing some design patterns.
- No integration with Cloud.
- Data Size can vary per month
- The notebook/model scripts are correct e.g. `family_hist_3` will always contain null/missing values.
- There are Dev, Pre-Prod and Prod environments we will deploy this script to.
- Will be able to collaborate with Data Scientists to improve model performance.


### Limitations
- Cloud vendor - Unknown at this point, so we just running the pipeline locally or via Github Actions in a Docker Container.
- Parallelisation - This code will mostly run single threaded for most of our custom functions and processes. Some modules do have built-in automatic use of threads and processes such as XGBoost and JobLib.
    - This code is also designed to run on a single instance/node/computer.
    - This means that this pipeline will not scale to large amounts of data very well.
- Containerisation - Right now we are using the UV Docker image in our cicd pipeline, but we may want to add more features in the future to support model deployment such as an API, entrypoint scripts, faster startup and build time etc... 
    - We are also using the same image for our CICD that we are using to run the pipeline.
- SQL Query - Currently our query is stored in a config file, but it should changed to point to an `.sql` file so that we can pass in bigger/more complex queries in future if we want and we can still benefit from versioning of the file.
- Github Repo rules - Currently there are no rules to prevent admins from pushing straight to main. 
- No Data Versioning - We don't save the data we currently query as a version of the dataset so it will be much more diffult if not impossible to replicate model results if data changes.

### Improvements
- Add MetaData & Model Artifact Saving to cloud storage.
    - Even better, integrate with model registry service like MLFLOW.
- Global Log list to avoid creating duplicate loggers.
- Finish CICD to deploy to Dev, Pre-Prod and Production environments.
- Use Joblib to implement paralleisation of pipeline steps and improve the overall performance of the pipeline.
- Improve pipeline.out storing by creating a folder per pipeline step for easier readability.
- Add further Github Rules to only allow pushing to main via a Pull request with 1 approval.
- Parallelise data preprocessing steps.
- Add support for custom docker image for model deployment.
- Create a custom docker image for model deployment.
- Implement support for running pipeline across multiple instances to support big data use cases.
- Data Versioning.

