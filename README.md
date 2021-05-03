## Declaration
Group 7
Team Members: Chang Feng-Yi, Ma, Jiachen, Wang Alan

Our project is about the construction of food serving robot, and more details related to the motivation, experimental design and analysis method could be found in our report. 

Here, we will focus on going through the navigation of the operation. This is the final version for the design of our robotic system based on the NAO robot. 


Also, we feel really thanksful for those who provide third-party open sources so that we can refer to some client APIs or SDKs for better completing the functional system in our project. We will mention and credit them in the process of the description.

## Outline
* An Overview of Program Structure in Github
* Env Setup 
* Nao Robot Operating System for HRI Design
* NAOqi Python SDK 
* Clarifai Python API for Food Recognition
* Food Calorie Predictor by using Web Crawler
* Online AI Modeling Resources for Face Prediction 

## An Overview of Program Structure in Github
Overall, there are few files that we need to look at. We will illustrate the min detail in the following sections.

* project_CRG / Nao_Advance.crg
```
Nao Robot Operating System for HRI Design
```
* nao_advance_serve.py 
    
    *  dev_file / videoInput_getImage.py (submodule 1)
    *  food.py (submodule 2 & 3)
    *  face_prediction.py (submodule 4)
```
Main Program for integrating submodules, list below

1. NAOqi Python SDK for retrieving image from NAO camera

2. Clarifai python API for food recognition based on image

3. Food calorie predictor by using web crawler based on food recognition

4. AI training modeling for face prediction based on image
```
* analyzer.py
```
Main Program for reporting time stamps during HRI interaction and save them
