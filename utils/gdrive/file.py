import io
import os
import requests
from utils.gdrive.gd_crud import GoogleDriveFileManager
from utils.gdrive.parse import extract_zip, get_pdf_link, parse_pdf_id

def download_list() -> list[str]:
    url = "https://www.accessdata.fda.gov/premarket/ftparea/pmn96cur.zip"

    # Send a HTTP GET request to the URL  
    response = requests.get(url)  
        
    # Check if the request was successful 
    if response.status_code == 200:  
        with open('pmn96cur.zip', 'wb') as temp_file:  
            temp_file.write(response.content)  
        print(f"PDF downloaded to temporary file")
        extract_zip(os.path.abspath('pmn96cur.zip'))
        results = parse_pdf_id(os.path.abspath('pmn96cur.txt'))
        return results
    else:  
        print(f"Failed to download PDF. Status code: {response.status_code}")
        return []

def download_and_upload_pdf(file_name: str, folder_id: str, gdrive_file_manager: GoogleDriveFileManager):   
    url = get_pdf_link(file_name)
    print(url)
    if url is None:
        print(f"There is no summary of {file_name}")
    else:
        # Download directly to memory
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_stream = io.BytesIO(response.content)
            # Upload to Google Drive  
            gdrive_file_manager.create_file(folder_id, file_name + '.pdf', file_stream)
        else:
            print(f"Failed to download from {url}. Status code: {response.status_code}")

def process_files_concurrently(filename_list, folder_id, gdrive_manager):
    for filename in filename_list:
        try:
            print("Start processing")
            download_and_upload_pdf(filename, folder_id, gdrive_manager)
        except Exception as error:
            print(f"Error processing {error}")
    # with ThreadPoolExecutor(max_workers=max_workers) as executor:
    #     futures = {executor.submit(download_and_upload_pdf, filename, folder_id, gdrive_manager): filename for filename in filename_list}
    #     for future in as_completed(futures):
    #         try:
    #             future.result()
    #             print("Start processing")
    #         except Exception as e:
    #             print(f"Error processing {futures[future]}: {e}")