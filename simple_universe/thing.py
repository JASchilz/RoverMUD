from basics import BaseThing

class SimpleThing(BaseThing):

    name = ""
    description = ""
    keywords = []

    takable = True

    def __init__(self, name, description, keywords=[], takable=True):

        self.name = name
        self.description = description
        self.keywords = keywords

        self.takable = takable

        self.short_description = self.name

    def room(self):

        answer = self.container

        while not answer.__class__.__name__ == "SimpleRoom":
            answer = answer.container

        return answer
