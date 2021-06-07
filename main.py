import requests
import json
import os
from PIL import Image
from io import open
from dotenv import load_dotenv



spacex_launch_data_url = 'https://api.spacexdata.com/v3/launches/64'
hubble_image_data_url = 'http://hubblesite.org/api/v3/images/spacecraft?page=all'


def load_spacex_pictures(spacex_launch_data_url):
    response = requests.get(spacex_launch_data_url)
    response.raise_for_status
    launch_data = json.loads(response.text)
    flickr_links = launch_data['links']['flickr_images'][:]
    for iteration_index, picture_link in enumerate(flickr_links):
        response = requests.get(picture_link)
        response.raise_for_status()
        spacex_picture_extension = get_picture_extension(picture_link)
        filename = os.path.join('images', f'spacex_image_{iteration_index}{spacex_picture_extension}')
        with open(filename, 'wb') as file:
            file.write(response.content)


def get_picture_extension(picture_link):
    _, extension = os.path.splitext(picture_link)
    return extension


def get_hubble_image_ids(hubble_image_data_url):
    response = requests.get(hubble_image_data_url)
    response.raise_for_status
    hubble_image_data = response.json()
    for hubble_picture_info in hubble_image_data:
        hubble_picture_id = hubble_picture_info['id']
        picture_ids_for_naming = []
        picture_ids_for_naming.append(hubble_picture_id)

    return picture_ids_for_naming


def load_hubble_pictures(picture_ids_for_naming):
    for hubble_picture_id in picture_ids_for_naming:
        hubble_image_url = f'http://hubblesite.org/api/v3/image/{hubble_picture_id}'
        response = requests.get(hubble_image_url)
        response.raise_for_status()
        main_part_of_download_url = response.json()['image_files'][-1]['file_url']
        image_download_url = f'https:{main_part_of_download_url}'
        response = requests.get(image_download_url, verify=False)
        response.raise_for_status()
        hubble_picture_extension = get_picture_extension(image_download_url)
        for picture_number, id in enumerate(picture_ids_for_naming):
            filename = f'images/hubble_image_{picture_number}{hubble_picture_extension}'
            with open(filename, 'wb') as file:
                file.write(response.content)


def crop_image():
    pics_dir = 'images'
    for filename in os.listdir(pics_dir):
        image = Image.open(f'{pics_dir}/{filename}')
        if image.width > 1080 or image.height > 1080:
            image.thumbnail((1080, 1080))
            image.save(f'{pics_dir}/{filename}')
        else:
            image.save(f'{pics_dir}/{filename}')
            pass


if __name__ == '__main__':
    load_dotenv()
    hubble_image_ids = get_hubble_image_ids(hubble_image_data_url)
    load_spacex_pictures(spacex_launch_data_url)
    load_hubble_pictures(hubble_image_ids)
    crop_image()