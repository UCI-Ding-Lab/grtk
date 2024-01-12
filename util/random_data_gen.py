# Random Data Generator
import numpy as np
import gzip
use_gzip = bool(int(input("use gzip? (1/0): ")))
if use_gzip:
    f = gzip.open("rand_gen.gz", "wt")
else:
    f = open("rand_gen.gr", "w")

start = float(input("start from: "))
end = float(input("end at: "))
step = float(input("step: "))
curve_num = int(input("number of curves: "))
spacer = int(input("spacer: "))
latitude = int(input("latitude: "))

minimum = 0
# for each curve, ask for maximum and minimum and name
for i in range(curve_num):
    x = np.arange(start, end, step)
    # count decimal places for step
    decimal = 0
    if "." in str(step):
        decimal = len(str(step).split(".")[1])
    # round to decimal places
    x = np.round(x, decimal)
    # generate random y
    maximum = minimum + latitude
    y = np.random.randint(minimum, maximum, len(x))
    # write x y  to file
    for j in range(len(x)):
        f.write(f"{x[j]} {y[j]}\n")
    minimum = maximum + spacer
    print(f"-> curve {i+1} generated")
# build closing line
strin = f"[GRTK],{int(len(x))},"
for i in range(curve_num):
    strin += f"data/{i+1},"
strin = strin[:-1]
f.write(strin)
f.close()
print("-> file generated")