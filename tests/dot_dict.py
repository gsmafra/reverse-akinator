class DotDict(dict):
    """
    A dictionary whose elements can be accessed with dot notation.  It
    automatically converts nested dictionaries and dictionaries within lists
    into DotDicts.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._convert_values()

    def __getattr__(self, attr):
        #  __getattr__ is called only as a last resort if the attribute
        #  is not found in the normal places.
        if attr in self:
            return self[attr]
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{attr}'"
        )

    def __setattr__(self, attr, value):
        if isinstance(value, dict):
            value = DotDict(value)
        elif isinstance(value, list):
            value = [DotDict(v) if isinstance(v, dict) else v for v in value]
        super().__setattr__(attr, value)
        self[attr] = value

    def __delattr__(self, attr):
        if attr in self:
            del self[attr]
        else:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{attr}'"
            )

    def __repr__(self):
        """
        Provides a more readable representation of the DotDict, similar to
        a standard dictionary.
        """
        return dict.__repr__(self)

    def _convert_values(self):
        """
        Recursively converts dictionary values and values within lists to DotDicts.
        """
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = DotDict(value)
            elif isinstance(value, list):
                self[key] = [DotDict(v) if isinstance(v, dict) else v for v in value]
