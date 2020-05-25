from stackoverservices.data.corpus import filters

import pandas as pd 

ddf = pd.read_csv("/so_data_questions_1103.csv")

filters.filter_quantile_union(ddf, 2, 'upper')