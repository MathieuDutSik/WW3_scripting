import matplotlib.pyplot as plt
from math import pi, sqrt, sinh, tanh
import os

def ReadFile(FileI):
    f = open(FileI, "r")
    l_lines = f.readlines()
    f.close()
    #
    ListX = []
    ListVal = []
    for i in range(1,len(l_lines)):
        e_lineA = l_lines[i]
        e_lineB = e_lineA.rstrip()
        LStr = e_lineB.split("; ")
        eX = float(LStr[0])
        eVal = float(LStr[1])
        ListX.append(eX)
        ListVal.append(eVal)
    return [ListX, ListVal]

def GetKvectorExact(eOmega, eDep):
    gAccel = 9.81
    eProd = eOmega*eOmega*eDep/gAccel
    eProd2 = eProd * eProd
    eProd4 = eProd2 * eProd2
    eProd5 = eProd * eProd4;
    aux1 = 1 + 0.6522 * eProd + 0.4622 * eProd2 + 0.0864 * eProd4 + 0.0675 * eProd5
    aux2 = 1/(eProd + 1 / aux1)
    wc = sqrt(gAccel*(aux2 * eDep))
    eK = eOmega / wc
    eKexact = eK
    for iter in range(200):
        eKexact = (eOmega*eOmega/gAccel) / tanh(eKexact*eDep)
    return eKexact

ePrefix = "WW3_transect/"

FileDynBathy = ePrefix + "Transect_1_DynBathy_0010_at_20100801_001000.txt"
FileHwave = ePrefix + "Transect_1_Hwave_0010_at_20100801_001000.txt"
FileTM02 = ePrefix + "Transect_1_TM02_0010_at_20100801_001000.txt"
FileZeta = ePrefix + "Transect_1_ZetaOcean_0010_at_20100801_001000.txt"
FileZetaSetup = ePrefix + "Transect_1_ZetaSetup_0010_at_20100801_001000.txt"

RecHwave = ReadFile(FileHwave)
RecTM02 = ReadFile(FileTM02)
RecZetaSetup = ReadFile(FileZetaSetup)
RecDynBathy = ReadFile(FileDynBathy)

ListLon = RecHwave[0]
EarthRadius = 6371 * 1000
ListX = [EarthRadius * x for x in ListLon]
ListWW3_Hwave = RecHwave[1]
ListWW3_ZetaSetup = RecZetaSetup[1]
deltaX = ListX[1] - ListX[0]

aHS = RecHwave[1][0]
TM02 = RecTM02[1][0]
eOmega = 2 * pi / TM02

alphaBreakingHS=0.81;
DynBathy = RecDynBathy[1]
n_ent = len(DynBathy)

while(True):
    ListKexact = [GetKvectorExact(eOmega, eDep) for eDep in DynBathy]
    kD = [ListKexact[u] * DynBathy[u] for u in range(n_ent)]
    Lwave = [2 * pi / ListKexact[u] for u in range(n_ent)]
    nNumber = [0.5 + e_kD / sinh(e_kD) for e_kD in kD]
    cPhase = [eOmega * eK for eK in ListKexact]
    cGroup = [cPhase[u] * nNumber[u] for u in range(n_ent)]
    #
    Cst = aHS * aHS * cGroup[0]
    ListHnobreak = [sqrt(Cst/eGroup) for eGroup in cGroup]
    MaxBreaking = [alphaBreakingHS*eDynBathy for eDynBathy in DynBathy]
    ListIdeal_Hwave = [min(ListHnobreak[u], MaxBreaking[u]) for u in range(n_ent)]
    ListHmono = [eH / sqrt(2) for eH in ListIdeal_Hwave]
    ListK = [2 * eN - 0.5 for eN in nNumber]
    ListSxx = [eH * eH * eK / 16 for eH, eK in zip(ListIdeal_Hwave, ListK)]
    TheDifferential = [(ListSxx[u+1] - ListSxx[u]) / deltaX for u in range(n_ent-1)]
    #
    ListIdeal_ZetaSetup = [0] * n_ent
    for u in range(n_ent-1):
        Dmid = (DynBathy[u] + DynBathy[u+1]) / 2
        TheDiff = - TheDifferential[u] / Dmid
        ListIdeal_ZetaSetup[u+1] = ListIdeal_ZetaSetup[u] - TheDiff * deltaX
    break


DoPlot = True
def plot_pairs(List_WW3, List_Ideal, eName):
    plt.figure(figsize=(14,10))
    plt.plot(ListX, List_WW3, label="WW3", color = "C0")
    plt.plot(ListX, List_Ideal, label="Ideal", color = "C1")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylabel(eName, fontsize=14)
    plt.legend(fontsize=14)
    plt.grid(True,alpha=0.3)
    plt.tight_layout()
    FileSave = eName + ".png"
    plt.savefig(FileSave)
    plt.close('all')

def plot_single(ListVal, eName):
    plt.figure(figsize=(14,10))
    plt.plot(ListX, ListVal, label=eName, color = "C0")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylabel(eName, fontsize=14)
    plt.legend(fontsize=14)
    plt.grid(True,alpha=0.3)
    plt.tight_layout()
    FileSave = eName + ".png"
    plt.savefig(FileSave)
    plt.close('all')

if DoPlot:
    plot_pairs(ListWW3_Hwave, ListIdeal_Hwave, "Hwave")
    plot_pairs(ListWW3_ZetaSetup, ListIdeal_ZetaSetup, "ZetaSetup")
    plot_single(ListKexact, "Kexact")
    plot_single(DynBathy, "DynBathy")
    plot_single(cPhase, "cPhase")
    plot_single(cGroup, "cGroup")


