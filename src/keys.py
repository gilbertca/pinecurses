"""**keys** contains the primary class: PinecursesKeys

This is used internally by the PinecursesApp for:
    1. Contains a loop for collecting keypresses
    2. Contains a map that relates keys to functions
    3. Executes the related function if applicable
"""

class PinecursesKeys:
    def __init__(self, keys_namespace):
        self.keys_namespace = keys_namespace
