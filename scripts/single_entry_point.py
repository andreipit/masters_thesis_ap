from utils.imports.entry_point_import import *

if __name__ == '__main__':
    print('hi')
    a: ArgsModel = ParserJson.convert_dict_to_vars(ParserJson.load_config(debug = False))
    #env = gym.make('environment:env-v1') # Env01()
    env = Env01()
    done = False
    state = env.reset(seed = None, return_info = False, options = None)





    
    
