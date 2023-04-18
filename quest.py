class Quest:
    def __init__(self, region, title, reward, solution, done=False):
        self.region = region
        self.title = title
        self.reward = reward
        self.solution = solution
        self.done = done

    def to_dict(self):
        return {
            'region': self.region,
            'title': self.title,
            'reward': self.reward,
            'solution': self.solution
        }

    def __str__(self):
        return f'Quest(region={self.region}, title={self.title}, reward={self.reward}, solution={self.solution})'
