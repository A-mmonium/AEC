import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Gabriel sujol lerchbacher
#File naming should be as "01M/10M""thickness/100"CP_"current density" or "1M/10M"OCP_begi/"current density" ex: "01M04CP_05.txt"
#Rc and Ra resistance should be entered manualy when prompted

input("Make sure files are properly formated and in the same directroy as this script, press enter to continue") #Initial set up

while True:
    suffix_Cp=["05","10","20","40","80","160","320"]
    suffix_Ocp=["05","10","20","40","80","160","320"]
    cons = input("KOH concentration (01M or 10M)?")
    prefix = cons+"M"
    thick = input("Thickness? (04, 08, 16)")
    prefix += thick

    yphi_c=[] #agregated vectors for 05 10... 80
    yphi_a =[]
    yeta_c =[]
    yeta_a=[]

    errphi_c=[] #error vectors
    errphi_a =[]
    erreta_c =[]
    erreta_a=[]

    res_c = float(input("Cathode resistance (must be number with . in OHM (0.12))")) #get resistance values
    res_a = float(input("Anode resistance (must be number with . in OHM (0.15))"))


    for i in range(len(suffix_Cp)): #File name builder loop as weel as base ploter and aggregator
        I = 5*2**(i)/1000 #current

        CP = prefix+"CP_"+suffix_Cp[i]+".txt" #filename constructor
        OCP = prefix+"OCP_"+suffix_Ocp[i]+".txt"

        data = pd.read_csv(OCP, sep="\t" ,decimal=',',thousands='.') #Load ocp and takes offsets
        data = data.iloc[1: ,:]
        df = data[["Vf7","Vf8"]]
        df.set_index(data["T"])
        df=df.apply(lambda x: x.str.replace(',','.')).astype(float)

        Rc_cor =df["Vf7"].tail(151).mean()
        Ra_cor =df["Vf8"].tail(151).mean()

        data = pd.read_csv(CP, sep="\t" ,decimal=',',thousands='.') #Load cp and gives data frame
        data = data.iloc[1: ,:]
        df = data[["Vf","Vf1","Vf2","Vf3","Vf4","Vf5","Vf6","Vf7","Vf8"]]
        df.set_index(data["T"])
        df=df.apply(lambda x: x.str.replace(',','.')).astype(float)


        df["Phic"]=-df["Vf7"] - I*res_c + Rc_cor#i*Rc #apply correction
        df["Phia"]=df["Vf8"] - I*res_a - Ra_cor #i*Ra

        df["etac"]=df["Vf1"] + I*res_c #i*Rc
        df["etaa"]=df["Vf2"] - I*res_a - 1.23 #i*Ra-equi potenetial oxygen evolution vs rhe



        dfz = df[["Phic","Phia","etac","etaa"]].copy() #plot the cp with ocp correction and displays to make sure the data is healthy
        #plt = dfz.plot(grid=True,title=str(I)+"mA/cm-2 N2 purge "+cons+" "+thick,xlabel="Time",ylabel="Voltage")
        #print("Rc"+str(Rc_cor))
        #print("Ra"+str(Ra_cor))
        #print(dfz["Phic"].tail(151).sd())
        #plt.legend(["φc "+str(np.round(dfz["Phic"].mean(),2)),"φa "+str(np.round(dfz["Phia"].mean(),2)),"ηc "+str(np.round(dfz["etac"].mean(),2)),"ηa "+str(np.round(dfz["etaa"].mean(),2))],bbox_to_anchor=(1.02, 1), loc='upper left')
        #fig = plt.get_figure()
        #fig.set_size_inches(18.5, 10.5, forward=True)
        #fig.savefig(cons+"_"+current+"_"+thick+".jpg")
        #input("Does everything seem fine?")

        yphi_c.append(dfz.tail(151).copy().mean().to_numpy()[0]) #aggregates the data to a list, the average of the last minute
        yphi_a.append(dfz.tail(151).copy().mean().to_numpy()[1])
        yeta_c.append(dfz.tail(151).copy().mean().to_numpy()[2])
        yeta_a.append(dfz.tail(151).copy().mean().to_numpy()[3])

        errphi_c.append(dfz["Phic"].tail(151).std())
        errphi_a.append(dfz["Phia"].tail(151).std())
        erreta_c.append(dfz["etac"].tail(151).std())
        erreta_a.append(dfz["etaa"].tail(151).std())


    thick += "00μm"
    x = [5,10,20,40,80,160,320] #current density x axis
    # print(yphi_c)
    # print(yphi_a)
    # print(yeta_c)
    # print(yeta_a)


    plt.figure(figsize=(8,5))
    plt.errorbar(x,yphi_c,c="red",linestyle="dotted",label="φc",yerr=errphi_c, ecolor = 'black',capsize=3)
    plt.errorbar(x,yphi_a,c="blue",linestyle="dotted",label="φa",yerr=errphi_a, ecolor = 'black',capsize=3)
    plt.errorbar(x,yeta_c,yerr=erreta_c,c="red",label="ηc", ecolor = 'black',capsize=3)
    plt.errorbar(x,yeta_a,yerr=erreta_a,c="blue",label="ηa",ecolor = 'black',capsize=3)
    plt.legend()
    plt.title("Over potential and electrostatic voltage vs current density in N2 purge for "+cons+"M " +thick)
    plt.xlabel("Current (mA)")
    plt.ylabel("Voltage (V)")
    plt.grid(True)
    #fig = plot.get_figure()
    #fig.set_size_inches(18.5, 10.5, forward=True)
    plt.savefig("Over pot and electro stat vs current dens"+cons+"M "+thick+".jpg")


    inp = input("Load new sequence? Y/N")
    if inp.lower() == "n":
        break
#end of code
