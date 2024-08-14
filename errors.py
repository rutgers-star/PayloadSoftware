class ERR(Exception):
    types = []
    def __init__(self, number):
        super().__init__(number)

raise ERR(101)