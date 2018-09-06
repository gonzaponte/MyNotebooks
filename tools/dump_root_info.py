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
#    input_filename   = "/Users/Gonzalo/github/elparametrization/PyScripts/ParamBuilder/output/NEW_S1parametrization_plots_zshift.root"
    input_filename   = "/Users/Gonzalo/github/elparametrization/PyScripts/ParamBuilder/output/NEXT100_S1parametrization_plots_zshift.root"
    output_filename  = "root_dump.dat"
    dr_filename_data = output_filename.replace(".", "_dr_data.")
    dr_filename_fit  = output_filename.replace(".", "_dr_fit." )
    zz_filename_data = output_filename.replace(".", "_z_data." )
    zz_filename_fit  = output_filename.replace(".", "_z_fit."  )
    pl_filename      = output_filename.replace(".", "_pull."   )

#    polynomial_degree_dr = 2
#    polynomial_degree_z  = 4
    polynomial_degree_dr = 4
    polynomial_degree_z  = 6
    
    with root_open(input_filename)           as     input_file     , \
              open(   dr_filename_data, "w") as dr_output_file_data, \
              open(   dr_filename_fit , "w") as dr_output_file_fit , \
              open(   zz_filename_data, "w") as zz_output_file_data, \
              open(   zz_filename_fit , "w") as zz_output_file_fit , \
              open(   pl_filename     , "w") as pl_output_file:

        dr_output_file_data.write("ring dphi z dr prob uncert\n")
        dr_output_file_fit .write("ring dphi z dr_coeff value uncert\n")
        zz_output_file_data.write("ring dphi dr_coeff z value uncert\n")
        zz_output_file_fit .write("ring dphi dr_coeff z_coeff value uncert\n")
        pl_output_file     .write("r z pull many\n")
        
        for key in input_file.GetListOfKeys():
            plot  = key .ReadObj ()
            title = plot.GetTitle().split(";")[0]
            print(repr(title))

            if title.startswith("corona"): # P vs dR plots
                if "pull" in title: continue
                if "c1"   in title: continue

                dr  = plot.GetX ()
                p   = plot.GetY ()
                u   = plot.GetEY()
                fit = plot.GetFunction("pol{}".format(polynomial_degree_dr))

                ring = int(      title.split(",")[0].split(" ")[1])
                z    = int(      title.split(",")[1].split(" ")[3])
                dphi = int(float(title.split(",")[2].split(" ")[3])) // 40
#                z    = 275 - z
                z    = 640 - z

                for i in range(plot.GetN()):
                    idr = dr[i]
                    ip  =  p[i]
                    iu  =  u[i]
                    s   = "{ring} {dphi} {z} {idr} {ip} {iu}\n".format(**locals())
                    dr_output_file_data.write(s)

                for ic in range(polynomial_degree_dr + 1):
                    ip = fit.GetParameters()[ic]
                    iu = fit.GetParErrors ()[ic]
                    s  = "{ring} {dphi} {z} {ic} {ip} {iu}\n".format(**locals())
                    dr_output_file_fit.write(s)
                    

            elif title.startswith("z fit"): # Coeff vs Z plots
                z   = plot.GetX ()
                c   = plot.GetY ()
                u   = plot.GetEY()
                fit = plot.GetFunction("pol{}".format(polynomial_degree_z))
                
                ring = int(title.split(" ")[3])
                drc  = int(title.split(" ")[5])
                dphi = int(title.split(" ")[7])
                
                for i in range(plot.GetN()):
                    iz = z[i]
                    ic = c[i]
                    iu = u[i]
                    s = "{ring} {dphi} {drc} {iz} {ic} {iu}\n".format(**locals())
                    zz_output_file_data.write(s)

                for ic in range(polynomial_degree_z + 1):
                    ip = fit.GetParameters()[ic]
                    iu = fit.GetParErrors ()[ic]
                    s = "{ring} {dphi} {drc} {ic} {ip} {iu}\n".format(**locals())
                    zz_output_file_fit.write(s)

            elif title == "pull":
                for i in range(1, plot.GetNbinsX() + 1):
                    pull = plot.GetXaxis().GetBinCenter (i)
                    many = plot           .GetBinContent(i)
                    s = "nan nan {pull} {many}\n".format(**locals())
                    pl_output_file.write(s)

            elif title == "pull vs z":
                for i in range(1, plot.GetNbinsX() + 1):
                    for j in range(1, plot.GetNbinsY() + 1):
                        z    = plot.GetXaxis().GetBinCenter(i)
                        pull = plot.GetYaxis().GetBinCenter(j)
                        many = plot           .GetBinContent(i, j)
                        s = "nan {z} {pull} {many}\n".format(**locals())
                        pl_output_file.write(s)

            elif title == "pull vs r":
                for i in range(1, plot.GetNbinsX() + 1):
                    for j in range(1, plot.GetNbinsY() + 1):
                        r    = plot.GetXaxis().GetBinCenter(i)
                        pull = plot.GetYaxis().GetBinCenter(j)
                        many = plot           .GetBinContent(i, j)
                        s = "{r} nan {pull} {many}\n".format(**locals())
                        pl_output_file.write(s)
                
            else:
                pass


