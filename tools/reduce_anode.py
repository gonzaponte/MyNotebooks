import os
import pandas as pd

path_tables       = "/Users/Gonzalo/github/NEXTdata/NEWtables/"
filename_anode    = os.path.join(path_tables,        "Anode.dat")
filename_sipm_map = os.path.join(path_tables, "sipm_mapping.dat")
filename_el_map   = os.path.join(path_tables,   "el_mapping.dat")

sipm   = pd.DataFrame.from_csv(filename_sipm_map, sep=" ", index_col=0)
el     = pd.DataFrame.from_csv(filename_el_map  , sep=" ", index_col=0)
r_max  = 100
r_max2 = r_max**2

def reduce_file_anode(filename):
    new_filename = filename.replace(".dat", "_reduced.dat")

    print(f"Reading {filename}...")
    with open(new_filename, "w") as file_out:
        header    = "Dummy PointID SensorID P0 P1\n"
        file_out.write(header)

        with open(filename, "r") as file_in:
            s = ""
            for i, line in enumerate(file_in):
                if not i and str.isalpha(line[0]): continue
                if     i and not i % 100000:
                    file_out.write(s)
                    s = ""
                    print(i // 100000)

                _, point_id, sensor_id, p0, p1, *_ = line.split()
                xp, yp    = el  .loc[int( point_id)]
                _, xs, ys = sipm.loc[int(sensor_id)]
                r2     = (xp - xs)**2 + (yp - ys)**2
                if r2 > r_max2: continue

                s += f"1 {point_id} {sensor_id} {p0} {p1}\n"
            if s:
                file_out.write(s)

if __name__ == "__main__":
    reduce_file_anode(filename_anode)