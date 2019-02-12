class TemplateFiller(object):
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

    def __len__(self):
        return 2


class FakeCollect(object):
    def __init__(self, t):
        self.real_collect = t._collect

    def __call__(self, it):
        entries = []
        while True:
            try:
                v = next(it)
            except NameError as e:
                try:
                    v = e.args[0].split("'")[1]
                except:
                    v = 'undefined'
            except StopIteration:
                break
            entries.append(v)
        return self.real_collect(iter(entries))
