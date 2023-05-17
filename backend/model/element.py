import os
from abc import ABC, abstractmethod
from typing import List

from db.db_handler import DATABASE, get_supercategories
from interface.displayable import Displayable, Category


class Element(ABC):

    def __init__(self, category, title, done=None):
        self.category = Category(category)
        self.title = Displayable(title)
        if done is None:
            self.done = False
        else:
            self.done = done == 'True'

    def to_dict(self):
        return {
            attr: str(getattr(self, attr))
            for attr in dir(self)
            if not attr.startswith('__') and not callable(getattr(self, attr))
               and not (isinstance(getattr(self, attr), ABC) or attr == '_abc_impl')
        }

    @classmethod
    def get_element_instances_from(cls, all_data: List[dict]):
        all_elements = []
        for data in all_data:
            element = cls(**data)
            all_elements.append(element)
        return all_elements

    def get_displayable_attributes(self):
        """Returns a list of the attributes that are instances of Displayable,
            except those which are instances of Category."""
        return [
            attr for attr in dir(self)
            if isinstance(getattr(self, attr), Displayable)
               and not isinstance(getattr(self, attr), Category)
        ]

    @abstractmethod
    def _init_displayables(self, ):
        pass

    def __str__(self):
        # Returns the string name of the specific class that inherits from Element, followed by a representation of
        # the result of to_dict
        return f'{self.__class__.__name__}({self.to_dict()})'


class Stackable(Element):
    def __init__(self, category, title, done=None, stackable_properties=None):
        super().__init__(category, title, done)
        if stackable_properties is None:
            self.stackable_properties = {}
        else:
            self.stackable_properties = stackable_properties
        self.constituent_stackables = []

    @property
    def stackable_properties(self):
        # Dynamically calculate stackable_properties based on constituent Stackables
        stackable_properties = self._stackable_properties.copy()  # Start with the base properties
        for stackable in self.constituent_stackables:
            if not stackable.done:
                for prop, value in stackable.stackable_properties.items():
                    if prop in stackable_properties:
                        stackable_properties[prop] += value
                    else:
                        stackable_properties[prop] = value
        return stackable_properties

    @stackable_properties.setter
    def stackable_properties(self, value):
        self._stackable_properties = value

    def stack_with(self, other):
        # Make sure the other object is a Stackable
        if not isinstance(other, Stackable):
            raise ValueError("Can only stack with another Stackable")
        # Create a new Stackable that represents the combination
        new_stackable = Stackable(self.category, self.title, self.done, self._stackable_properties.copy())
        new_stackable.constituent_stackables = self.constituent_stackables + [other]
        return new_stackable

    def unstack(self, other):
        # Similar to stack_with, but subtracts the properties of the other stackable
        if not isinstance(other, Stackable):
            raise ValueError("Can only unstack with another Stackable")

        new_stackable = Stackable(self.category, self.title, self.done, self.stackable_properties.copy())
        new_stackable.stack = self

        for prop, value in other.stackable_properties.items():
            if prop in new_stackable.stackable_properties:
                new_stackable.stackable_properties[prop] -= value
                if new_stackable.stackable_properties[prop] <= 0:
                    # If the property value becomes 0 or negative, remove it from the stackable
                    del new_stackable.stackable_properties[prop]
            else:
                # If the property doesn't exist in the current stackable, ignore it
                pass

        return new_stackable

    def _init_displayables(self):
        """Init each displayable attribute in order of appearance in the GUI"""
        self.__init_title()

    def __init_title(self):
        title = self.title
        title.set_font_size(20)
        title.set_font_weight('bold')
        title.set_alignment('center')
        title.set_word_wrap(True)
        title.set_text_format('rich')


class Quest(Element):

    def __init__(self, category, title, reward, solution, done=False):
        super().__init__(category, title, done)
        self.reward = Displayable(reward)
        self.solution = Displayable(solution)
        self._init_displayables()

    def _init_displayables(self):
        """Init each displayable attribute in order of appearance in the GUI"""
        self.__init_category()
        self.__init_title()
        self.__init_reward()
        self.__init_solution()

    def __init_category(self):
        category = self.category
        try:
            for supercategory in get_supercategories():
                path = os.path.join(DATABASE, supercategory.value)
                for i, filename in enumerate(os.listdir(path)):
                    if category.value.lower() in filename.lower():
                        color = Category.get_colors()[i % len(Category.get_colors())]
                        self.category.set_background_color(color)
                        break
        except FileNotFoundError:
            pass

    def __init_title(self):
        title = self.title
        title.set_font_size(20)
        title.set_font_weight('bold')
        title.set_alignment('center')
        title.set_word_wrap(True)
        title.set_text_format('rich')

    def __init_solution(self):
        solution = self.solution
        solution.set_font_size(15)
        solution.set_word_wrap(True)
        solution.set_text_format('rich')

    def __init_reward(self):
        reward = self.reward
        reward.set_font_weight('italic')
        reward.set_word_wrap(True)
        reward.set_text_format('rich')
