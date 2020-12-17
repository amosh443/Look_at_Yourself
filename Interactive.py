class Poll:
    def __init__(self, event='', question='', answers='', responses='', type=0, id=0):
        self.event = event
        self.question = question
        self.answers = answers
        if self.answers != '' and self.answers[-1] == '\n':
            self.answers = answers[:-1]
        self.responses = responses
        if self.responses != '' and self.responses[-1] == '\n':
            self.responses = self.responses[:-1]
        self.type = type
        self.id = id

    def list(self):
        return [self.event, self.question, self.type, self.answers, self.responses, self.id]

    def list_to_add(self):
        return [self.event, self.question, self.type, self.answers, self.responses]


def from_list(list):
    return Poll(list[1], list[2], list[4], list[5], list[3], id=list[0])
