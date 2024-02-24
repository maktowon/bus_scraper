class BusScraperException(Exception):
    """Base class for all errors"""


class InvalidLongitudeException(BusScraperException):
    def __init__(self, longitude: float, message: str = "Longitute is not in (-180, 180) range."):
        self.longitude = longitude
        self.message = message
        super().__init__(self.message)


class InvalidLatitudeException(BusScraperException):
    def __init__(self, latitude: float, message: str = "Latitude is not in (-90, 90) range."):
        self.latitude = latitude
        self.message = message
        super().__init__(self.message)


class FetchingDataApiException(BusScraperException):
    def __init__(self, url: str, status_code: int, message: str = ""):
        self.url = url
        self.status_code = status_code
        if not message:
            self.message = f"Error fetching data from {url}, status: {status_code}"
        else:
            self.message = message


class FileNotExistsException(BusScraperException):
    def __init__(self, file_path: str, message: str = "File does not exist."):
        self.file_path = file_path
        self.message = message
        super().__init__(self.message)
