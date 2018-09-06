import os
import glob
import math
import operator

s1_path = "/Volumes/SAMSUNG/NEXT100tables/S1/"

# Defines active_map
exec(open(os.path.join(s1_path, "NEXT100_maps.py")).read())
reverse_active_map = {tuple(map(int, val)): key for key, val in active_map.items()}

def create_active_mapping(active_dict, output_filename):
    with open(output_filename, "w") as file:
        file.write("PointID X Y Z\n")
        zmax = max(map(operator.itemgetter(2), active_dict.values()))
        print(zmax)
        for point_id, (x, y, z) in sorted(active_dict.items()):
            file.write(f"{point_id} {x} {y} {zmax - z}\n")    

def create_pmt_mapping(pmt_dict, ring_dict, phi_dict, output_filename):
    with open(output_filename, "w") as file:
        file.write("SensorID X Y Corona R Phi\n")
        for sensor_id, (x, y) in sorted(pmt_dict.items()):
            ring = ring_dict[sensor_id]
            c, s =  phi_dict[sensor_id]
            r    = (x**2 + y**2)**0.5
            phi  = math.atan2(r*s, r*c)
            file.write(f"{sensor_id} {x} {y} {ring} {r} {phi}\n")

def create_sipm_mapping(sipm_dict, output_filename):
    with open(output_filename, "w") as file:
        file.write("SensorID X Y Dice idx\n")
        for sensor_id, (x, y) in sorted(sipm_dict.items()):
            dice = sensor_id // 1000
            idx  = 64 * (dice - 1) + sensor_id % 1000
            file.write(f"{sensor_id} {x} {y} {dice} {idx}\n")

def create_el_mapping(el_dict, output_filename):
    with open(output_filename, "w") as file:
        file.write("PointID X Y\n")
        for point_id, (x, y) in sorted(el_dict.items()):
            file.write(f"{point_id} {x} {y}\n")

def split_table_columns(input_filename, output_filename):
    with open(output_filename, "w") as file:
        file.write("PointID SensorID Prob\n")
        for i, line in enumerate(open(input_filename)):
            if not i: continue
            point_id, *probs = line.rstrip().split()
            lines = [f"{point_id} {pmt_no} {prob}" for pmt_no, prob in enumerate(probs)]
            file.write("\n".join(lines) + "\n")


print("Creating active map...", end="", flush=True)
active_mapping = os.path.join(s1_path, "active_mapping.dat")
create_active_mapping(active_map, active_mapping)
print("OK")

print("Creating pmt map...", end="", flush=True)
pmt_mapping = os.path.join(s1_path, "pmt_mapping.dat")
create_pmt_mapping(PMT_map, corona_map, PMT_phi_map, pmt_mapping)
print("OK")

print("Creating sipm map...", end="", flush=True)
sipm_mapping = os.path.join(s1_path, "sipm_mapping.dat")
create_sipm_mapping(SiPM_map, sipm_mapping)
print("OK")

print("Creating el map...", end="", flush=True)
el_mapping = os.path.join(s1_path, "el_mapping.dat")
create_el_mapping(EL_map, el_mapping)
print("OK")

print("Reshaping S1 table...", end="", flush=True)
s1_table_in  = os.path.join(s1_path, "S1table_original.dat")
s1_table_out = os.path.join(s1_path, "S1table.dat")
#split_table_columns(s1_table_in, s1_table_out)
print("OK")
