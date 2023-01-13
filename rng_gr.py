import random

def twenty_megabytes():
    lines = 1400000
    with open("big_test_data.gr", "w") as file:
        file.writelines([f"{int(i)} {random.randint(1,999999)}\n" for i in range(lines)])