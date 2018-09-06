import os
import glob

s1_path = "/Volumes/SAMSUNG/NEWtables/S1/"

# Defines active_map
exec(open(os.path.join(s1_path, "active_map.py")).read())
active_map_2 = {i: ( -215 + 10.* ((i% 1936)//44),
                     -215 + 10 * ((i% 1936)% 44),
                     -300 + 10 * ( i//1936)    )  for i in range(118096)}

reverse_active_map = {tuple(map(int, val)): key for key, val in active_map.items()}

def create_active_mapping(active_dict, output_filename):
    with open(output_filename, "w") as file:
        file.write("PointID X Y Z\n")
        for point_id, (x, y, z) in sorted(active_dict.items()):
            file.write(f"{point_id} {x} {y} {z}\n")    

def split_table_columns_v0(input_filename, output_filename):
    with open(output_filename, "w") as file:
        file.write("PointID SensorID Prob\n")
        for i, line in enumerate(open(input_filename)):
            if not i: continue
            point_id, *probs = line.rstrip().split()
            lines = [f"{point_id} {pmt_no} {prob}" for pmt_no, prob in enumerate(probs)]
            file.write("\n".join(lines) + "\n")

def split_table_columns_v1(input_filename, output_filename):
    with open(output_filename, "w") as file:
        file.write("PointID SensorID Prob\n")
        for i, line in enumerate(open(input_filename)):
            if not i: continue
            index, x, y, z, *probs = line.rstrip().split()
            point_id = reverse_active_map[tuple(map(int, (x, y, z)))]
            lines = [f"{point_id} {pmt_no} {prob}" for pmt_no, prob in enumerate(probs)]
            file.write("\n".join(lines) + "\n")

def merge_minitables(input_filenames, output_filename):
    with open(output_filename, "w") as output_file:
        output_file.write("X Y Z SensorID Prob\n")
        for filename in input_filenames:
            file_data = open(filename).read()
            if file_data[-1] != "\n": file_data = file_data + "\n"
            output_file.write(file_data)
    
print("Creating active map...", end="", flush=True)
active_mapping = os.path.join(s1_path, "active_mapping.dat")
#create_active_mapping(active_map, active_mapping)
print("OK")

print("Creating active map...", end="", flush=True)
active_mapping = os.path.join(s1_path, "active_mapping_2.dat")
#create_active_mapping(active_map_2, active_mapping)
print("OK")

print("Reshaping S1 table...", end="", flush=True)
s1_table_in  = os.path.join(s1_path, "S1_old", "S1tableFULL.dat")
s1_table_out = os.path.join(s1_path, "S1_old", "S1table.dat")
#split_table_columns_v0(s1_table_in, s1_table_out)
print("OK")

print("Reshaping S1 table...", end="", flush=True)
s1_table_in  = os.path.join(s1_path, "S1_august2017", "S1TableAugust2017_V1.txt")
s1_table_out = os.path.join(s1_path, "S1_august2017", "S1table.dat")
#split_table_columns_v1(s1_table_in, s1_table_out)
print("OK")

print("Reshaping S1 table...", end="", flush=True)
s1_table_in  = os.path.join(s1_path, "S1_fnal", "S1table_original.dat")
s1_table_out = os.path.join(s1_path, "S1_fnal", "S1table.dat")
#split_table_columns_v0(s1_table_in, s1_table_out)
print("OK")

print("Merging S1 tables...", end="", flush=True)
s1_files_in  = glob.glob(os.path.join(s1_path, "S1_fnal", "table_X*_Y*.dat"))
s1_table_out = os.path.join(s1_path, "S1_fnal", "S1table_merged.dat")
merge_minitables(s1_files_in, s1_table_out)
print("OK")
