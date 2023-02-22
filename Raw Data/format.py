import pathlib
with open(pathlib.Path("/Users/tiger/Documents/Github/grtk/raw/303.gr"), "r") as file:
    b = file.readlines()
with open(pathlib.Path("/Users/tiger/Documents/Github/grtk/raw/formatted303.gr"), "w") as file:
    for i in range(len(b)):
        file.write(f"{i} {b[i]}")