import logger
"""
NOTE: Any object that inherits a Cursor object MUST
inherit from a PycursesObject as their top-level parent.
I.E. PycursesObject must be the farthest right inherited object.
"""


class Cursor:
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def select_item(self, item_instance):
        """
        Takes an instance of an Item and runs it's on_select function.
        """
        pass

class SingleObjectCursor(Cursor):
      
    def __init__(self, *args, **kwargs):
         """
         NOTE: wrap_objects relies on an attribute in a json file.
         """
         super().__init__(*args, **kwargs)
         wrap_objects = kwargs.get('wrap_objects')
         self.wrap_objects = False if wrap_objects is None else wrap_objects
         self.selected_object_index = 0
         self.selected_object_list = getattr(self, 'children')
         logger.log_t(str(self.selected_object_list))
         self.selected_object = lambda : self.selected_object_list[self.selected_object_index]

    def get_selected_object(self):
        return self.selected_object_list[self.selected_object_index]
    
    def next_object(self):
        """
        Increments self.selected_object_index by 1.
        If wrap_objects = True, and the Cursor is pointing at the last object,
            then self.selected_object_index will become 0 (to indicate returning to the top of the list).
        If wrap_objects = False, and the Cursor is pointing at the last object,
            then nothing happens.
        """
        # end_of_list is True when self.selected_object_index is at the end of the selected_object_list
        end_of_list = lambda : self.selected_object_index == len(self.selected_object_list) - 1
        # If EOL and wrapping enabled: set self.selected_object_index to 0
        if end_of_list() and (self.wrap_objects == True):
            self.selected_object_index = 0
        # If EOL and wrapping disabled: do nothing
        elif end_of_list() and (self.wrap_objects == False):
            pass
        # If not EOL: increment self.selected_object_index by 1
        else:
            self.selected_object_index += 1

    def previous_object(self):
        """
        Decrements self.selected_object_index by 1.
        If wrap_objects = True, and the Cursor is pointing at the first object,
            then self.selected_object_index will be set to 
            the length of self.selected_object_list minus 1 (to indicate going to the end of the list).
        If wrap_objects = False, and the Cursor is pointing at the first object,
            then nothing happens.
        """
        # start_of_list is True when self.selected_object_index is at the beginning of the selected_object_list
        start_of_list = lambda : self.selected_object_index == 0
        # If SOL and wrapping enabled: set self.selected_object_index to length of self.selected_object_list minus 1
        if start_of_list() and (self.wrap_objects == True):
            self.selected_object_index = len(self.selected_object_list) - 1
        # If SOL and wrapping disabled: do nothing
        elif start_of_list() and (self.wrap_objects == False):
            pass
        # If not EOL: increment self.selected_object_index by 1
        else:
            self.selected_object_index += 1