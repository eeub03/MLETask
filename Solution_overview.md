## Problem Case
In this repo, we have been tasked with converting a Jupyter Notebook to a production ready pipeline. This pipeline needs to be:
- Robust and Tested Regularly.
- Model to be updated Regularly (Data comes in daily, so this Daily is probably the minimum).

## Key Design Decisions
This repo has been designed to use the following tools:
- Functional Style Programming
    - This repo has mostly been written in functional style, with some sprinkle of OOP for specific use cases such as the logger.
    - The reason for choosing Functional was that there was not much use for techniques such as Encapsulation and Stateful handling.
    - 
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
    - 
- Pandera
    - Data Validation
- Ruff
    - Linter and Formatter
- Pytype
    - Type Checker for type hints and returns.
- Config Files
    - Environment variables storage.
## Approach
My approach to this problem was iterative in nature. 
Firstly, setup a developer environment using UV and Github. Then installing packages to get the notebook to run, running and reading the notebook to gain understanding. 
Then, prepare the repo to handle different environments and also install packages to help with development such as pytype, Flake8 and black (now using ruff instead), pytest. 
Then, using Test Driven Development approach with the first part of the pipeline. Data collection, develop the data collection script.
Repeat this, without TDD for the rest of the notebook due to time constraints.
Once this was done, getting a simple CICD process setup with github actions by and also getting it to work locally for testing. 
Then after testing the individual notebook scripts, developing the main pipeline script to join them together.
Then Refactoring to reduce code duplication, improve readability and maintainability. Also Schema Validation to help ensure data integrity.
The main advantage of this approach is that it allowed me to firstly get the notebook working in script form, before doing any refactoring which allowed me to focus on getting it working first, then making it more robust and production ready. 


Assumptions:
- Users of this Repo are Data Scientists and ML Engineers.
- This if the first productionised use case.
- No integration with Cloud.
- Data Size can vary per month

Improvements:
- Add MetaData & Model Artifact Saving to cloud storage.
    - Even better, integrate with model registry service like MLFLOW
- Global Log list to avoid creating duplicate loggers.
- Finish CICD to deploy to Dev, Pre-PRod and Production environments.
- Use Joblib to implement paralleisation of pipeline steps and improve the overall performance of the pipeline.
- Improve pipeline out storing by creating a folder per pipeline step.
