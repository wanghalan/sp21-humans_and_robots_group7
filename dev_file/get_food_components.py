import os
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from decouple import config

'''
Reference:
    https://github.com/Clarifai/clarifai-python/blob/master/README.md
'''


def get_food_results(path, local_file=True):
    # can check https://www.clarifai.com/models/ai-food-recognition
    results = None
    app = ClarifaiApp(api_key=config('CLARIFAI_API_KEY'))
    model = app.models.get('food-items-v1.0')
    if local_file:
        response = model.predict_by_filename(path)
    else:
        response = model.predict_by_url(path)
    # print('results: %s' % results)

    for each in response['outputs'][0]['data']['concepts']:
        print(each['name'], ' ', each['value'])
    return response


if __name__ == '__main__':
    r = get_food_results('https://www.applesfromny.com/wp-content/uploads/2020/05/Jonagold_NYAS-Apples2.png', False)
    print('-'*80)
    r = get_food_results('./img/apple.jpg')
