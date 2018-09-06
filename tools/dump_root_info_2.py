import string
import sys
import contextlib
import ROOT
import pandas

@contextlib.contextmanager
def root_open(filename, *args, **kwargs):
    file = ROOT.TFile(filename, *args, **kwargs)
    yield file
    file.Close

if __name__ == "__main__":
    input_filename   = "/Users/Gonzalo/github/elparametrization/PyScripts/ParamBuilder/output/NEXT100_S2PMTparametrization_plots.root"
    output_filename  = "root_dump.dat"
    pmt_filename_data = output_filename.replace(".", "_pmt_data.")
    pmt_filename_fit  = output_filename.replace(".", "_pmt_fit." )
    pul_filename      = output_filename.replace(".", "_pmt_pull." )

    polynomial_degree_1 = 5
    polynomial_degree_2 = 6
    
    with root_open(input_filename)           as      input_file     , \
              open(  pmt_filename_data, "w") as pmt_output_file_data, \
              open(  pmt_filename_fit , "w") as pmt_output_file_fit , \
              open(  pul_filename     , "w") as pul_output_file:

        pmt_output_file_data.write("sensor_id r prob many\n")
        pmt_output_file_fit .write("sensor_id dr_coeff value uncert\n")
        pul_output_file     .write("pmt pull many\n")
        
        for key in input_file.GetListOfKeys():
            plot  = key .ReadObj ()
            name  = plot.GetName ().split(";")[0]
            title = plot.GetTitle().split(";")[0]
            print(repr(name), repr(title))

            if name.startswith("PMT"): # P vs R plots
                if "profile" in name: continue

                sensor_id = int(name.split(" ")[1])
                xaxis     = plot.GetXaxis()
                yaxis     = plot.GetYaxis()
                xaxisn    = plot.GetNbinsX()
                yaxisn    = plot.GetNbinsY()
                xaxisc    = [xaxis.GetBinCenter(i   ) for i in range(1, xaxisn + 1)]
                yaxisc    = [yaxis.GetBinCenter(   j) for j in range(1, yaxisn + 1)]
                for i in range(xaxisn):
                    ir = xaxisc[i]
                    for j in range(yaxisn):
                        ip   = yaxisc[j]
                        many = plot.GetBinContent(i + 1, j + 1)

                        s = "{sensor_id} {ir} {ip} {many}\n".format(**locals())
                        pmt_output_file_data.write(s)

            elif name.startswith("fit"): # Coeff vs Z plots
                numbers   = []
                save      = False
                current   = ""
                sensor_id = int(name.split("_")[1])

                sign      = "+"
                for k, char in enumerate(title):
                    if char == "(" and k and title[k-1] in "+-":
                        sign = title[k-1]
                    if char in string.digits + ".e-+":
                        save = True
                        current = current + char
                    if char in "*()":
                        if len(current) > 3:
                            numbers.append(float(sign + current))
                        current = ""
                        save = False

                first  = numbers[:polynomial_degree_1 + 1 ]
                second = numbers[ polynomial_degree_1 + 1:]

                for ic in range(polynomial_degree_1 + 1):
                    ip = numbers[ic]
                    iu = 0
                    s = "{sensor_id} {ic} {ip} {iu}\n".format(**locals())
                    pmt_output_file_fit.write(s)

                for ic in range(polynomial_degree_1 + 1, polynomial_degree_1 + polynomial_degree_2 + 2):
                    ip = numbers[ic]
                    iu = 0
                    s = "{sensor_id} {ic} {ip} {iu}\n".format(**locals())
                    pmt_output_file_fit.write(s)

            elif name.startswith("pull") and "vs" not in name:
                pmt = name.split(" ")[-1]
                if pmt == "summed": pmt = -1
                for i in range(1, plot.GetNbinsX() + 1):
                    pull = plot.GetXaxis().GetBinCenter (i)
                    many = plot           .GetBinContent(i)
                    s = "{pmt} {pull} {many}\n".format(**locals())
                    pul_output_file.write(s)
            else:
                pass


