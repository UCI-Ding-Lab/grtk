import numpy as np
import os
import pathlib

class gparse(object):
    def __init__(self):
        self.seperator: str = "-"*10
        self.debug: bool = False
        self.time_str: str = "time"
        self.default_curveType: str = "data"
        self.type_indicator: str = "_"
        self.delete_curveType: str = "del"
        self.newFile_suffix: str = "_parsed.gr"
        self.default_combinedFile: str = "all.gr"
    
    def set_seperator(self, name: str) -> bool:
        if name == "":
            raise ValueError("No Value")
        self.seperator = name
        return True
    
    def set_timeStr(self, name: str) -> bool:
        if name == "":
            raise ValueError("No Value")
        self.time_str = name
        return True
    
    def set_defaultCurveType(self, name: str) -> bool:
        if name == "":
            raise ValueError("No Value")
        self.default_curveType = name
        return True
    
    def set_typeIndicator(self, name: str) -> bool:
        if name == "":
            raise ValueError("No Value")
        self.type_indicator = name
        return True
    
    def set_deleteCurveType(self, name: str) -> bool:
        if name == "":
            raise ValueError("No Value")
        self.delete_curveType = name
        return True
    
    def set_newFile_suffix(self, name: str) -> bool:
        if name == "":
            raise ValueError("No Value")
        if ".gr" not in name:
            print("WARN: Include .gr suffix to run in GRTK")
        self.newFile_suffix = name
        return True
    
    def set_defaultCombinedFile(self, name: str) -> bool:
        if name == "":
            raise ValueError("No Value")
        if ".gr" not in name:
            print("WARN: Include .gr suffix to run in GRTK")
        self.default_combinedFile = name
        return True
    
    def proc_group(self, files: list[str], features: list[str], new_fileName: str=None) -> None:
        for file in files:
            self.proc_single(file, features, new_fileName)

    def proc_single(self, file: str, features: list[str], new_fileName: str=None) -> None:
        allCurves: dict[str,np.ndarray] = {}
        with open(pathlib.Path(file), "r") as raw:
            toList: list[str] = raw.read().split("\n")
        rowCount: int = len(toList)
        colCount: int = len(toList[0].split())
        if len(features) > colCount:
            raise ValueError("Features Overfit")
        elif len(features) < colCount:
            raise ValueError("Features Underfit")
        if self.time_str not in features:
            raise ValueError("Time Str Not Given")
        proc = np.empty([rowCount,colCount])
        for indRow, Row in enumerate(toList):
            for indCol, Col in enumerate(Row.split()):
                proc[indRow,indCol] = float(Col)
        for indRow in range(colCount):
            allCurves[features[indRow]] = proc.T[indRow]
        build: dict[str,np.ndarray] = {}
        for key, val in allCurves.items():
            if key != self.time_str:
                build[key] = np.vstack((allCurves["time"],val)).T
        if new_fileName != None:
            parsedFile = open(pathlib.Path(new_fileName), "w")
        else:
            parsedFile = open(pathlib.Path(file+self.newFile_suffix), "w")
        empty: bool = True
        for key, val in build.items():
            rows = ["{} {}".format(a, b) for a, b in build[key]]
            if self.type_indicator not in key:
                curveType = self.default_curveType
                curveName = key
            elif self.type_indicator+self.delete_curveType in key:
                rows = None
                continue
            elif self.type_indicator in key:
                curveType = key.split(self.type_indicator)[1]
                curveName = key.split(self.type_indicator)[0]
            if empty:
                text = "\n".join([curveType,curveName,"\n".join(rows)]) + "\n"
                parsedFile.write(text)
                empty = False
            else:
                text = "\n".join([self.seperator,curveType,curveName,"\n".join(rows)]) + "\n"
                parsedFile.write(text)
        parsedFile.close()
        if new_fileName != None:
            print(f"DONE: {pathlib.Path(new_fileName)}")
        else:
            print(f"DONE: {pathlib.Path(file+self.newFile_suffix)}")
    
    def proc_combineDirectory(self, dir: str, new_fileName: str=None) -> None:
        buf = ""
        for filename in os.listdir(dir):
            if filename.endswith(".DS_Store"):
                continue
            with open(os.path.join(dir, filename)) as f:
                buf += f.read()+"\n"
        if new_fileName != None:
            with open(os.path.join(dir, new_fileName),"w") as f:
                f.write(buf)
        else:
            with open(os.path.join(dir, self.default_combinedFile),"w") as f:
                f.write(buf)
    
    def get_shape(self, file: str) -> tuple[int]:
        with open(pathlib.Path(file), "r") as raw:
            toList: list[str] = raw.read().split("\n")
        rowCount: int = len(toList)
        colCount: int = len(toList[0].split())
        return (rowCount, colCount)


if __name__ == "__main__":
    a = gparse()
    a.proc_single(
        "./UCSD_Data/000",
        [
            "time",
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "21",
            "22",
            "23",
            "24",
            "25",
            "26",
            "27",
            "28",
            "29",
            "30",
            "31",
            "32",
            "33",
            "34",
            "35"
        ]
    )
    print(a.get_shape("./UCSD_Data/000"))
        