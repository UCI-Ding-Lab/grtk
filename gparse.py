import numpy as np
import os

def gparse(arg: str, raw: str, f: str, sep: str) -> str:
    """GRTK INPUT PARSING

    Args:
        arg (str): any format, but must contain data.
        raw (str): standard format, splitlines

    Returns:
        str: _description_
    """
    fm = arg.split(",")
    allCurves: dict[str,np.ndarray] = {}
    ## --- ##
    toList: list[str] = raw.split("\n")
    rowCount = len(toList)
    colCount = len(toList[0].split())
    if len(fm) != colCount:
        raise ValueError
    proc = np.empty([rowCount,colCount])
    for indRow, Row in enumerate(toList):
        for indCol, Col in enumerate(Row.split()):
            proc[indRow,indCol] = float(Col)
    ## --- ##
    for indRow in range(colCount):
        allCurves[fm[indRow]] = proc.T[indRow]
    ## --- ##
    build: dict[str,np.ndarray] = {}
    with open(f+"_parsed.gr","w") as fNew:
        empty = True
        for key, val in allCurves.items():
            if key != "time":
                build[key] = np.vstack((allCurves["time"],val)).T
                rows = ["{} {}".format(a, b) for a, b in build[key]]
                if "_" not in key:
                    curveType = "data"
                    curveName = key
                else:
                    curveType = key.split("_")[1]
                    curveName = key.split("_")[0]
                if empty:
                    text = "\n".join([curveType,curveName,"\n".join(rows)]) + "\n"
                    fNew.write(text)
                    empty = False
                else:
                    text = "\n".join([sep,curveType,curveName,"\n".join(rows)]) + "\n"
                    fNew.write(text)
    ## --- ##
    print("DONE:", f+"_parsed.gr")
        


if __name__ == "__main__":
    directory = './UCSD_Data'
    for filename in os.listdir(directory):
        if filename.endswith(".DS_Store"):
            continue
        with open(os.path.join(directory, filename)) as f:
            gparse("time,c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c31,c33,c34,c35",f.read(),f.name,"-"*10)
    
    # buf = ""
    # for filename in os.listdir(directory):
    #     if filename.endswith(".DS_Store"):
    #         continue
    #     with open(os.path.join(directory, filename)) as f:
    #         buf += f.read()+"\n"
    # with open(os.path.join(directory, "all.gr"),"w") as f:
    #     f.write(buf)
        