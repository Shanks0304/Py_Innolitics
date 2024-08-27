import os
from utils.gdrive.gd_crud import GoogleDriveFolderManager, GoogleDriveFileManager
from utils.gdrive.file import download_list, process_files_concurrently


if __name__ == '__main__':
    # Connect Google Drive
    service_account_file = 'gd_credential.json'
    folder_manager = GoogleDriveFolderManager(service_account_file)
    file_manager = GoogleDriveFileManager(service_account_file)

    # Get the destination folder id
    folder_id = folder_manager.retrieve_folder_by_name("test_FDA")[0].get('id')


    pdf_file_names = download_list()[200:220]
    process_files_concurrently(pdf_file_names, folder_id, file_manager)
    os.remove(os.path.abspath('pmn96cur.zip'))