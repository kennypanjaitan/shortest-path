# Shortest Path Finder
> Third mini-project for Algorithm Strategies (IF2211) course from Informatics Engineering, Bandung Institute of Technology.

<br>

## Contributors
| NIM | Name |
|:---:|:----:|
|13521006| [Azmi Hasna Zahrani](https://github.com/goodgirlwannabe)|
|13521023| [Kenny Benaya Nathan](https://github.com/kennypanjaitan)|

## Table of Contents
- [General Informations](#general-informations)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [How to Run](#how-to-run)
- [Project Status](#project-status)
- [Acknowledgements](#acknowledgements)

## General Informations
A program which finds the shortest path from two points in a graph. This program applies Uniform-Cost Search and A* algorithm. This program is written in Python and uses a simple GUI as its interface. The program can receive input from a .txt file containing a weighted adjacency matrix and a list of nodes or a specific map from the available locations. The program will show the distance, the path of the shortest path, and the visualization of the graph. The visualization of the shortest path from a specific locations can also be seen in Google Maps with the help of gmplot package. 

## Project Structure
```
├───doc                                 # Documentation
|    ├───Tucil3_13521006_13521023.pdf
|    ├───Tucil3-Stima-2023.pdf
|
├───src                                 # Source Code
|    ├───core                           # Core Program
|    |    ├───Area.py
|    |    ├───Components.py
|    |    ├───algorithm.py
|    |    ├───funtion.py
|    |    └───parsing.py
|    |
|    ├───gui                            # GUI Program
|    |    ├───images/
|    |    ├───gui.py
|    |    ├───gui.qrc
|    |    └───gui.ui
|    |
|    └───places                         # Places Data
|         ├───alunalun.py
|         ├───itbBdg.py
|         ├───itbNangor.py
|         ├───cilacap.py
|         └───buahBatu.py
│
├───main.py                             # Main Program
├───mymap.html                          # Map Output
├───matrix.txt                          # Matrix Data
└───README.md
```

## Technologies Used
- Python - 3.11.2
- PyQt5 - 5.15.9
- Figma
- Package sys
- Package webbrowser
- Package gmplot
- Package os
- Package matplotlib

## Features
- User can upload a .txt file containing a weighted adjacency matrix and a list of nodes. The example of the file can be seen in the file 'matrix.txt'
- User can choose a specific map to be used in the program. The available locations are ITB Bandung, Alun-Alun Bandung, ITB Jatinangor, Cilacap, and Buah Batu.
- User can see the available nodes in the map by clicking the 'Show' button below graph dropdown
- User can choose the start and final node
- User can choose the algorithm to be used to find the shortest path
- User can see the graph visualization of the shortest path
- User can see the distance and the path of the shortest path
- User can see the visualization of the shortest path in Google Maps by clicking the 'OpenGMaps' button



## How to Run
<div>
1. Clone this repository by running this command on your terminal:

```bash
git clone https://github.com/goodgirlwannabe/Tucil3_13521006_13521023.git
```
</div>

<div>
2. Install all the required packages
</div>

<div>
3. Run the program by running this command on your terminal:

```bash
py main.py
```
</div>

![](doc/images/img_gui.png)

<br>
4. In the program, user can upload a file containing a weighted adjacency matrix and a list of nodes by clicking the 'input file' button. Note that the file format that can be uploaded is a .txt file. The example of the file can be seen in the file 'matrix.txt'. Another example of the file format is as follows:

```txt
0 25 14             < Weighted Adjecency Matrix >
25 0 10             < Every column seperated with a space >
14 10 0             < Every row seperated with a newline >

A B C               < name each ccorresponding node seperated with a space >
< Seperate matrix and its node with an empty line >
< Ignore text within <> block >
```
![](doc/images/img_chooseFile.png)
![](doc/images/img_searchTxt.png)

<br>
5. Input the desired start and final node in the text box beside 'Start:' and 'Final:'. 

![](doc/images/img_inputNode.png)

<br>
6. Choose the desired algorithm to be used to find the shortest path by clicking either 'UCS' or 'A*' button. As soon as you click the button, the program will run the algorithm. The result will show the distance, the path of the shortest path, and the visualization of the graph.

![](doc/images/img_runFile.png)

<br>
7. User can also choose a specific map to be used in the program. Click the dropdown beside 'Graph:' and choose the desired map.

![](doc/images/img_chooseFile.png)

<br>
8. User can see the available nodes in the map by clicking the 'Show' button below graph dropdown

![](doc/images/img_showMap.png)

<br>
9. Repeat step 5 and 6 to find the shortest path in the chosen map.

![](doc/images/img_runAlgo.png)

<br>
10. A new file named 'mymap.html' will be created in the root directory. User can see the visualization of the shortest path in Google Maps by clicking the 'OpenGMaps' button.

![](doc/images/img_showGmap.png)

## Project Status
Project Status: Completed

## Acknowledgements
- This program was made to fulfill the third mini-project for Algorithm Strategies (IF2211) course from Informatics Engineering, Bandung Institute of Technology.
- Many thanks to prof. Ir. Rila Mandala, M.Eng., Ph.D. as the lecturer of IF2211 Algorithm Strategies course.
- Many thanks to all assistants of IF2211 Algorithm Strategies course.