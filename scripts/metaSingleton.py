class MetaSingleton(type):
    """
    Метакласс для класса Bot, для реализации синглтона
    """
    __instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls.__instance
