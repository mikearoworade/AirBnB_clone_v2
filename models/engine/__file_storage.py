#!/usr/bin/python3
"""Defines the FileStorage class"""
import json
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

"""Handles long term storage of all class instances
        classes - this variable is a dictionary with:
        keys: Class Names
        values: Class type (used for instantiation)
"""
classes = {
        'BaseModel': BaseModel,
        'Amenity': Amenity,
        'City': City,
        'Place': Place,
        'Review': Review,
        'State': State,
        'User': User
    }

class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of instantiated objects in __objects.

        If a cls is specified, returnsif cls == value.__class__ or cls == value.__class__.__name__: a dictionary of objects of that type.
        Otherwise, returns the __objects dictionary.
        """
        if cls is not None:
            new_objs = {}
            for clsid, obj in self.__objects.items():
                if cls == obj.__class__ or cls == obj.__class__.__name__:
                    new_objs[clsid] = value
            return new_objs
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        clsname = obj.__class__.__name__
        clsname_id = "{}.{}".format(clsname, obj.id)
        FileStorage.__objects[clsname_id] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        fileName = FileStorage.__file_path
        json_objects = {}
        for clsname_id, clsname_obj in FileStorage.__objects.items():
            json_objects[clsname_id] = clsname_obj.to_dict()
        with open(fileName, mode="w", encoding='utf-8') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        fileName = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(fileName, mode='r', encoding='utf-8') as f:
                new_objs = json.load(f)
                for obj_id, objdict in new_objs.items():
                    clsname = objdict["__class__"]
                    FileStorage.__objects[obj_id] = classes[clsname](**objdict)
        except:
            return

    def delete(self, obj=None):
        """Delete a given object from __objects, if it exists."""
        if obj:
            clsname_id = "{}.{}".format(type(obj).__name__, obj.id)
            all_class_objs = self.all(obj.__class__.__name__)
            if all_class_objs.get(clsname_id):
                del FileStorage.__objects[clsname_id]
            self.save()

    def delete_all(self):
        """Deletes all stored objects, for testing purposes"""
        try:
            with open(FileStorage.__file_path, mode='w') as f_io:
                pass
        except:
            pass
        del FileStorage.__objects
        FileStorage.__objects = {}
        self.save()

    def close(self):
        """Call the reload method."""
        self.reload()

    def get(self, cls, id):
        """retrieves one object based on class name and id"""
        if cls not in classes.values():
            return None

        all_obj = self.all(cls)
        for value in all_obj.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """returns the count of all objects in storage"""
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(self.all(clas).values())
        else:
            count = len(self.all(cls).values())

        return count
