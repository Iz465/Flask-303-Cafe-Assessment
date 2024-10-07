
from operator import itemgetter

class MenuHandler():
    def __init__(self, data_dict):
        self.data = data_dict
    def sorteddata(self, method_sort):
        if method_sort == "name":
            sorted_list = sorted(self.data, key=itemgetter('title'))
        elif method_sort == "price":
            sorted_list = sorted(self.data, key=itemgetter('price'))
        return sorted_list