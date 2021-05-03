# sp_21_nao
## Declaration
Group 7
Team Members: Chang Feng-Yi, Ma, Jiachen, Wang Alan

Our project is about the construction of food serving robot, and more details related to the motivation and experimental design and analysis method could be found in our report. 

Here, we will focus on going through the navigation of the operation. This is the final version for the design of our robotic system based on the NAO robot. 


Also, we feel really thanksful for those who provide third-party open sources so that we can refer to some client APIs or SDKs for better completing the functional system in our project. We will mention them in the process of the description.

## Outline
* An Overview of Program Structure in Github
* Env Setup 
* Nao Robot Operating System for HRI Design
* NAOqi Python SDK 
* Clarifai Python API for Food Recognition
* Food Calorie Predictor by using Web Crawler
* Online AL Modeling Resources for Face Prediction 

## An Overview of Program Structure in Github



Currently, there are two files that we need to look at.

### Save image from NAO to local computer
- videoInput_getImage.py: This file is to get the image from the Nao camrea, then save the image to the local computer.
- bot_final/final2.py: Mainly start from line 155, the url link of the imgur image will be thrown to Clarfifai API. 

### Next, we will get the list which shows the ingredients from the food image.
- get_food_components.py: Call the main function to see an example of how local and web-based images can be looked at through the lens of Clarifai

### Next, we calculate calorie of each ingredient with the help of web crawler.
