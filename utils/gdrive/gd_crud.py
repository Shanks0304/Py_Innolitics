import os  
from pathlib import Path  
from google.oauth2 import service_account  
from googleapiclient.discovery import build  
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload

class GoogleDriveBase:  
    """  
    Base class for handling Google Drive operations.  
    """  
    def __init__(self, service_account_file):  
        self.service_account_file = service_account_file  
        self.scopes = ['https://www.googleapis.com/auth/drive']  
        self.credentials = service_account.Credentials.from_service_account_file(  
            self.service_account_file, scopes=self.scopes  
        )  
        self.service = build('drive', 'v3', credentials=self.credentials)  

    def list_files(self, query=None):  
        """List files matching a query."""  
        results = self.service.files().list(q=query, fields="files(id, name, mimeType)").execute()  
        return results.get('files', [])  

class GoogleDriveFolderManager(GoogleDriveBase):  
    """  
    Derived class for managing folders in Google Drive.  
    """  
    def create_folder(self, parent_id, folder_name):  
        file_metadata = {  
            'name': folder_name,  
            'mimeType': 'application/vnd.google-apps.folder',  
            'parents': [parent_id]  
        }  
        folder = self.service.files().create(body=file_metadata, fields='id').execute()  
        print(f'Created folder ID: {folder.get("id")}')  
        return folder.get("id")  

    def retrieve_folder_by_name(self, name):  
        query = f"mimeType='application/vnd.google-apps.folder' and name='{name}'"  
        return self.list_files(query)  

    def list_all_folders(self):  
        query = "mimeType='application/vnd.google-apps.folder'"  
        return self.list_files(query)  

    def delete_folder_by_id(self, folder_id):  
        self.service.files().delete(fileId=folder_id).execute()  
        print(f'Deleted folder ID: {folder_id}')

class GoogleDriveFileManager(GoogleDriveBase):  
    """  
    Derived class for managing files in Google Drive.  
    """  
    def create_file(self, folder_id, file_name, file_stream):  
        # Check if the file already exists in the folder
        existing_files = self.list_files_in_folder(folder_id)
        print(existing_files)
        if any(f['name'] == file_name for f in existing_files):
            print(f"File {file_name} already exists in Google Drive. Skipping upload.")
            return None

        file_metadata = {'name': file_name, 'parents': [folder_id]}
        media = MediaIoBaseUpload(file_stream, mimetype='application/pdf', resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'Uploaded file ID: {file.get("id")}')
        return file.get("id")  

    def retrieve_file_by_name(self, name):  
        query = f"mimeType != 'application/vnd.google-apps.folder' and name='{name}'"  
        return self.list_files(query)  

    def list_all_files(self):  
        query = "mimeType != 'application/vnd.google-apps.folder'"  
        return self.list_files(query)  

    def list_files_in_folder(self, folder_id):  
        query = f"'{folder_id}' in parents"  
        return self.list_files(query)  

    def delete_file_by_id(self, file_id):  
        self.service.files().delete(fileId=file_id).execute()  
        print(f'Deleted file ID: {file_id}')  
