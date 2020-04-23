class Person:
    """
    Represents a person, holds name, socket client and IP address
    """
    def __init(self, addr, client):
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self, name):
        """

        :return
        """
        self.name = name

    def __repr__(self):
        return f"Person({self.addr},{self.name}"
