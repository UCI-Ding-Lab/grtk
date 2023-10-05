import numpy as np

def gparse(H: bool, arg: str, raw: str) -> str:
    """GRTK INPUT PARSING

    Args:
        arg (str): any format, but must contain data.
        raw (str): standard format, splitlines

    Returns:
        str: _description_
    """
    if H:
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
        for key, val in allCurves.items():
            print(key, val)
    else:
        fm = arg.split(",")
        


if __name__ == "__main__":
    with open("./UCSD_Data/001") as f:
        gparse(True, "time,c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26,c27,c28,c29,c30,c31,c31,c33,c34,c35",f.read())
        # gparse(False, "-x10,name,time,data")