class FakeSerial():
    def write(self, rr):
        return '3'
    def isOpen(self):
        return True
    
    def inWaiting(self):
        return 0