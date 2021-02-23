
class StorageError(Exception):
    pass


class Storage:
    def __init__(self, capacity):
        self.inventory = 0
        self.capacity = capacity
        if self.capacity < 0:
            raise StorageError
        self.storage_loss = 0
        self.check_inventory()

    def add_inventory(self, new_stock):
        self.inventory += new_stock
        self.check_inventory()

    def remove_inventory(self, request):
        if request <= self.inventory:
            self.inventory -= request
            self.check_inventory()
            return request
        else:
            available_inventory = self.inventory
            self.inventory = 0
            self.check_inventory()
            return available_inventory

    def check_inventory(self):
        if self.inventory > self.capacity:
            self.storage_loss += self.inventory - self.capacity
            self.inventory = self.capacity
        elif self.inventory < 0:
            raise StorageError
        else:
            pass

    def lose_inventory(self, loss_rate=0.05):
        lost_inventory = self.inventory * loss_rate
        self.storage_loss += lost_inventory
        self.inventory -= lost_inventory
        self.check_inventory()
