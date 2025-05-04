class Task():
    def __init__(self, text, date, completed=False):
        self.text = text
        self.date = date
        self.completed = completed
    
    def __repr__(self):
        return f"{self.text}\nDate de modification : {self.date}"

    def to_dict(self):
        return {"text" : self.text, "date" : self.date, "completed" : self.completed}