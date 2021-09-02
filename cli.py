class CLI():
    def __init__(self):
        pass
    
    def info(self, c):
        print(self.construct_string(c, ""))
    
    def error(self, c):
        print(self.construct_string(c, "ERROR"))
    
    def failed(self, c):
        print(self.construct_string(c, "FAILED"))

    def success(self, c):
        print(self.construct_string(c, "SUCCESS"))
    
    def focus(self, c):
        print(self.construct_string(c, "FOCUS"))

    def construct_string(self, line, typ):
        line =  line + " \x1b[0m"
        if typ == "SUCCESS":
            line = "\x1b[2;35;42m" + line
        elif typ == "FAILED":
            line = "\x1b[1;31;40m" + line
        elif typ ==  "ERROR":
            line = "\x1b[6;37;41m" + line
        elif typ ==  "FOCUS":
            line = "\x1b[2;34;40m" + line
        return line