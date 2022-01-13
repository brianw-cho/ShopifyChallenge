import copy
from collections import deque
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

class MissingFieldsException(Exception):
    """
    Exception raised for calling a function with empty strings

    Attributes:
        - message: explanation of the error
    """

    def __init__(self, message="One or more of the fields are empty strings"):
        self.message = message
        super().__init__(self.message)



class ItemManager:
    """
    Class that manages items in the inventory

    Instance Attributes:
        - inventory: a dictionary mapping that maps an Item id to the number stored in the inventory
        - items: a dictionary mapping that maps an Item id to the Item object stored in the inventory
        - deleted: a stack of recently deleted items
    """
    __inventory: dict
    __items: dict
    __deleted: deque

    def __init__(self):
        self.__inventory = dict()
        self.__items = dict()
        self.__deleted = deque()

    def is_empty(self):
        """
        Returns whether the inventory is empty.

        :return: True if inventory is empty, False otherwise
        """
        return not self.__inventory

    def is_delete(self):
        """
        Returns whether there were recently deleted items

        :return: True if there were recently deleted items, False otherwise
        """
        return len(self.__deleted) != 0

    def create_item(self, name: str, id: str, num: int = 0) -> None:
        """
        Creates a new item to store in the inventory. If an item with the same id or name already exists in the
        inventory, an ExistingItemException is raised. If at least one of the fields is an empty string,
        a MissingFieldsException is raised.

        :param name: name of the item
        :param id: unique id of the item
        :param num: number of item to be stored in the inventory. 0 by default
        """
        if id in self.__inventory or name in {i.get_name() for i in self.__items.values()}: #TODO: test
            raise ExistingItemException
        elif name == '' or id == '':
            raise MissingFieldsException
        else:
            new_item = Item(name, id)
            self.__inventory[id] = num
            self.__items[id] = new_item

    def delete_item(self, id: str, comment: str) -> None:
        """
        Deletes an existing item in the inventory with the given id along with deletion comment.
        If an item with the given id does not exist, a NoSuchItemException is raised.
        If argument id is an empty string, a MissingFieldsExceptionis raised.

        :param id: id of the item to be removed
        """
        if id not in self.__inventory:
            raise NoSuchItemException
        elif id == '':
            raise MissingFieldsException
        else:
            self.add_deleted(self.__items[id], self.__inventory[id], comment)
            del self.__inventory[id]
            del self.__items[id]

    def add_deleted(self, item: Item, num: int, comment: str) -> None:
        """
        Helper function that adds an item along with a deletion comment to the recently deleted stack

        :param item: item to be added to the deleted stack
        :param num: number of items in the inventory before deletion
        :param comment: deletion comment
        """
        delete = (item, num, comment)

        if len(self.__deleted) == 10:
            self.__deleted.popleft()
            self.__deleted.append(delete)
        else:
            self.__deleted.append(delete)

    def undelete(self) -> None:
        """
        Undeletes the most recently deleted item. If there is an item with the same name or ID in the
        inventory at the time, an ExistingItemException is raised and the item remains in the deleted stack.
        If no more undeletes can be made, a NoSuchItemException is raised.
        """
        if len(self.__deleted) == 0:
            raise NoSuchItemException

        undeleted = self.__deleted.pop()
        undeleted_item, undeleted_num = undeleted[0], undeleted[1]
        undeleted_id = undeleted_item.get_id()

        if undeleted_id in self.__inventory or undeleted_item.get_name() in {i.get_name() for i in self.__items.values()}:
            self.__deleted.append(undeleted)
            raise ExistingItemException
        else:
            self.__inventory[undeleted_id] = undeleted_num
            self.__items[undeleted_id] = undeleted_item


    def set_num(self, id: str, num: int) -> None:
        """
        Sets the recorded number of items stored in the inventory. If an item with the given id does not
        exist, a NoSuchItemException is raised. If the argument id is an empty string, a MissingFieldsException
        is raised.

        :param num: the new recorded number of items
        """
        if id not in self.__inventory:
            raise NoSuchItemException
        elif id == '':
            raise MissingFieldsException
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
        df = pd.DataFrame({"Name":pd.Series(names), "Num":pd.Series(self.__inventory)})
        df.index.name = 'ID'
        df.reset_index(inplace=True)
        return df

    def deleted_dataframe(self) -> pd.DataFrame:
        """
        Returns the deleted as a dataframe

        :return: pandas dataframe that represents deleted
        """
        new_deleted = copy.deepcopy(self.__deleted)
        data = []
        for _ in range(len(new_deleted)):
            i, num, comment = new_deleted.pop()
            data.append([i.get_id(), i.get_name(), num, comment])
        df = pd.DataFrame(data, columns=["ID", "Name", "Num", "Comment"])
        return df