# Report Regarding Tweezer Meeting 12/1/2022

### Language

*We choose Python as the programming language for reasons specified below.* 

1. Manual memory management/manipulation was unavoidable in the original C version, which can easily cause error and crushes. Python automatically manages the memory usage, which increases the program’s reliability. 
2. Python provides more built-in functionalities in solving problems like this, i.e. classes, while C doesn’t. Also increases reliability.
3. Python provides more built-in data structures and libraries for data manipulation and management, and these functionalities also come with great optimization, which can provide a higher data processing power, essentially increases performance and reliability.
4. The design concept of Python emphasizes the readability of the code, which is convenient for other laboratory team members to understand the source code and continue to build on it.
5. As a relatively young language, Python has a large number of external libraries which still being frequently updated. We think the current project needs a reliable GUI library as environment support.

*For this specific problem, there isn’t much cons in using Python rather than C.*

### Libraries

- Prototype - “xvingtk”

  - GTK (GUI) https://www.cairographics.org/
  - Cairo (2D Data visualization) https://www.cairographics.org/

- Python - New Software

  - NumPy (Dimensional array computing) https://github.com/numpy/numpy
  - Tkinter/Tkinter Canvas (GUI) https://docs.python.org/3/library/tkinter.html

  

  *GUI and data visualization libraries are still TBA. Other libraries that may be used include automatic updates, executable file packaging, file I/O, etc.*