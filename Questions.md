# Questions

## 1. What are the assumptions you have made for this service and why?
See `Solution_overview.md` assumptions section.

## 2. How would you do to transition this solution into a cloud-based solution?
### 2.a What changes (if any) to your code would need to be made?
Some cloud vendors provide their own pipeline SDKs. I have designed my code to work with Sagemake Pipelines in particular, as you are able to wrap their pipeline steps around Python functions.
The main change would be most likely not pass data directly between steps like in the script. Instead, saving the output of each pipeline step to a bucket/data store in the cloud and then reading it in from there instead. 
I would also develop a separate
### 2.b What services would be required to implement this and which teams would you need to support you? Feel free to use any cloud provider you are familiar with or a diagram if helpful.
Support from Cloud enablement teams to setup the three accounts/environments of Dev, Pre-Prod and Prod. 
I would require the cloud vendors specific Machine learning pipelines SDK. Below I am going to show how I would implement this on Sagemaker.
I would implement approval gates, so the training pipeline would be developed locally, the data scientist and ml engineer approve it once they confirm it working in a dev environment. 
This then gets the model promoted to the central tooling account where models are hosted. The pipeline would also be promoted to a pre-production account where it runs on live data. 
Then, if it passes testing in pre-prod it goes live to the production account where it runs on a schedule to update the model in the central account.
This process would be repeated for the inference pipeline. Pipeline is deployed to dev using dev model registry, then if approved, deployed to pre-prod using the tooling account central model registry.
Then if working in pre-prod deployed to prod, also running on a schedule.
Below is a diagram to show

![training_pipeline](/diagrams/Training_pipeline_diagram.drawio.png)

### 2.c How would you ensure reliability of newly developed code before releasing to a production environment?
I briefly mention in `Solution_overview.md` about github PRs but will reiterate here as well. 
There should be PR rules on this repo in place to force users to merge only via Pull Requests, as well as requiring 1 or 2 approvers. This ensures that all code is reviewed before being merged to main and published to the dev/test envirionment.

On top of this, the use of `Ruff` as a linter and formatter, Pytype to enforce typing is consistent and unit tests with Pytests means that code is non-breaking, correctly formatted and type hinted.
Additionally, this code should go through testing in a dev environment and then a preprod environment. Dev environment is an environment where changes can be made easily and users have more permissions meaning that if the pipeline fails then changes can be tested and traced easily in the dev environment. Pre-Prod, however, acts as an exact mirror of Prod with the same connections. The only difference is that the output is not linked to a live service.

There should also be monitoring the model in all of these environments and tracking different statsitics such as Data Drift, Model Drift, Model performance, endpoint availability, hardware usage etc... This allows for tracking changes over time and detect perforamnce issues with the model, pipeline or infastructure before it affects our users.

## 3. What considerations are there to ensure the business can leverage this service?
Once the model has been made available to use either via batch inference or live inference, it should be made available to other engineering teams of the business by exposing it via a rest api or a web interface. We could also provide the model itself to other data science teams for usage by leveraging a central model registry. However, if this were to be done there should be SLAs agreed, horizontal scalabilty potentially needed as well as monitoring capabilities.
Theres also considerations around Data and AI governance on the use of the model, especially if we are using PII data to train it. We would need to lock down the environment the model deployed into and ensure we are using the businesses single sign on to allow access. 

### 3.a Is there anything you would need to improve or confirm with stakeholders that would increase the efficacy of this service?
See my improvements section in `solution_overview.md`.