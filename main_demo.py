import numpy

if __name__ == "__main__":
    a = numpy.array([1,2,3])
    b = numpy.array([1,2,3,4])
    c = a-b[:a.size]
    print(c)