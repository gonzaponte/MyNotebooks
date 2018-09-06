import shutil

def fix_file_cathode(filename):
    print(f"Reading {filename}...")
    file_data = open(filename, "r").read()
    modified  = False

    if str.isdigit(file_data[0]):
        print(f"Adding header...")
        header    = "Dummy PointID SensorID P0 P1 P2 P3 P4 P5 P6 P7 P8 P9 P10 P11 P12 P13 P14 P15 P16 P17 P18 P19\n"
        file_data = header + file_data 
        modified  = True

    if " \n" in file_data:
        print(f"Removing trailing whitespaces...")
        file_data = file_data.replace(" \n", "\n")
        modified  = True

    if modified:
        print(f"Writing data back to {filename}...")
        open(filename, "w").write(file_data)
    print("Done!")

def fix_file_anode(filename):
    filename_temp = filename + "_temp"
    print(f"Reading {filename}...")
    with open(filename, "r", ) as file_in:
        with open(filename_temp, "w") as file_out:
            for i, line in enumerate(file_in):
                if not i and str.isdigit(line[0]):
                    print(f"Adding header...")
                    header    = "Dummy PointID SensorID P0 P1\n"
                    file_out.write(header)
                    continue
                if " \n" in line:
                    line = line.replace(" \n", "\n")

                file_out.write(line)
    shutil.move(filename_temp, filename)
    print("Done!")
    
cathode_filename = "/Volumes/SAMSUNG/NEXT100tables/S2/Cathode.dat"
anode_filename   = "/Volumes/SAMSUNG/NEXT100tables/S2/Anode.dat"


#fix_file_cathode(cathode_filename)
fix_file_anode  (anode_filename)