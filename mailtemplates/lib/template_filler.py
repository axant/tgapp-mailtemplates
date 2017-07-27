class TemplateFiller:
    def __init__(self, name=None):
        self.name = name
        self.rounds = 0

    def __getitem__(self, item):
        return TemplateFiller(name=item)

    def __getattr__(self, item):
        return TemplateFiller(name=item)

    def __html__(self):
        return self.name

    def __nonzero__(self):
        return True

    def __unicode__(self):
        return self.name

    def __iter__(self):
        return TemplateFiller(self.name)

    def __repr__(self):
        return self.name

    def next(self):
        if self.rounds >= 2:
            raise StopIteration()
        self.rounds += 1
        return TemplateFiller(self.name)

    def __call__(self, *args, **kwargs):
        return self.name
