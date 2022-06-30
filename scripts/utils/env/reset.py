from utils.network.server_unity3d import Server


class EnvReset():
    def __init__(self):
        print('reset done')
    
    def run(self):

        Server.message_to_send = 'reset'
        print('run reset')



