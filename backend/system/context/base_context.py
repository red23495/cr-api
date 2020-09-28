class BaseContext(dict):
    """
     warning: This is a singletone object. Don't create a instance of this object directly
    """
    context_obj: 'BaseContext' = None

    initial_data: dict = {
    }

    def initialize(self):
        """ Initializes the context with default data """
        self.update(self.initial_data)

    def clean(self):
        """ Clears all context data """
        self.clear()

    def reset(self):
        """ Clears all context data and re-initializes the dict with default data """
        self.clean()
        self.reset()

    @classmethod
    def get_instance(cls):
        if BaseContext.context_obj is None:
            BaseContext.context_obj = cls()
            BaseContext.context_obj.initialize()
        return BaseContext.context_obj

