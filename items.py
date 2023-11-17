
class Object:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.interaction_options = {"inspect": self.inspect}

    def inspect(self):
        return f"{self.name}\n" \
               f"{self.description}"
