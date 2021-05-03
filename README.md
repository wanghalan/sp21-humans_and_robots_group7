## Declaration
Group 7
Team Members: Chang Feng-Yi (fc4wa), Ma, Jiachen (jm7gz), Wang Alan (ahw9f)

Our project is about the construction of food serving robot, and more details related to the motivation, experimental design and analysis method could be found in our report. 

Here, we will focus on going through the navigation of the operation. This is the final version for the design of our robotic system based on the NAO robot. 


Also, we feel really thanksful for those who provide third-party open sources so that we can refer to some client APIs or SDKs for better completing the functional system in our project. We will mention and credit them in the process of the description.

## Outline
* An Overview of Program Structure in Github
* Env Setup 
* Nao Robot Operating System for HRI Design
* [NAOqi Python SDK](http://doc.aldebaran.com/2-8/dev/python/install_guide.html#python-install-guide)
* [Clarifai Python API for Food Recognition](https://github.com/Clarifai/clarifai-python)
* Food Calorie Predictor by using Web Crawler
* [Online AI Modeling Resources for Face Prediction](https://towardsdatascience.com/real-time-age-gender-and-emotion-prediction-from-webcam-with-keras-and-opencv-bde6220d60a)

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
```
* data_ref / final_analysis.ipynb
```
Analysis method implementation based on experimental raw data (analyzer.py).
```

## Env Setup
1. PC Operating System：Mac Pro
2. Python 2.7 & Python 3.6
```
Python 2.7 : NAOqi Python SDK 

Python 3.6： pip install -r requirements.txt
```

## Nao Robot Operating System for HRI Design
* project_CRG / Nao_Advance.crg

We can refer to the interaction logic in the follwoing path. Theoretically, the NAO will start the interaction process with humans by following the procedures shown in 'logic_timeStamp.jpeg'. 

* data_ref / logic_timeStamp / logic_timeStamp.jpeg


Particulartly, the file  analyzer.py will note some time stamps and save them as data for our further analysis.


## NAOqi Python SDK
```
Save image from NAO to local computer
```
With the help of NAOqi Python SDK, we are able to better make our computer to getData, insertData, and RemoveData from NAO robot. 
* nao_advance_serve.py
    * dev_file / videoInput_getImage.py
    
        * This file is to get the image from the Nao camrea, then save the image to the local computer for food recognition or face prediction based on the needs.

## Clarifai Python API for Food Recognition
```
Food recognition based on the image
```
* nao_advance_serve.py
    * food.py (first part)

        * Call Clarifai Python API for AI training based on the food image, the output would be the list of possible ingredients of the food.

## Food Calorie Predictor by using Web Crawler
```
Calculation of food calorie based on food recognition
```
* nao_advance_serve.py
    * food.py (last part)

        * Next, we calculate the total calorie of food by  web crawling the calorie of each food ingredients.


## Online AI Modeling Resources for Face Prediction
```
Obtain gender, age, and emotion of a person based on facial recognition
```
* nao_advance_serve.py

    * face_prediction.py 

        * This program will get the image of person based on NAO cameara. Then feed the image into face AI traning model with the help of modeling open sources dataset. As the result, the output would be gender, age, and emotion of a person based on the facial image.

        * The pre-trained models can be downloaded from [here](https://drive.google.com/file/d/1NvushEV_jqOcjT2zDv0CmUX-XJXJ7Epy/view)
