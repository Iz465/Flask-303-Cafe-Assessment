
from operator import itemgetter

class MenuHandler():
    def __init__(self, data_dict):
        self.data = data_dict
    def sorteddata(self, method_sort):
        sorted_list =[]
        if method_sort == "name":
            sorted_list = sorted(self.data, key=itemgetter('title'))
        elif method_sort == "price":
            sorted_list = sorted(self.data, key=itemgetter('price'))
        return sorted_list
    def searchdata(self, search_value):
        datalist = []
        for item in self.data:
            if search_value.upper() in item["title"].upper():
                datalist.append(item)
        return datalist