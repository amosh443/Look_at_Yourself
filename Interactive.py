class Poll:
    def __init__(self, event_id=0, question='', answers=[], responses=[], type=0, id=0):
        self.event_id = event_id
        self.question = question
        self.answers = answers
        self.responses = responses
        self.type = type
        self.id = id

    def list_questions(self):
        return [self.event_id, self.question, self.type, self.id]

    def list_to_add(self):
        return [self.event_id, self.question, self.type]

    def list_answers(self):
        res = []
        for i, answer in enumerate(self.answers):
            res.append([i, self.id, answer])
        return res

    def list_responses(self):
        res = []
        for i, response in enumerate(self.responses):
            res.append([i, self.id, response])
        return res


def from_list(list):
    return Poll(list[1], list[2], type=list[3], id=list[0])
