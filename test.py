from utilities.pyutils import as_tuple, combine_dfs, keys_tuple_list
from probability.mvprob import probs, probs_dict
from information.EntroPy import EntroPy
import pandas as pd
import math


x = pd.DataFrame([0,1,3,2,7,1,1,2,3,1,2,1,3], columns=['a'])
#x['v'] = [3,1,3,2,3,1,3,5,3,1,2,1,3]
y = pd.DataFrame([0,1,3,1,1,1,1,2,3,1,2,4,3], columns=['b'])
#y['v'] = [1,2,2,2,7,2,1,2,3,1,2,1,3]
print(x.to_records(index=False).tolist())

result = EntroPy.relative_entropy(x, y)
print(result)

