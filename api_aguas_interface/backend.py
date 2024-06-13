from api_aguas_interface.access_handler import Access
from api_aguas_interface.utils import get_image, get_image_paths
import requests
import wget

from urllib.parse import urljoin
import os
from api_aguas_interface.logger_config import logger  # Import the logger from the logger_config module

class GenerateReport:
    def __init__(self, endpoint, username, password):
        self.access = Access(endpoint, username, password)
        self.endpoint = endpoint
        self.id_inspection = None
        self.id_report = None
        logger.info("GenerateReport class initialized")

    def _get_header(self):
        header = {'Authorization': f"Bearer {self.access()}"}
        logger.debug(f"Generated header: {header}")
        return header
    
    def _request(self, extension, data=None, files=None, method='POST'):
        headers = self._get_header()
        url = urljoin(self.endpoint, extension)
        logger.debug(f"Request URL: {url}, Method: {method}, Data: {data}, Files: {files}")

        # Choose HTTP method dynamically
        method = method.upper()
        if method not in {'GET', 'POST', 'PUT', 'DELETE'}:
            logger.error("Invalid HTTP method. Supported methods: GET, POST, PUT, DELETE")
            raise ValueError("Invalid HTTP method. Supported methods: GET, POST, PUT, DELETE")
        
        # Call the appropriate requests method dynamically
        request_method = getattr(requests, method.lower())
        response = request_method(url, headers=headers, data=data, files=files)

        logger.debug(f"Response: {response}")
        response_data = response.json()
        logger.debug(f"Response data: {response_data}")
        return response_data

    def create_inspection(self, payload):
        data = self._request("inspection/", data=payload)
        self.id_inspection = data['pk']
        logger.info(f"Inspection created with ID: {self.id_inspection}")
        return data 

    

    def load_image(self, path_image):
        file_ = get_image(path_image)
        name_image = file_[0][1][0]
        payload = {
            "name": name_image,
            "inspection": self.id_inspection,
            "position": int(os.path.splitext(name_image)[0]),
        }
        data = self._request("image/", data=payload, files=file_)
        logger.info(f"Image loaded: {name_image} for inspection ID: {self.id_inspection}")
        return data 

    def load_folder(self, folder):
        image_paths = get_image_paths(folder)
        for image_path in image_paths:
            self.load_image(image_path)
            logger.debug(f"Image loaded from path: {image_path}")
    
    def generate_report(self):
        payload = {'inspection': self.id_inspection}
        data = self._request("report/", data=payload)
        self.id_report = data['pk']
        logger.info(f"Report generated with ID: {self.id_report}")
        return data

    def download_report(self):
        data = self._request(f"report/{self.id_report}", method="GET")
        pdf_url = data['pdf_report']
        wget.download(pdf_url)
        logger.info(f"Report downloaded from URL: {pdf_url}")
        return pdf_url
