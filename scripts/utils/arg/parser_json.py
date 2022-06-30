import json
from typing import Any
import io
import os
import numpy as np

from utils.arg.model import ArgsModel

class ParserJson():
    def __init__(self):
        pass

    @staticmethod
    def load_config(debug = False) -> dict:
        conf_file: io.TextIOWrapper = open('utils/config/config.json')
        conf: dict = json.load(conf_file)
        if debug:
            print('future_reward_discount=',type(conf["future_reward_discount"]))
            for x in conf:
                print(x, '=', conf[x])
            #[print(x, conf[x]) for x in conf]
        return conf

    @staticmethod
    def convert_dict_to_vars(c: dict) ->ArgsModel:
        """Just copy and convert: path to abs, list to np.array"""

        res: ArgsModel = ArgsModel()

        res.workspace_limits = np.asarray(c['workspace_limits'], dtype = float) # Cols: min max, Rows: x y z (define workspace limits in robot coordinates)
        res.stage = c['stage']
        res.goal_obj_idx = c['goal_obj_idx']

        return res


