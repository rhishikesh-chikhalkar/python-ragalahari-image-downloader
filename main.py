import os
import sys

import requests
from bs4 import BeautifulSoup


def download_image(image_url, save_directory):
    # Send an HTTP request to get the image data
    response = requests.get(image_url)
    if response.status_code == 200:
        # Get the file name from the URL
        file_name = image_url.split('/')[-1]

        # Combine the file name with the save directory to get the full file path
        file_path = os.path.join(save_directory, file_name)

        # Save the image to the specified directory
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Image '{file_name}' downloaded successfully.")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


def is_folder_empty(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    # Get the list of files and directories in the folder
    items = os.listdir(folder_path)

    # Check if the list is empty
    return len(items) == 0


def main():
    root_url = sys.argv[1]

    folder_name = root_url.split('/')[-1].removesuffix('aspx')
    save_directory = os.path.join(r'D:\UDEMY_Workspace\__downloads\_images', folder_name)
    if is_folder_empty(save_directory):
        print(f"folder path is empty, you can save the files.")
    else:
        raise Exception(f"Folder path not empty: {save_directory}")

    result = requests.get(root_url)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    # print(soup.prettify())

    # Pagination
    pagination = soup.find('td', id='pagingCell')
    pages = pagination.find_all('a')
    last_page = len(pages)

    for page in range(0, last_page):
        if page == 0:
            page_url = root_url
        else:
            page_url = root_url.replace(f"{root_url.split('/')[-1]}", f"{page}/{root_url.split('/')[-1]}")

        result = requests.get(page_url)
        content = result.text
        soup = BeautifulSoup(content, 'lxml')
        anchor_links = soup.find_all('a', href=True)
        href_links = []
        img_links = []
        for link in anchor_links:
            href_link = link['href']
            if href_link.startswith('/actress/'):
                img_tag = link.find('img')
                if img_tag:
                    img_link = img_tag['src']
                    img_links.append(img_link.replace('t.jpg', '.jpg'))
            href_links.append(href_link)

        for img_link in img_links:
            try:
                download_image(image_url=img_link, save_directory=save_directory)
            except Exception as E:
                print(f"Exception: {E}")
                continue
    print('completed.')


if __name__ == '__main__':
    main()
