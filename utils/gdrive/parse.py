import os
import zipfile
import re
from bs4 import BeautifulSoup
import requests

def extract_zip(zip_path):
    directory = os.path.dirname(zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extract(member='pmn96cur.txt', path=directory)
        print(f"Extracted files to: {directory}")

def get_pdf_link(file_name):
    # Construct the URL  
    url = f"https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID={file_name}"  
    
    # Make the request  
    response = requests.get(url)  

    # Check if the request was successful  
    if response.status_code == 200:  
        # Parse the HTML content  
        soup = BeautifulSoup(response.text, 'html.parser')  

        # Find all 'a' tags  
        links = soup.find_all('a', href=True)  

        # Iterate over the links to find the 'Summary' link  
        for link in links:  
            # Check if the link text is 'Summary'  
            if 'Summary' in link.text:  
                return link['href']  # Return the href link  

        # If no 'Summary' link is found  
        return None  
    else:  
        # If the request was not successful  
        print(f"Failed to retrieve the page. Status code: {response.status_code}")  
        return None

def parse_pdf_id(file_path):
    # Regular expression to find K-numbers (K followed by 6 digits)  
    k_number_pattern = re.compile(r'\bK\d{6}\b')  

    # Open and read the file  
    with open(file_path, 'r') as file:  
        content = file.read()  

    # Find all K-numbers in the content  
    k_numbers = k_number_pattern.findall(content)  

    return k_numbers