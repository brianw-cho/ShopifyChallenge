from item import Item
import pandas as pd


class ExistingItemException(Exception):
    """
    Exception raised for attempting to create and add an item that already exists

    Attributes:
        - message: explanation of the error
    """

    def __init__(self, message="Item already exists in the inventory"):
        self.message = message
        super().__init__(self.message)

class NoSuchItemException(Exception):
    """
    Exception raised for attempting to access an item that does not exist

    Attributes:
        - message: explanation of the error
    """

    def __init__(self, message="Item does not exist in the inventory"):
        self.message = message
        super().__init__(self.message)


class ItemManager:
    """
    Class that manages items in the inventory

    Instance Attributes:
        - inventory: a dictionary mapping that maps an Item id to the number stored in the inventory
        - items: a dictionary mapping that maps an Item id to the Item object stored in the inventory
    """
    __inventory: dict
    __items: dict

    def __init__(self):
        self.__inventory = dict()
        self.__items = dict()

    # def __init__(self, inventory: dict):
    #     self.inventory = inventory
    #     self.items =

    def create_item(self, name: str, id: str, num: int = 0) -> None:
        """
        Creates a new item to store in the inventory. If an item with the same id already exists in the
        inventory, an ExistingItemException is raised.

        :param name: name of the item
        :param id: unique id of the item
        :param num: number of item to be stored in the inventory. 0 by default
        """
        if id in self.__inventory:
           raise ExistingItemException
        else:
            new_item = Item(name, id)
            self.__inventory[id] = num
            self.__items[id] = new_item

    def delete_item(self, id: str) -> None:
        """
        Deletes an existing item in the inventory with the given id. If an item with the given id does not
        exist, a NoSuchItemException is raised.

        :param id: id of the item to be removed
        """
        if id not in self.__inventory:
            raise NoSuchItemException
        else:
            del self.__inventory[id]
            del self.__items[id]

    def set_num(self, id: str, num: int) -> None:
        """
        Sets the recorded number of items stored in the inventory. If an item with the given id does not
        exist, a NoSuchItemException is raised.

        :param num: the new recorded number of items
        """
        if id not in self.__inventory:
            raise NoSuchItemException
        else:
            self.__inventory[id] = num

    def get_num(self, id: str) -> int:
        """
        Returns the number of the item with the given id in the inventory. Raises a NoSuchItemException
        if the item does not exist

        :param id: id of the item
        :return: number of items with the id in the inventory
        """
        if id in self.__inventory:
            return self.__inventory[id]
        else:
            raise NoSuchItemException

    def get_name(self, id: str) -> str:
        """
        Return the name of the item with the given id. Raises a NoSuchItemException
        if the item does not exist

        :param id: id of the item
        :return: name of the item with the id
        """
        if id in self.__inventory:
            return self.__items[id].get_name()
        else:
            raise NoSuchItemException

    def contains(self, id: str) -> bool:
        """
        Returns true if the item with the given id exists in the inventory.

        :param id: id of the item
        :return: True if item exists, otherwise False
        """
        return id in self.__inventory

    def to_dataframe(self) -> pd.DataFrame:
        """
        Returns the inventory as a dataframe

        :return: pandas dataframe that represents the inventory
        """
        names = {iden : self.__items[iden].get_name() for iden in self.__items}
        df = pd.DataFrame({"name":pd.Series(names), "num":pd.Series(self.__inventory)})
        return df