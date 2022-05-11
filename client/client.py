from urllib import request
from bs4 import BeautifulSoup
from tqdm import tqdm
from glob import glob
import requests
import os
import shutil


class Client:
    def __init__(self, file_server_url: str):
        self.__file_server_url = file_server_url

    def _get_files_in_file_server(self) -> list:
        """
        Get the files in the file server
        :return: **list** of files in that particular directory
        """
        with request.urlopen(self.__file_server_url) as response:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            result = soup.findAll("a")
            files = [x.text for x in result if 'firmware' in str(x).lower()]
        return files

    def check_new_firmware_version(self, installed_firmware_version: str, download=False) -> str:
        """
        Check for new version of firmware is available or not in the file server
        :param installed_firmware_version: **str** current firmware version installed
        :param download: **bool** new firmware should be downloaded or not
        :return: **str** firmware download path or firmware name if available
        """
        files_in_server = self._get_files_in_file_server()
        new_version_avl = installed_firmware_version not in files_in_server[-1]
        file_name_in_server = files_in_server[-1] if new_version_avl else ''
        if file_name_in_server:
            if download:
                return self.download_file_from_file_server(file_name_in_server)
            return f'New firmware update available: {self.__file_server_url + file_name_in_server}'
        return 'Your firmware is up-to-date'

    def download_file_from_file_server(self, file_name_in_server: str) -> str:
        """
        Download the firmware from the file server
        :param file_name_in_server: **str** file name present in the file server
        :return: **str** downloaded file path
        """
        file_path_in_server = self.__file_server_url + file_name_in_server

        with requests.get(file_path_in_server, stream=True) as r:
            # check header to get content length, in bytes
            total_length = int(r.headers.get("Content-Length"))

            # implement progress bar via tqdm
            with tqdm.wrapattr(r.raw, "read", total=total_length, desc="") as raw:
                # save the output to a file
                with open(os.path.basename(r.url), 'wb') as output:
                    shutil.copyfileobj(raw, output)

        return glob(os.getcwd() + os.sep + file_name_in_server)[0]
