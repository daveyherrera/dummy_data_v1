import random
import sys
sys.path.insert(0,'/Users/davey.herrera/Documents/BBDN-dummy-data-python/BBDN-dummy-data-python/')

from local_deployment.learn_api_explorer.data_handler import Data
from local_deployment.learn_api_explorer.global_util import read_file_return_json, dummy_courses_location, config_location, write_file_json


class CourseMemberships(Data):
    def __init__(self):
        self.type_of_data = "memberships"
        self.membership_endpoint = "/learn/api/public/v1/courses/{courseId}/users/{userId}"
        self.read_users_endpoint = "/learn/api/public/v1/users"
        self.read_courses_endpoint = "/learn/api/public/v3/courses"
        self.dummy_users_created = self.read_data(endpoint=self.read_users_endpoint)
        self.dummy_courses_created = self.read_data(endpoint=self.read_courses_endpoint)
        super().__init__("", "", True, "")

    def __str__(self) -> str:
        return super().__str__()
    

read_users = CourseMemberships()
print(read_users.dummy_users_created)


