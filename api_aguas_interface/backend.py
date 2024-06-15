from api_aguas_interface.access_handler import Access
from api_aguas_interface.utils import get_image, get_image_paths
import requests
import json 

from urllib.parse import urljoin
import os
from api_aguas_interface.logger_config import logger  # Import the logger from the logger_config module

class GenerateReport:
    def __init__(self, endpoint, username, password):
        try:
            self.endpoint = endpoint
            self.check_endpoint_validity()
            self.access = Access(endpoint, username, password)
            self.id_inspection = None
            self.id_report = None
            logger.info("GenerateReport class initialized")
        except Exception as e:
            logger.error(f"Failed to initialize GenerateReport class: {e}")
            raise  # Propaga la excepción a la capa superior
    
    def check_endpoint_validity(self):
        try:
            response = requests.get(self.endpoint)
            response.raise_for_status()  # Esto lanzará una excepción si la respuesta no es exitosa (código de estado 2xx)
            logger.info(f"Endpoint {self.endpoint} is valid")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to access endpoint {self.endpoint}: {e}")
            raise  # Propaga la excepción a la capa superior

    def _get_header(self):
        try:
            header = {'Authorization': f"Bearer {self.access()}"}
            logger.debug(f"Generated header: {header}")
            return header
        except Exception as e:
            logger.error(f"Failed to get header: {e}")
            raise  # Propaga la excepción a la capa superior
    
    def _request(self, extension, data=None, files=None, method='POST'):
        try:
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
            response.raise_for_status()  # Raise an HTTPError for bad responses

            logger.debug(f"Response: {response}")
            if method != 'DELETE':
                response_data = response.json()
                logger.debug(f"Response data: {response_data}")
                return response_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise  # Propaga la excepción a la capa superior
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse response: {e}")
            raise  # Propaga la excepción a la capa superior

    def create_inspection(self, payload):
        try:
            data = self._request("inspection/", data=payload)
            self.id_inspection = data['pk']
            logger.info(f"Inspection created with ID: {self.id_inspection}")
            return data 
        except Exception as e:
            logger.error(f"Failed to create inspection: {e}")
            raise  # Propaga la excepción a la capa superior

    def delete_inspection(self):
        try:
            if self.id_inspection is not None:
                self._request(f"inspection/{self.id_inspection}/", method='DELETE')
                logger.info(f"Inspection with ID: {self.id_inspection} deleted")
                self.id_inspection = None
        except Exception as e:
            logger.error(f"Failed to delete inspection: {e}")
            raise  # Propaga la excepción a la capa superior

    def load_image(self, path_image):
        try:
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
        except Exception as e:
            logger.error(f"Failed to load image: {e}")
            self.delete_inspection()  # Delete the inspection if image loading fails
            raise  # Propaga la excepción a la capa superior

    def load_folder(self, folder):
        try:
            image_paths = get_image_paths(folder)
            if len(image_paths) == 0:
                raise ValueError(f"No images were found in the folder {folder}")
            
            for image_path in image_paths:
                self.load_image(image_path)
                logger.debug(f"Image loaded from path: {image_path}")
        except Exception as e:
            logger.error(f"Failed to load folder: {e}")
            self.delete_inspection()  # Delete the inspection if folder loading fails
            raise  # Propaga la excepción a la capa superior
    
    def generate_report(self):
        try:
            payload = {'inspection': self.id_inspection}
            data = self._request("report/", data=payload)
            self.id_report = data['pk']
            logger.info(f"Report generated with ID: {self.id_report}")
            return data
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            self.delete_inspection()  # Delete the inspection if report generation fails
            raise  # Propaga la excepción a la capa superior

    def download_report(self):
        try:
            data = self._request(f"report/{self.id_report}", method="GET")
            pdf_url = data['pdf_report']
            logger.info(f"Report downloaded from URL: {pdf_url}")
            return pdf_url
        except Exception as e:
            logger.error(f"Failed to download report: {e}")
            raise  # Propaga la excepción a la capa superior