class Item:
    """
    Class that represents an item in the inventory tracking system

    Instance Attributes:
        - name: name of the type of item stored in the inventory
        - id: unique id associated with the item
    """
    __name: str
    __id: str

    def __init__(self, name: str, id: str):
        """
        Initializes an instance of Item

        :param name: name of item
        :param id: unique id associated with item
        """
        self.__name = name
        self.__id = id

    def get_name(self) -> str:
        """Returns the name of the item"""
        return self.__name

    def get_id(self) -> str:
        """Returns the number of items in the inventory"""
        return self.__id

    def is_same_item(self, other_id) -> bool:
        "Compares the id of the item with other_id and returns true if the two are the same"
        return self.__id == other_id


