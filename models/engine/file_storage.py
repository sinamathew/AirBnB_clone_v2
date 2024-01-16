#!/usr/bin/python3
import json
import os
""" file storage module """


class FileStorage:
    """ A class that stores objects in a file in json format """

    # Private Class Attributes
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a list of all objects, or a dictionary if cls is provided."""
        if cls is None:
            return list(self.__objects.values())
        else:
            return {key: obj for key, obj in self.__objects.items() if isinstance(obj, cls)}



    def new(self, obj):
        """Adds new object to the storage dictionary."""
        self.__objects[obj.to_dict()['__class__'] + '.' + obj.id] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            for key, obj in self.__objects.items():
                temp[key] = obj.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.__objects[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from the storage.

        Args:
            obj: The object to delete. If None, does nothing.
=======
    # Public instance method
    def all(self):
        """ returns the dictionary __objects """
        return (FileStorage.__objects)

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """
        cls_name = obj.__class__.__name__
        key = cls_name + "." + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """

        # Convert __objects to dictionary before storing in file
        object_dict = {}
        for key, value in FileStorage.__objects.items():
            object_dict[key] = value.to_dict()

        # Serialization to JSON
        json_str = json.dumps(object_dict)

        with open(FileStorage.__file_path, "w") as file:
            file.write(json_str)

    def delete(self, obj_id):
        """ delete an object from json file """
        del self.__objects[obj_id]
        self.save()

    def reload(self):
>>>>>>> 928eb9037ad9b6e471bdbcd092b58e16e47e9cb3
        """
            deserializes the JSON file to __objects (only if the JSON file
            (__file_path) exists ; otherwise, do nothing. If the file doesn’t
            exist, no exception should be raised)
        """
        if os.path.exists(FileStorage.__file_path):
            json_str = ""
            with open(FileStorage.__file_path, "r") as file:
                json_str = file.read()

            # models imported here to avoid circular import
            from models.base_model import BaseModel
            from models.user import User
            from models.place import Place
            from models.review import Review
            from models.amenity import Amenity
            from models.city import City
            from models.state import State

            # Deserialized back to python dictionary
            object_dict = json.loads(json_str)
            for key, value in object_dict.items():
                if value['__class__'] == "BaseModel":
                    obj = BaseModel(**value)
                elif value['__class__'] == "User":
                    obj = User(**value)
                elif value['__class__'] == "Place":
                    obj = Place(**value)
                elif value['__class__'] == "City":
                    obj = City(**value)
                elif value['__class__'] == "State":
                    obj = State(**value)
                elif value['__class__'] == "Amenity":
                    obj = Amenity(**value)
                elif value['__class__'] == "Review":
                    obj = Review(**value)
                FileStorage.__objects[key] = obj
