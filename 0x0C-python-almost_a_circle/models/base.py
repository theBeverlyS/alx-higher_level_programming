#!/usr/bin/python3

'''A module used to act as a base for other modules'''


import json
import csv
import turtle


class Base:
    '''A base class for other classes'''

    __nb_objects = 0

    def __init__(self, id=None):
        '''
        A constructor function for the Base class

        Args:
            id: int
        '''
        self.id = None

        if id is None:
            Base.__nb_objects += 1
            self.id = Base.__nb_objects
        else:
            self.id = id

    @staticmethod
    def to_json_string(list_dictionaries):
        '''
        A function to convert dict-based attributes in to json string

        Args:
            list_dictionaries: list
        Returns:
            str
        Raises:
            json.JSONDecodeError
        '''
        if isinstance(list_dictionaries, (list))\
                and len(list_dictionaries) >= 0:
            if all(isinstance(obj, dict) for obj in list_dictionaries):
                return json.dumps(list_dictionaries)
            else:
                raise TypeError(
                        'argument should only contain list of dictionaries'
                        )
        if list_dictionaries is None or len(list_dictionaries) <= 0:
            return "[]"
        else:
            raise TypeError(
                    "argument should only contain list of dictionaries"
                    )

    @staticmethod
    def from_json_string(json_string):
        '''
        A static method tgat returns the list of the JSON string representation

        Args:
            json_string: str
        Returns:
            list
        Raises:
            json.JSONDecodeError
        '''
        if json_string is None:
            return []
        if isinstance(json_string, (str)):
            if len(json_string) == 0:
                return []
            else:
                return json.loads(json_string)
        else:
            raise TypeError("must be a string")

    @classmethod
    def save_to_file(cls, list_objs):
        '''
        A function that writes teh JSON string representation of list_objs
        to a file

        Args:
            cls: class
            list_objs: class objects
        Raises:
            ValueError
        '''
        dict_list = []

        if list_objs is None:
            with open(cls.__name__ + ".json", 'w') as file:
                file.write(cls.to_json_string(dict_list))
            return
        if len(list_objs) == 0:
            with open(cls.__name__ + ".json", 'w') as file:
                file.write(cls.to_json_string(dict_list))
            return

        if all(isinstance(obj, cls) for obj in list_objs):
            dict_list = [obj.to_dictionary() for obj in list_objs]
            with open(cls.__name__ + ".json", 'w') as file:
                file.write(cls.to_json_string(dict_list))
        else:
            raise AttributeError(
                    "list does not contain objects of the same class"
                    )

    @classmethod
    def create(cls, **dictionary):
        '''
        A class method that returns an instance with all attributes already set

        Args:
            cls: class
            dictionary: dict
        '''
        dummy = None
        if cls.__name__ == 'Rectangle':
            dummy = cls(4, 8)
        if cls.__name__ == 'Square':
            dummy = cls(8)
        dummy.update(**dictionary)
        return dummy

    @classmethod
    def load_from_file(cls):
        '''
        A class method that returns a list of instances

        Args:
            cls: class
        Returns:
            list
        Raises:
            FileNotFoundError
        '''
        instances = []
        json_list = None

        try:
            with open(cls.__name__ + '.json', 'r') as file:
                json_list = cls.from_json_string(file.read())
            for element in json_list:
                instances.append(cls.create(element))
            return instances
        except FileNotFoundError:
            return instances

    @classmethod
    def save_to_file_csv(cls, list_objs):
        '''
        A class method that deserializes in CSV

        Args:
            cls: class
            list_objs: list
        Raises:
            TypeError
        '''
        csv_string = ''
        if len(list_objs) > 0 and isinstance(list_objs, (list)):
            if all(isinstance(obj, cls) for obj in list_objs):
                for obj in list_objs:
                    for value in obj.to_dictionary().values():
                        csv_string += str(value) + ','
                    csv_string[-1] = '\n'
                with open(cls.__name__ + '.csv', 'w') as file:
                    file.write(csv_string)
            else:
                raise TypeError(
                        "list does not contain objects of the same class"
                        )
        else:
            with open(cls.__name__ + '.csv', 'w') as file:
                file.write(csv_string)

    @classmethod
    def load_from_file_csv(cls):
        '''
        A class method that serializes in CSV

        Args:
            cls: class
        '''
        obj_list = []
        fieldnames = None
        try:
            with open(cls.__name__ + '.csv', 'r') as file:
                rows = []
                if cls.__name__ == "Rectangle":
                    fieldnames = ["id", "width", "height", "x", "y"]
                elif cls.__name__ == "Square":
                    fieldnames = ["id", "size", "x", "y"]
                elif not issubclass(cls, Base):
                    raise TypeError("Incompatible object type")

                reader = csv.DictReader(file, fieldnames=fieldnames)
                for row in reader:
                    for data in row:
                        row[data] = int(row[data])
                    rows.append(row)

                obj_list = [cls.create(**obj) for obj in rows]
        except FileNotFoundError:
            return []
        return obj_list

    @classmethod
    def draw(cls, list_rectangles, list_squares):
        '''
        Draw rectangles and squares side by side using the turtle module.

        Args:
            list_rectangles: list
            list_squares: list
        '''
        screen = turtle.Screen()
        screen.bgcolor("#180302")
        screen.title("Shapes | theLazyProgrammer^_^")

        drawer = turtle.Turtle()
        drawer.pensize(5)
        drawer.shape("circle")
        drawer.speed(5)

        cls._draw_shapes(drawer, list_rectangles, "#f4f45d", side_by_side=True)
        cls._draw_shapes(drawer, list_squares, "#0670d4", side_by_side=True)

        turtle.exitonclick()

    @staticmethod
    def _draw_shapes(turtle_drawer, shapes, color, side_by_side=False):
        '''
        Draw a list of shapes using the turtle module.

        Args:
            turtle_drawer: turtle.Turtle
            shapes: list
            color: str
            side_by_side: bool
        '''
        turtle_drawer.color(color)

        for shape in shapes:
            turtle_drawer.showturtle()
            turtle_drawer.up()

            if side_by_side:
                if shape.__class__.__name__ == "Square":
                    turtle_drawer.goto(shape.x + shape.size, shape.y)
                elif shape.__class__.__name__ == "Rectangle":
                    turtle_drawer.goto(shape.x + shape.width, shape.y)
            else:
                turtle_drawer.goto(shape.x, shape.y)

            turtle_drawer.down()
            if shape.__class__.__name__ == "Square":
                for _ in range(4):
                    turtle_drawer.forward(shape.size)
                    turtle_drawer.left(90)
            elif shape.__class__.__name__ == "Rectangle":
                for _ in range(2):
                    turtle_drawer.forward(shape.width)
                    turtle_drawer.left(90)
                    turtle_drawer.forward(shape.height)
                    turtle_drawer.left(90)
            turtle_drawer.hideturtle()
