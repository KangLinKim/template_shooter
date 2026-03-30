class GameManager:
    def __init__(self):
        self._score = 0

    @property
    def score(self):
        return self._score
    
    def earn_score(self, amount):
        self._score += amount