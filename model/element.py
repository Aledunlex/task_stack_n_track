import os
from abc import ABC, abstractmethod

from model.displayable import Displayable, Category

DATABASE = "DATABASE"


class Element(ABC):
    def __init__(self, category, title, done=False):
        self.category = Category(category)
        self.title = Displayable(title)
        self.done = done

    def to_dict(self):
        return {attr: str(getattr(self, attr)) for attr in dir(self)
                if not attr.startswith('__') and not callable(getattr(self, attr))}

    def get_displayable_attributes(self):
        """Returns a list of the attributes that are instances of Displayable,
        except those which are instances of Category."""
        return [attr for attr in dir(self)
                if isinstance(getattr(self, attr), Displayable) and not isinstance(getattr(self, attr), Category)]


    @abstractmethod
    def _init_displayables(self, ):
        pass

    def __str__(self):
        # Returns the string name of the specific class that inherits from Element, followed by a representation of
        # the result of to_dict
        return f'{self.__class__.__name__}({self.to_dict()})'


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
        for i, filename in enumerate(os.listdir(DATABASE)):
            if category.value.lower() in filename.lower():
                color = Category.get_colors()[i % len(Category.get_colors())]
                self.category.set_background_color(color)
                break

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
