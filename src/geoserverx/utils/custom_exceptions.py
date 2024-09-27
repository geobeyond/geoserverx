class GSModuleNotFound(Exception):
    def __init__(self, message="Module not found", status_code=412):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
