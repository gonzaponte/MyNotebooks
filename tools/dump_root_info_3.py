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
    input_filename   = "/Users/Gonzalo/github/elparametrization/PyScripts/ParamBuilder/output/NEXT100_S2SiPMparametrization_plots.root"
    output_filename  = "root_dump.dat"
    sipm_filename_data = output_filename.replace(".", "_sipm_data.")
    sipm_filename_fit  = output_filename.replace(".", "_sipm_fit." )
    pul_filename      = output_filename.replace(".", "_sipm_pull." )

    polynomial_degree = 9
    with root_open(input_filename)           as      input_file     , \
              open(  sipm_filename_data, "w") as sipm_output_file_data, \
              open(  sipm_filename_fit , "w") as sipm_output_file_fit , \
              open(  pul_filename     , "w") as pul_output_file:

        sipm_output_file_data.write("bin dr prob uncert\n")
        sipm_output_file_fit .write("bin dr_coeff value uncert\n")
        pul_output_file     .write("bin pull many\n")
        
        for key in input_file.GetListOfKeys():
            plot  = key .ReadObj ()
            name  = plot.GetName ().split(";")[0]
            title = plot.GetTitle().split(";")[0]
            if "corr" in name: continue
            print(repr(name), repr(title))
            try:    bin = list(filter(str.isdigit, name))[0]
            except: bin = -1
            print(bin)

            if name.startswith("full"): # P vs R plots
                print(plot.GetN())
                ndata     = plot.GetN()
                xdata     = plot.GetX()
                ydata     = plot.GetY()
                udata     = plot.GetEY()
                for i in range(ndata):
                    x = xdata[i]
                    y = ydata[i]
                    u = udata[i]
                    s = "{bin} {x} {y} {u}\n".format(**locals())
                    sipm_output_file_data.write(s)

            elif name.startswith("fit"): # Coeff vs Z plots
                numbers   = []
                save      = False
                current   = ""
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

                for ic in range(polynomial_degree + 1):
                    c = numbers[ic]
                    u = 0
                    s = "{bin} {ic} {c} {u}\n".format(**locals())
                    sipm_output_file_fit.write(s)

            elif name.startswith("pull") and "vs" not in name:
                for i in range(1, plot.GetNbinsX() + 1):
                    pull = plot.GetXaxis().GetBinCenter (i)
                    many = plot           .GetBinContent(i)
                    s = "{bin} {pull} {many}\n".format(**locals())
                    pul_output_file.write(s)
            else:
                pass


