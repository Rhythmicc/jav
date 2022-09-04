import os
import pickle
from .. import config

wish_list_path = config.select('wish_list_path')

class WishList:
    def __init__(self):
        if os.path.exists(wish_list_path):
            with open(wish_list_path, 'rb') as f:
                self.items = pickle.load(f)
        else:
            self.items = {}

    def add(self, item):
        if item['designation'] not in self.items:
            self.items[item['designation']] = item
        else:
            from .. import _ask
            if _ask({
                'type': 'confirm',
                'name': 'confirm',
                'message': f'已存在 {item["designation"]}，是否覆盖?',
                'default': False
            }):
                self.items[item['designation']] = item

    def remove(self, item):
        self.items.pop(item['designation'])
    
    def get_list(self):
        return self.items
    
    def store(self):
        with open(wish_list_path, 'wb') as f:
            pickle.dump(self.items, f)
