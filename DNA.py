class DNA:

    def __init__(self, value='random'):
        self.value = value

    def getDnaType(self, *args, **kwargs):
        if self.value == 'random':
            print('Random')
        else:
            print('Mutation detected! (doesn\'t have a valid DNA)')

    def __str__(self):
        print(self.value)
