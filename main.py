import csv
import os
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin

def scrape_data_and_download_images(url, download_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        
        links = soup.find_all('a')
        hrefs = [link.get('href') for link in links if link.get('href') is not None and re.match('https://lenouvelliste.com/', link.get('href'))]

        
        p_tags = soup.find_all('p')
        paragraphs = [p.text for p in p_tags]

        
        images = soup.find_all('img', src=True)
        image_sources = [urljoin(url, image['src']) for image in images]

        
        with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Link', 'Paragraph Text', 'Image Source'])

            
            for link, paragraph, image_source in zip(hrefs, paragraphs, image_sources):
                csv_writer.writerow([link, paragraph, image_source])

       
        download_images(image_sources, download_path)

        print("Data and images saved successfully.")
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")

def download_images(image_sources, download_path):
    for i, source in enumerate(image_sources):
        try:
            response = requests.get(source, stream=True)
            response.raise_for_status()

            # Extracting the filename from the URL
            filename = os.path.join(download_path, f"image_{i+1}.jpg")

            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"Image downloaded: {filename}")
        except requests.RequestException as e:
            print(f"Error downloading image from {source}: {e}")

def main():
    url = "https://lenouvelliste.com/"
    script_directory = os.path.dirname(os.path.realpath(__file__))
    download_path = os.path.join(script_directory, "images")

    scrape_data_and_download_images(url, download_path)

if __name__ == "__main__":
    main()
