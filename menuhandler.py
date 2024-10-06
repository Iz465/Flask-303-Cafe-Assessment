from enum import Enum
from operator import itemgetter
class Sort(Enum):
    NAME = 1
    PRICE = 2

class MenuHandler():
    def __init__(self, data_dict):
        self.data = data_dict
    def sorteddata(self):
        sorted_list = sorted(self.data, key=itemgetter('title'))
        return sorted_list