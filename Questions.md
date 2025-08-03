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


### 2.c How would you ensure reliability of newly developed code before releasing to a production environment?