import os
import glob

import numpy  as np
import pandas as pd
import tables as tb

data_path          = "/Users/Gonzalo/github/NEXTdata/MC/ECEC/v2_center/kdst/output/data"
output_filename    = "center_1s2.npy"
n_events_generated = int(1e5)

filenames     = glob.glob(os.path.join(data_path, "*"))
dfs           = [pd.DataFrame.from_records(tb.open_file(filename).root.DST.Events.read()) for filename in filenames]
df            = pd.concat(dfs)
subdf         = df[df.nS2 == 1]
events        = subdf.event.drop_duplicates().values.astype(int)
n_events_kdst = np.unique(   df.event).size
n_events_2S2  = np.unique(subdf.event).size

np.save(output_filename, events)

print(f"Total number of events generated: {n_events_generated:>8} = {100 * n_events_generated / n_events_generated:>6.2f} %")
print(f"Total number of events in kDST  : {n_events_kdst     :>8} = {100 * n_events_kdst      / n_events_generated:>6.2f} %")
print(f"Total number of events with 2 S2: {n_events_2S2      :>8} = {100 * n_events_2S2       / n_events_generated:>6.2f} %")

