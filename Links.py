class Link:
    def __init__(self, name='', text='', attachment=''):
        self.name = name
        self.text = text
        self.attachment = attachment

    def list(self):
        return [self.name, self.text, self.attachment]


def from_list(list):
    return Link(list[0], list[1], list[2])