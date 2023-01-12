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

FileDynBathy = "Transect_1_DynBathy_0010_at_20100801_001000.txt"
FileHwave = "Transect_1_Hwave_0010_at_20100801_001000.txt"
FileTM02 = "Transect_1_TM02_0010_at_20100801_001000.txt"
FileZeta = "Transect_1_ZetaOcean_0010_at_20100801_001000.txt"
FileZetaSetup = "Transect_1_ZetaSetup_0010_at_20100801_001000.txt"

RecHwave = ReadFile(FileHwave)
RecZetaSetup = ReadFile(FileZetaSetup)

