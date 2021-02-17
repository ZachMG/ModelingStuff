class Producer:
    def __init__(self, name, p_rate=1):
        self.name = name

        self.production_rate = p_rate
        self.sales = 0
        self.total_production = 0

        self.inventory = 0
        self.lost_inventory = 0
        self.total_losses = 0

        self.storage = None

    def produce_object(self):
        self.total_production += self.production_rate
        self.inventory += 1

    def track_sales(self, sold=False):
        if sold is True and self.inventory >= 1:
            self.sales += 1
            self.inventory -= 1
        else:
            pass

    def clear_inventory(self):
        if self.storage is None:
            self.lost_inventory += self.inventory
            self.inventory = 0
        if self.storage is not None:
            self.store_inventory(self.inventory)

    def add_storage(self, storage):
        self.storage = storage

    def store_inventory(self, inventory):
        self.storage.add_inventory(inventory)

    def request_inventory(self, request):
        self.inventory += self.storage.remove_inventory(request)

    def upgrade_storage(self, increase_cap):
        self.storage.capacity += increase_cap

    def update_losses(self):
        self.total_losses = self.lost_inventory + self.storage.storage_loss
