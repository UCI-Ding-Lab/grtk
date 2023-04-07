import re

with open("/Users/tiger/Downloads/303 bd1 0.475 smooth choice ASCII.gr", "r") as f:
    r = re.compile(r'\[(.*?)\](.*)')
    settings = {}
    for line in f:
        if r.match(line) is not None:
            current = r.match(line).group(1)
            settings[current] = []
            continue
        elif line != "\n":
            settings[current].append(line[:-1].split(" "))