import os
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import ApiRequestError


class UploadClient:
    def __init__(self, source_path: str, dest: str, dest_id: Optional[str] = None):
        self.source_path = source_path
        self.dest = dest
        self.dest_id = dest_id
        self.drive = GoogleDrive(self._auth())

    def _auth(self):
        auth = GoogleAuth()
        auth.LocalWebserverAuth()
        return auth

    def _get_dest_id(self):
        dir_pool = []
        drive_content = self.drive.ListFile({"q": "trashed=false"}).GetList()
        for file in drive_content:
            if file['title'] == self.dest:
                dir_pool.append(file['id'])
        if dir_pool:
            dest_id = dir_pool[-1]
        else:
            gdrive_dir = self._make_dir(self.dest)
            dest_id = gdrive_dir['id']
        return dest_id

    def _make_dir(self, name: str):
        gdrive_dir = self.drive.CreateFile({
            'title': name,
            "mimeType": "application/vnd.google-apps.folder"
        })
        gdrive_dir.Upload()
        return gdrive_dir

    def _upload_file(self, file):
        file_path = os.path.join(self.source_path, file)
        try:
            f = self.drive.CreateFile({
                'title': file,
                "parents": [{"id": self.dest_id}]
            })
            f.SetContentFile(file_path)
            f.Upload()
        except ApiRequestError as exc:
            print(f'Failed to upload {file}. Error message: {exc}')

    def upload(self):
        self.dest_id = self.dest_id or self._get_dest_id()
        files = os.listdir(self.source_path)
        with ThreadPoolExecutor() as pool:
            pool.map(self._upload_file, files)
