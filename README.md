# sp_21_nao

Currently, there are two files that we need to look at.

### Save image from NAO to local computer
- videoInput_getImage.py: This file is to get the image from the Nao camrea, then save the image to the local computer.
- bot_final/final2.py: Mainly start from line 155, the url link of the imgur image will be thrown to Clarfifai API. 

### Next, we will get the list which shows the ingredients from the food image.
- get_food_components.py: Call the main function to see an example of how local and web-based images can be looked at through the lens of Clarifai

### Next, we calculate calorie of each ingredient with the help of web crawler.
