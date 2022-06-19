from utils.server import Server


class EnvReset():
    def __init__(self):
        print('reset done')
    
    def run(self):

        Server.message_to_send = 'reset'
        print('run reset')



