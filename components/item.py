class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
        self.use_function=use_function
        self.targeting=targeting
        self.targeting_message=targeting_message
        self.function_kwargs=kwargs

    def __str__(self):
        return 'It casts {0}, does {1}have targeting, and with the kwargs of: {2}'.format(self.use_function, '' if self.targeting else 'not ', self.function_kwargs)