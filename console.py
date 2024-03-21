#!/usr/bin/python3
"""Defines the HBNB console."""
import cmd
import sys
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """Defines the HBNB command interpreter.
        Attributes:
            prompt(str): The command prompt.
    """
    prompt = "(hbnb) "

    classes = {'BaseModel': BaseModel, 'User': User, 'Place': Place,
                'State': State, 'City': City, 'Amenity': Amenity,
                'Review': Review
            }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float, 'age': int
            }

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """Usage: create <class> <key 1>=<value 2> <key 2>=<value 2> ...
        Create a new class instance with given keys/values and print its id.
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")

            kwargs = {}
            for i in range(1, len(my_list)):
                key, value = tuple(my_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                new_instance = HBNBCommand.classes[my_list[0]]()
            else:
                new_instance = HBNBCommand.classes[my_list[0]](**kwargs)
                storage.new(new_instance)
            print(new_instance.id)
            new_instance.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, args):
        """Usage: show <class> <id>
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        new = args.partition(" ")
        cls_name = new[0]
        cls_id = new[2]
        key = cls_name + "." + cls_id
        objdict = storage.all()

        if not cls_name:
            print("** class name is missing  **")
            return
        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exist  **")
            return
        if not cls_id:
            print("** instance id missing  **")
            return
        
        try:
            print(objdict[key])
        except KeyError:
            print("** no instance found  **")

    def do_destroy(self, args):
        """Usage: destroy <class> <id>
        Delete a class instance of a given id.
        """
        args = args.partition(" ")
        cls_name = args[0]
        cls_id = args[2]
        key = cls_name + "." + cls_id
        objdict = storage.all()

        if not cls_name:
            print("** class name is missing  **")
            return
        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exist  **")
            return
        if not cls_id:
            print("** instance id missing  **")
            return

        try:
            del(objdict[key])
            print(key, "Successfully deleted")
            storage.save()
        except KeyError:
            print("** no instance found **")

    def do_all(self, line):
        """Usage: all <class> or all
        Display string representations of all instances of a given class.
        If no class is specified, display all instantiated objects.
        """
        print_list = []

        if not line:
            objdict = storage.all()
            print([objdict[k].__str__() for k in objdict])
            return
        try:
            args = line.split(" ")
            if args[0] not in HBNBCommand.classes:
                raise NameError()

            objdict = storage.all(eval(args[0]))
            print([objdict[k].__str__() for k in objdict])
            return

        except NameError:
            print("** class doesn't exist **")

    def do_update(self, args):
        """Usage: update <class> <id> <attribute_name> <attribute _value>
        Update a class instance of a given id by adding or updating
        a given attribute key/pair or dictionary.
        """
        cls_name = cls_id = attr_name = attr_value = kwargs = ""
        objdict = storage.all()

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            cls_name = args[0]
        else:
            print("** class name missing  **")
            return
        if cls_name not in HBNBCommand.classes:
            print("** class doesn't exit  **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            cls_id = args[0]
        else: #id not present
            print("** instance id missing  **")
            return

        #generate key from class and id
        key = cls_name + "." + cls_id
        #determine if key is present
        if key not in objdict:
            print("** no instance found  **")
            return

         # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)

        else: # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                attr_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')
            # if attr_name was not quoted arg
            if not attr_name and args[0] != ' ':
                attr_name = args[0]

            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                attr_value = args[2][1:args[2].find('\"', 1)]

            # if attr_value was not quoted arg
            if not attr_value and args[2]:
                attr_value = args[2].partition(' ')[0]

            args = [attr_name, attr_value]

        # retrieve dictionary of current objects
        obj_to_update = objdict[key]

        # iterate through attr names and values
        for i, attr_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                attr_value = args[i + 1]  # following item is value
                if not attr_name:  # check for attr_name
                    print("** attribute name missing **")
                    return
                if not attr_value:  # check for attr_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if attr_name in HBNBCommand.types:
                    attr_value = HBNBCommand.types[attr_name](attr_value)

                # update dictionary with name, value pair
                obj_to_update.__dict__.update({attr_name: attr_value})
        print(obj_to_update)
        storage.save()

    def do_count(self, args):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        count = 0
        objdict = storage.all()
        for k, v in objdict.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
