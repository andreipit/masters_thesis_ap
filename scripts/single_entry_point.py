from utils.imports.entry_point_import import *

if __name__ == '__main__':
    print('hi')
    env = gym.make('environment:env-v1')
    #env = Env01()


    a: ArgsModel = ParserJson.convert_dict_to_vars(ParserJson.load_config(debug = False))




    
    
