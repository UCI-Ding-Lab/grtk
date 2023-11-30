import pathlib
import os
import numpy as np

class SaveManager():
    def __init__(self, GUI=None):
        self.GUI = GUI

    def _create_datafile(self, df_path: str) -> None:
        fp = pathlib.Path(df_path)
        if fp.exists():
            os.remove(fp)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.touch()
        return None
    
    def _save(self, container, df_path: str) -> None:
        curves_list = container.get_curves_list()
        with open(df_path, 'w') as f:
            for i in curves_list:
                f.write("--curve\n")
                f.write(f"file_path={i[0]}\n")
                f.write(f"type={i[1]}\n")
                f.write(f"curve_id={i[2]}\n")
                f.write(f"pref_show_on_graph={i[3]}\n")
                f.write(f"pref_line_color={i[4]}\n")
                f.write(f"pref_line_size={i[5]}\n")
                f.write(f"pref_marker_style={i[6]}\n")
                f.write(f"pref_marker_size={i[7]}\n")
                f.write(f"pref_marker_face_color={i[8]}\n")
                f.write(f"pref_marker_edge_color={i[9]}\n")
                f.write(f"tip={i[10]}\n")
                f.write("coords(x,y)=\n")
                for x, y in i[11]:
                    # f.write(f"{j[0]},{j[1]}\n")
                    # f.write(f"{j},{i[11][1][j]}\n")
                    f.write(f"{x},{y}\n")
                f.write("--end\n")
        return None
  
    def save(self, container, df_path: str) -> None:
        self._save(container, df_path)
        return None
    
    def _fetch_curves(self, df_path: str) -> list:
        prefs = []
        coords = []
        
        with open(df_path, 'r') as f:
            temp_pref = []
            temp_coords = []
            lines = f.readlines()
            for line in lines:
                # processed_line = line.rstrip('\n')
                processed_pref = line.rstrip('\n').split("=")
                processed_coords = line.rstrip('\n').split(",")
                if line == "--curve\n":
                    temp_pref = []
                    continue
                elif line == "coords(x,y)=\n":
                    temp_coords = []
                    continue
                elif len(processed_pref) == 2 and '' not in processed_pref:
                    # print(f"SMtest::{processed_pref}")
                    if processed_pref[1][0] == "(" and processed_pref[1][-1] == ")":
                        temp_processed = processed_pref[1][1:len(processed_pref[1])-1].split(",")
                        processed_pref[1] = []
                        for i in temp_processed:
                            processed_pref[1].append(float(i))
                        processed_pref[1] = tuple(processed_pref[1])
                    temp_pref.append(processed_pref[1])
                elif len(processed_coords) == 2:
                    temp_coords.append([float(processed_coords[0]), float(processed_coords[1])])

                elif line == "--end\n":
                    coords.append(temp_coords.copy())
                    temp_coords = []
                if len(temp_pref) >= 11:
                    prefs.append(temp_pref.copy())
                    temp_pref = []
        # coords=np.array(coords, ndmin=3)
        # print(coords.shape)
        # print(coords[:2])
        # print(coords[0][0])
        # coords = np.array(coords)
        return prefs, coords
    
    def fetch_curves(self, df_path: str) -> list:
        return self._fetch_curves(df_path)