
from operator import itemgetter

class MenuHandler():
    def sorteddata(self,data, method_sort):
        sorted_list = data
        if method_sort == "name":
            sorted_list = sorted(data, key=itemgetter('title'))
        elif method_sort == "price":
            sorted_list = sorted(data, key=itemgetter('price'))
        return sorted_list
    def searchdata(self,data, search_value):
        datalist = []
        for item in data:
            if search_value.upper() in item["title"].upper():
                print(item["title"])
                datalist.append(item)
        return datalist