import urllib.request
import json
import device_check as device
import datetime

# device calls utilites and api gen calls device

class LearnJsonApiGenerator(device.Device):
    def __init__(self) -> None:
        # The constructor super() is required to access the parent class, we need to first call it in order to have access to the init values of the inherited class
        super().__init__()
        # I really do hope this swagger url is never updated, if it is, here is where the new swagger url json file should be placed
        self.learn_swagger_url = "http://devportal-docstore.s3.amazonaws.com/learn-swagger.json"
        self.swagger_file_name = self.curr_path + "/" + "swagger.json"
        self.path_swagger_json = self.curr_path + "/" + "path_swagger.json"
        self.swagger_last_update_file_name = self.curr_path + "/" + "swagger_last_update.json"
        self.path_to_swagger_file = self.curr_path + "/" + self.swagger_file_name
        self.swagger_file = ""
        self.swagger_learn_api_version = ""
        self.swagger_available_http_methods = ["get", "post", "patch", "put", "delete"]
        self.swagger_latest_version = ""
        self.minimal_requirements = self.validate_device()
        if not self.minimal_requirements:
            raise Exception("The device does not meet the minimal requirements to run this script")
        
    def is_swagger_file_up_to_date(self):
        if self.file_exists(self.swagger_last_update_file_name):
            swagger_last_update = self.date_converter(self.read_file_return_json(self.swagger_last_update_file_name)['date'], 'date')
            if self.today > swagger_last_update:
                print("Swagger was downloaded before today")
                return False
            else:
                print("No new swagger is needed")
                return True
        else:
            print("file does not exist")
            return False
        
    def download_swagger_json_file(self):
        try:
            urllib.request.urlretrieve(self.learn_swagger_url, self.swagger_file_name)
            with open(self.swagger_file_name, "r") as f:
                swagger = f.read()
                swagger = json.loads(swagger)
                self.swagger_learn_api_version = swagger["info"]["version"]
                self.swagger_file = swagger
                # Actualizar la fecha
                self.write_file(self.swagger_last_update_file_name, json.dumps({"date": str(self.today)}))
                print("New swagger downloaded")
                return True
        except urllib.error.URLError:
            print("There was an error downloading the swagger file")
            return False


    def create_new_swagger(self):
        try:
            path_to_summary = {}
            for path in self.swagger_file["paths"]:
                for method in self.swagger_available_http_methods:
                    if method in self.swagger_file["paths"][path]:
                        if 'deprecated' not in self.swagger_file["paths"][path][method].keys():
                            path_to_summary.update(
                                {
                                    self.swagger_file["paths"][path][method]["summary"]:{
                                            "method": method,
                                            "path": path
                                    }
                                })
            self.write_file_json(self.path_swagger_json , path_to_summary)
            print("New swagger created")
            return True
        except KeyError:
            print("There was an error processing the swagger file")
            return False
    
    # Main function
    def swagger_generator_main(self):
        if self.is_swagger_file_up_to_date():
            return True
        else:
            print("Downloading new swagger")
            self.download_swagger_json_file()
            return False
            
                        
if __name__ == "__main__":
    new_swagger = LearnJsonApiGenerator()
    new_swagger.swagger_generator_main()