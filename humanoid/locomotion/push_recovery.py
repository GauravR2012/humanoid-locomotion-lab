class PushRecovery:

    def __init__(self,gain=0.5):

        self.gain=gain

    def recover(self,pos,disturbance):

        return pos+self.gain*disturbance