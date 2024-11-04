import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent
params = 'paramsConfigs'
data = 'data'

PARAM_PATH = os.path.join(root, params)
DATA_PATH = os.path.join(root, data)



if __name__ == '__main__':
    print(PARAM_PATH)
    print(DATA_PATH)