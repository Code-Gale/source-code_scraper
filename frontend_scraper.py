import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

# Function to create a folder if it doesn't exist
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Function to save content to a file
def save_to_file(content, file_path):
    with open(file_path, 'wb') as file:
        file.write(content)

# Function to download resources like stylesheets and scripts
def download_resource(url, base_url, folder_name):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            file_name = os.path.join(folder_name, os.path.basename(urlparse(url).path))
            save_to_file(response.content, file_name)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Ask the user for the parent folder name
parent_folder = input("Enter the name to save the parent folder as: ")
create_folder(parent_folder)

# Ask the user for the URL to scrape
website_url = input("Enter the URL of the website to scrape: ")

# Create a folder to save the website content
output_folder = os.path.join(parent_folder, "website_content")
create_folder(output_folder)

# Fetch the webpage
response = requests.get(website_url)

if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Save the main HTML content
    save_to_file(response.content, os.path.join(output_folder, "index.html"))

    # Find and download external resources (CSS and JS)
    for link in soup.find_all(['link', 'script']):
        if link.has_attr('href') or link.has_attr('src'):
            resource_url = link.get('href') or link.get('src')
            absolute_url = urljoin(website_url, resource_url)
            download_folder = "CSS" if resource_url.endswith('.css') else "JS" if resource_url.endswith('.js') else "Other"
            create_folder(os.path.join(output_folder, download_folder))
            download_resource(absolute_url, website_url, os.path.join(output_folder, download_folder))

    print(f"Website content has been scraped and saved in the '{parent_folder}' folder.")
else:
    print(f"Failed to fetch {website_url}. Status code: {response.status_code}")
