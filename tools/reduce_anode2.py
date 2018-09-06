import os
import time
import numpy  as np
import pandas as pd

path_tables       = "/Users/Gonzalo/github/NEXTdata/NEWtables/"
path_tables       = "/Volumes/SAMSUNG/NEXT100tables/S2"
filename_anode    = os.path.join(path_tables,        "Anode.dat")
filename_sipm_map = os.path.join(path_tables, "sipm_mapping.dat")
filename_el_map   = os.path.join(path_tables,   "el_mapping.dat")


@np.vectorize
def to_index(sensor_id):
    return (sensor_id // 1000 - 1) * 64   + sensor_id % 1000


def reduce_file_anode(filename, df_sipm, df_el, r_max):
    new_filename = filename.replace(".dat", "_reduced2.dat")

    print(f"Reading {filename}...", flush=True, end="")
    t0 = t00     = time.time()
    anode        = pd.DataFrame.from_csv(filename_anode, sep=" ", index_col=None)
    pointid      = anode.PointID
    full_df_size = len(anode)
    dt           = time.time() - t0
    print(f"Done! Ellapsed time: {dt:.2f} s")
    print(f"Original df size is {full_df_size} rows")

    print("Computing indices...", flush=True, end="")
    t0      = time.time()
    indices = anode.SensorID.map(df_sipm.idx)
    dt      = time.time() - t0
    print(f"Done! Ellapsed time: {dt:.2f} s")

    print("Computing dx and filtering...", flush=True, end="")
    t0         = time.time()
    dx         = indices.map(df_sipm.X) - pointid.map(df_el.X)
    sel        = np.abs(dx) <= r_max
    anode      = anode  [sel]
    indices    = indices[sel]
    pointid    = pointid[sel]
    dx         = dx     [sel]
    dx_df_size = len(anode)
    dt         = time.time() - t0
    print(f"Done! Ellapsed time: {dt:.2f} s")
    print(f"After dx filtering df size is {dx_df_size} rows = {100 * dx_df_size / full_df_size:.3f} %")

    print("Computing dy and filtering...", flush=True, end="")
    t0         = time.time()
    dy         = indices.map(df_sipm.Y) - pointid.map(df_el.Y)
    sel        = np.abs(dy) <= r_max
    anode      = anode  [sel]
    indices    = indices[sel]
    pointid    = pointid[sel]
    dx         = dx     [sel]
    dy         = dy     [sel]
    dy_df_size = len(anode)
    dt         = time.time() - t0
    print(f"Done! Ellapsed time: {dt:.2f} s")
    print(f"After dy filtering df size is {dy_df_size} rows = {100 * dy_df_size / full_df_size:.3f} %")

    print("Computing dr and filtering...", flush=True, end="")
    t0         = time.time()
    dr         = np.sqrt(dx**2 + dy**2)
    sel        = np.abs(dr) <= r_max
    anode      = anode[sel]
    dr_df_size = len(anode)
    dt         = time.time() - t0
    print(f"Done! Ellapsed time: {dt:.2f} s")
    print(f"After dr filtering df size is {dr_df_size} rows = {100 * dr_df_size / full_df_size:.3f} %")

    print(f"Writing data to {new_filename}...")
    t0 = time.time()
    with open(new_filename, "w") as file_out:
        header    = "Dummy PointID SensorID P0 P1\n"
        file_out.write(header)

        s = ""
        n = dr_df_size
        m = n // 10
        for i, row in anode.reset_index(drop=True).iterrows():
            if i and not i % m:
                file_out.write(s)
                s = ""
                p = 100 * i / n
                print(f"{p:.1f} %")

            s += f"1 {int(row.PointID)} {int(row.SensorID)} {row.P0} {row.P1}\n"
        if s:
            file_out.write(s)

    dt  =  time.time() - t0
    dt0 = (time.time() - t00) / 3600
    print(f"Done! Ellapsed time: {dt :.2f} s")
    print(f"Total ellapsed time: {dt0:.2f} h")


if __name__ == "__main__":
    sipm        = pd.DataFrame.from_csv(filename_sipm_map, sep=" ", index_col=0)
    el          = pd.DataFrame.from_csv(filename_el_map  , sep=" ", index_col=0)
    sipm["idx"] = to_index(sipm.index.values)
    r_max       = 100

    reduce_file_anode(filename_anode, sipm, el, r_max)