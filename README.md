# Responsible AI Template

## License
This template is licensed to Customer subject to the terms of the license agreement between Domino and the Customer on file.

## About this project
This project examplify our project structure and how to ensure we deliver the best models to our users. It helps you ensure that projects run all these steps before deploying your model to a staging environment. 

- [ ] Run bias validation 
- [ ] Run fairness validation 
- [ ] Check probability distribution 
- [ ] Check confusion matrix
- [ ] Analyse features importance 
- [ ] Analyse conterfactuals 

## Prerequisities

### Environment
Does this template work with a standard environment? If so, mention which environment is required. If not, please fill the sections below to indicate how a custom environment should be set up to use this template:

#### Base Image
Specify the base image for the custom environment. The base image should be publicly accessible. Domino should be able to download it without requiring credentials.

#### Dockerfile Instructions
Add Dockerfile instructions that a user will copy into the Dockerfile for their custom environment.

#### Workspace Tools
Specify which workspace IDEs are required for your project:
Jupyter
JupyterLab
VSCode
RStudio

### Hardware Requirements
Does this template require any specific hardware, such as GPUs? If so, mention the requirements in detail.

### Other prerequisities
Do any scripts need to be run after the project is created from the template? What are these scripts used for? Specify what each script does, and instructions for running it.
Please make sure that the scripts are all included in the source code of the project (the repo you are creating using this template).

## Usage Instructions
List step-by-step instructions for how to use a project created from this template

1. Run Notebook X.ipynb
2. Run Notebook Y.ipynb
3. Run script model.py
4. ...
5. ...

## Known issues
Document all the known issues with the repo in this section

## References
Any references you'd like to include go here.
