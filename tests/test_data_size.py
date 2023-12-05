import random
import struct
import time

def get_random_float():
    return random.uniform(0, 2000)

def get_float_list():
    float_list = []
    for i in range(190000*36): # 3 hours of data
        temp = []
        for j in range(36):
            temp.append(get_random_float())
        float_list.append(temp)
        temp = []
    return float_list

def save_text(data):
    with open('test_data.txt', 'w') as file:
        for i in data:
            # line = struct.pack('d'*len(i), *i)
            line = ""
            for j in i:
                line += f"{str(j)} "
            line += "\n"
            file.write(line)

def save_dat(data):
    """Save data in binary format (double).
        In Python, float is 64 bits, which is the 
        same as a double in C. So in other places of this 
        module, I used the term 'float' to refer to the 64 bit
        binary representation of floating point numbers.
        
        However, the struct.pack() function distinguishes double and 
        float in the concept of C. So please be aware.
    """
    with open('test_data.dat', 'wb') as file:
        for i in data:
            # 'd' stands for double (64 bit)
            # 'f' stands for float (32 bit) but comes with some data 
            #      loss after 2 or 3 decimal places.
            line = struct.pack('d'*len(i), *i)
            file.write(line)
            

def load_text(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            # Split the line into strings and convert each to float
            float_values = [float(x) for x in line.strip().split()]
            data.append(float_values)
    return data
    
def load_dat(filename):
    data = []
    with open(filename, 'rb') as file:
        while True:
            # Read 8 bytes (size of one double)
            bytes = file.read(8)
            if not bytes:
                break
            # Unpack the float, 'd' stands for double
            value = struct.unpack('d', bytes)[0]
            data.append(value)
    
    # Convert flat list to list of lists (assuming 36 floats per sublist)
    structured_data = [data[i:i + 36] for i in range(0, len(data), 36)]
    return structured_data

# Example usage
if __name__ == "__main__":
    """3 hours of data with 36 columns"""
    float_list = get_float_list()
    # print(float_list[0])
    
    # start_time = time.time()
    # save_text(float_list)
    # print("save_text::", "--- %s seconds ---" % (time.time() - start_time))
    
    """Takes roughly 12 seconds with a file size of 1.83 GB"""
    start_time = time.time()
    save_dat(float_list)
    print("save_dat::", "--- %s seconds ---" % (time.time() - start_time))
    
    # start_time = time.time()
    # data = load_text('test_data.txt')
    # print("load_text::", "--- %s seconds ---" % (time.time() - start_time))
    
    # print("text::", len(data))
    # print("text::", len(data[0]))
    # print("text::", data[0])
    
    """Takes roughly 217 seconds / 3.7 minutes"""
    start_time = time.time()
    data = load_dat('test_data.dat')
    print("load_dat::", "--- %s seconds ---" % (time.time() - start_time))
    # print("dat::", len(data))
    # print("dat::", len(data[0]))  # Print the first sublist to check
    # print("dat::", data[0])