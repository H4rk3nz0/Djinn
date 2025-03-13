class util:
    def __init__(self):
        self.PURPLE = '\033[35m'
        self.BLUE = '\033[34m'
        self.GREEN = '\033[32m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[31m'
        self.END = '\033[0m'

    def print_p(self, text):
        print(f'[~]{self.PURPLE} {text} {self.END}')
    
    def print_c(self, text):
        print(f'[+]{self.GREEN} {text} {self.END}')

    def print_f(self, text):
        print(f'[!]{self.RED} {text} {self.END}')

    def print_w(self, text):
        print(f'[*]{self.YELLOW} {text} {self.END}')