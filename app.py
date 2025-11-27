import sys
import os
import pandas as pd

from PyQt6.QtWidgets import *
import pyqtgraph as pg

# IMPORT YOUR PAGE HERE!
import app_pages.example as example
from app_pages.approximation_vol_diff import build_all
import app_pages.flexuralStress as FlexuralStress

# YOU CAN IGNORE THESE! Just click on the arrow to the left of "#region" on the line below this to hide this section.
#region Helper Functions

def importHull(exportDate, exportYear):

    script_dir = os.path.abspath('data')

    # Read in the csv files
    dfInnerHull = pd.read_csv(os.path.join(script_dir, f"HullDesignExports/{exportYear}/{exportDate}/Hull Inner.csv"), header=None)
    dfOuterHull = pd.read_csv(os.path.join(script_dir, f"HullDesignExports/{exportYear}/{exportDate}/Hull Outer.csv"), header=None)
    dfInnerGunwale = pd.read_csv(os.path.join(script_dir, f"HullDesignExports/{exportYear}/{exportDate}/Gunwale Inner.csv"), header=None)
    dfOuterGunwale = pd.read_csv(os.path.join(script_dir, f"HullDesignExports/{exportYear}/{exportDate}/Gunwale Outer.csv"), header=None)

    # Remove brackets and make data values into decimal numbers
    dfInnerHull[dfInnerHull.columns[0]] = dfInnerHull[dfInnerHull.columns[0]].apply(lambda x: float(x[1:]))
    dfInnerHull[dfInnerHull.columns[1]] = dfInnerHull[dfInnerHull.columns[1]].apply(lambda x: float(x))
    dfInnerHull[dfInnerHull.columns[2]] = dfInnerHull[dfInnerHull.columns[2]].apply(lambda x: float(str(x)[:-1]))

    dfOuterHull[dfOuterHull.columns[0]] = dfOuterHull[dfOuterHull.columns[0]].apply(lambda x: float(str(x)[1:]))
    dfOuterHull[dfOuterHull.columns[1]] = dfOuterHull[dfOuterHull.columns[1]].apply(lambda x: float(x))
    dfOuterHull[dfOuterHull.columns[2]] = dfOuterHull[dfOuterHull.columns[2]].apply(lambda x: float(str(x)[:-1]))

    dfInnerGunwale[dfInnerGunwale.columns[0]] = dfInnerGunwale[dfInnerGunwale.columns[0]].apply(lambda x: float(x[1:]))
    dfInnerGunwale[dfInnerGunwale.columns[1]] = dfInnerGunwale[dfInnerGunwale.columns[1]].apply(lambda x: float(x))
    dfInnerGunwale[dfInnerGunwale.columns[2]] = dfInnerGunwale[dfInnerGunwale.columns[2]].apply(lambda x: float(str(x)[:-1]))

    dfOuterGunwale[dfOuterGunwale.columns[0]] = dfOuterGunwale[dfOuterGunwale.columns[0]].apply(lambda x: float(str(x)[1:]))
    dfOuterGunwale[dfOuterGunwale.columns[1]] = dfOuterGunwale[dfOuterGunwale.columns[1]].apply(lambda x: float(x))
    dfOuterGunwale[dfOuterGunwale.columns[2]] = dfOuterGunwale[dfOuterGunwale.columns[2]].apply(lambda x: float(str(x)[:-1]))

    # Sort the hull points into stations, then by the y-axis
    dfInnerHull = dfInnerHull.sort_values(by=[dfInnerHull.columns[0], dfInnerHull.columns[1]], ascending=True)
    dfOuterHull = dfOuterHull.sort_values(by=[dfOuterHull.columns[0], dfOuterHull.columns[1]], ascending=True)

    # Sort the gunwales into stations and then separate into positive and negative
    dfInnerGunwaleSorted = dfInnerGunwale.sort_values(by=[dfInnerGunwale.columns[0]], ascending=True)
    dfOuterGunwaleSorted = dfOuterGunwale.sort_values(by=[dfOuterGunwale.columns[0]], ascending=True)

    dfInnerGunwalePosSorted = dfInnerGunwaleSorted[dfInnerGunwaleSorted[dfInnerGunwaleSorted.columns[1]] > 0]
    dfInnerGunwaleNegSorted = dfInnerGunwaleSorted[dfInnerGunwaleSorted[dfInnerGunwaleSorted.columns[1]] < 0]
    dfOuterGunwalePosSorted = dfOuterGunwaleSorted[dfOuterGunwaleSorted[dfOuterGunwaleSorted.columns[1]] > 0]
    dfOuterGunwaleNegSorted = dfOuterGunwaleSorted[dfOuterGunwaleSorted[dfOuterGunwaleSorted.columns[1]] < 0]

    # Split stations
    dfInnerGunwaleStations = []
    dfOuterGunwaleStations = []

    for stationLoc in sorted(dfInnerGunwale[dfInnerGunwale.columns[0]].unique()):
        
        InnerPos = dfInnerGunwalePosSorted[dfInnerGunwalePosSorted[dfInnerGunwalePosSorted.columns[0]] == stationLoc]
        InnerNeg = dfInnerGunwaleNegSorted[dfInnerGunwaleNegSorted[dfInnerGunwaleNegSorted.columns[0]] == stationLoc]
        
        dfInnerGunwaleStations.append([
            InnerNeg.sort_values(by=[InnerPos.columns[1]], ascending=False).sort_values(by=[InnerNeg.columns[2]], ascending=False),
            InnerPos.sort_values(by=[InnerPos.columns[1]], ascending=False).sort_values(by=[InnerPos.columns[2]], ascending=True),
        ])
        
        OuterPos = dfOuterGunwalePosSorted[dfOuterGunwalePosSorted[dfOuterGunwalePosSorted.columns[0]] == stationLoc]
        OuterNeg = dfOuterGunwaleNegSorted[dfOuterGunwaleNegSorted[dfOuterGunwaleNegSorted.columns[0]] == stationLoc]
        
        dfOuterGunwaleStations.append([
            OuterNeg.sort_values(by=[InnerPos.columns[1]], ascending=False).sort_values(by=[OuterNeg.columns[2]], ascending=False),
            OuterPos.sort_values(by=[InnerPos.columns[1]], ascending=False).sort_values(by=[OuterPos.columns[2]], ascending=True),
        ])
        
    # Arrange each station
    dfInnerTotal = pd.DataFrame()
    dfOuterTotal = pd.DataFrame()

    for station in zip(range(dfInnerHull[dfInnerHull.columns[0]].nunique()), sorted(dfInnerHull[dfInnerHull.columns[0]].unique())):
        dfInnerTotal = pd.concat([dfInnerTotal, dfInnerGunwaleStations[station[0]][0]], ignore_index=True)
        dfInnerTotal = pd.concat([dfInnerTotal, dfInnerHull[dfInnerHull[dfInnerHull.columns[0]] == station[1]]], ignore_index=True)
        dfInnerTotal = pd.concat([dfInnerTotal, dfInnerGunwaleStations[station[0]][1]], ignore_index=True)
        
        dfOuterTotal = pd.concat([dfOuterTotal, dfOuterGunwaleStations[station[0]][0]], ignore_index=True)
        dfOuterTotal = pd.concat([dfOuterTotal, dfOuterHull[dfOuterHull[dfOuterHull.columns[0]] == station[1]]], ignore_index=True)
        dfOuterTotal = pd.concat([dfOuterTotal, dfOuterGunwaleStations[station[0]][1]], ignore_index=True)

    # Set the Inner anf Outer Hull files
    dfInnerTotal.to_csv('data/Inner Hull.csv', index=False, header=None)
    dfOuterTotal.to_csv('data/Outer Hull.csv', index=False, header=None)

    print("CSV files sorted and imported.")

PEN_COLORS = [
    '#1f77b4',  # tab:blue
    '#ff7f0e',  # tab:orange
    '#2ca02c',  # tab:green
    '#d62728',  # tab:red
    '#9467bd',  # tab:purple
    '#8c564b',  # tab:brown
    '#e377c2',  # tab:pink
    '#7f7f7f',  # tab:gray
    '#bcbd22',  # tab:olive
    '#17becf'   # tab:cyan
]

def makeGraphInputs(inputNames):
    inputWidget = QWidget()
    inputLayout = QVBoxLayout()
    
    inputs = []
    
    for i in range(len(inputNames)):
        inputLabelWidget = QWidget()
        inputLabelLayout = QHBoxLayout()
        inputs.append(QLineEdit(""))
        inputLabelLayout.addWidget(QLabel(inputNames[i] + ":"))
        inputLabelLayout.addWidget(inputs[i])
        inputLabelWidget.setLayout(inputLabelLayout)
        inputLayout.addWidget(inputLabelWidget)
        
    inputWidget.setLayout(inputLayout)
    
    return inputWidget, inputs

def plot(plotData, connect_inputs=[]):
    
    inputs = []
    
    for i in range(len(connect_inputs)):
        try:
            inputs.append(float(inputs[i].text()))
        except Exception:
            inputs.append(0)
    
    x, y, title, xlabel, ylabel = plotData(*inputs)
    
    widget = pg.PlotWidget()
    widget.setBackground("w")
    widget.showGrid(x=True, y=True)
    widget.getAxis('left').setTextPen('black')
    widget.getAxis('bottom').setTextPen('black')
    
    widget.setTitle(title, size='18pt', color='black')
    widget.setLabel("bottom", xlabel, color='black')
    widget.setLabel("left", ylabel, color='black')
    
    updateRefs = []
    
    if isinstance(x[0], list):
        for i in range(len(x)):
            pen = pg.mkPen(color=PEN_COLORS[i], width=3)
            updateRefs.append(widget.plot(x[i], y[i], pen=pen))
    else:
        pen = pg.mkPen(color=PEN_COLORS[0], width=3)
        updateRefs.append(widget.plot(x, y, pen=pen))
        
    if connect_inputs != []:
        gu = GraphUpdate(inputs)
        for i in range(len(connect_inputs)):
            connect_inputs[i].textChanged.connect(lambda x, index=i: gu.updateGraph(updateRefs, plotData, index)(x))
    
    return widget

class GraphUpdate:
    def __init__(self, inputs):
        self.inputs = inputs
        
    def updateGraph(self, updateRefs, plotData, inputNum):
        
        def func(newInput):
            
            try:
                a = float(newInput)
                self.inputs[inputNum] = a
            except Exception:
                pass
            
            x, y, title, xlabel, ylabel = plotData(*self.inputs)
            
            if isinstance(x[0], list):
                for i in range(len(x)):
                    updateRefs[i].setData(x[i], y[i])
            else:
                updateRefs[0].setData(x, y)
                
        return func

#endregion

# You choose the function name. This will determine the name of the page in the array and on the tab layout.
def example_page():
    widget = QWidget()
    grid = QGridLayout()
    widget.setLayout(grid)
    
    # You can use other layouts than grid, see https://www.pythonguis.com/tutorials/pyqt-layouts/
    # However, for working with graphs, the grid layout is quite useful for keeping things the same size :)
    # For the grid layout, you choose the coordinates of each item, with 0,0 being the top left
    
    # Text
    text_result = QLabel(example.TextResult())
    grid.addWidget(text_result, 0, 0)
    
    # Graph without inputs
    # The first argument is the function your graph uses, and the second is the inputs to the graph (in this case an empty array)
    graph1 = plot(example.Graph1)
    grid.addWidget(graph1, 0, 1)

    # Inputs
    inputs2, connect_inputs2 = makeGraphInputs(["Paddler 1", "Paddler 2", "Paddler 3"])
    grid.addWidget(inputs2, 1, 0)

    # Graph using inputs
    graph2 = plot(example.Graph2, connect_inputs2)
    grid.addWidget(graph2, 1, 1)

    return widget


def flexural_stress_page():

    widget = QWidget()
    grid = QGridLayout()
    widget.setLayout(grid)
    
    INPUT_FILES = ["Shear_and_Moment_6 Paddlers.csv", "Shear_and_Moment_4 Paddlers.csv", "Shear_and_Moment_3 Paddlers.csv", "Shear_and_Moment_2 Paddlers.csv", "Shear_and_Moment_Display_Stand.csv"]
    MOMENT_FILES = ["Length_vs_Moment_6 Paddler.csv", "Length_vs_Moment_4 Paddler.csv", "Length_vs_Moment_3 Paddler.csv", "Length_vs_Moment_2 Paddler.csv", "Length_vs_Moment_Display_Stand.csv", ]
    CASE_NAMES = ["Swamp", "4 Paddler", "3 Paddler", "2 Paddler", "Display Stand"]

    # You can use other layouts than grid, see https://www.pythonguis.com/tutorials/pyqt-layouts/
    # However, for working with graphs, the grid layout is quite useful for keeping things the same size :)
    # For the grid layout, you choose the coordinates of each item, with 0,0 being the top left
    
    PAD_CASE_LENGTH, PAD_CASE_MOMENT, stressTopByCase, stressBottomByCase, stations_mm, stressTopArray, stressBottomArray, resistanceTensTopArray, resistanceTensBottomArray = FlexuralStress.initialLoop(MOMENT_FILES)

    station_mm_per_case = [stations_mm] * len(INPUT_FILES)

    # Max Negative Moments Text
    momentResultsByCase = []

    momentResults = FlexuralStress.Max_Negative_Moments(INPUT_FILES)

    momentResultString = ""
    for file in momentResults:
        fileResults = momentResults[file]
        fileResultString = ""
        fileMomentResults = [
            f"\tTensile Flexural Stress: {fileResults['tensile_flexural_stress']} MPa",
            f"\tCompressive Flexural Stress: {fileResults['compressive_flexural_stress']} MPa",
            f"\tApplied Negative Moment: {fileResults['applied_negative_moment']} Nm",
            f"\tStress Top: {fileResults['stress_top']} MPa",
            f"\tStress Bottom: {fileResults['stress_bottom']} MPa",
            f"\tResistance Top: {fileResults['resistance_top']} Nm",
            f"\tResistance Bottom: {fileResults['resistance_bottom']} Nm",
            "",
            "",
            f"\tExtrema of Envelope: {max(resistanceTensTopArray)}\t{min(resistanceTensBottomArray)}"
        ]
        caseName = CASE_NAMES[INPUT_FILES.index(file)] 
        fileResultString += caseName + ":\n"
        fileResultString += "\n".join(fileMomentResults) + "\n"
        momentResultsByCase.append(fileResultString)

        momentResultString+=fileResultString
    
    momentResultString += f"Max Envelope Value: {max(resistanceTensTopArray)} @ {resistanceTensTopArray.index(max(resistanceTensTopArray))} / {len(resistanceTensTopArray)}"



    results = [
        f"Max Compressive Stress Top: {max(stressTopArray)} MPa",
        f"Max Tensile Stress Top: {min(stressTopArray)} MPa",
        f"Max Compressive Stress Bottom: {max(stressBottomArray)} MPa",
        f"Max Tensile Stress Bottom: {min(stressBottomArray)} MPa"
    ]
    resultString = "\n".join(results)

    grid.addWidget(QLabel(resultString),0,0)



    # Top Stress Graphs
    Top_Stress_Stack_Layout = QStackedLayout()
    Top_Stress_Graphs = []

    for i in range(len(stressTopByCase)):
        stressTop = stressTopByCase[i]
        Top_Stress_Graph = plot(lambda: (stations_mm, stressTop, "Top Stress", "x (mm)", "Stress (MPa)"))
        Top_Stress_Stack_Layout.addWidget(Top_Stress_Graph)
        Top_Stress_Graphs.append(Top_Stress_Graph)
    grid.addLayout(Top_Stress_Stack_Layout,0,1)


    # Bottom Stress Graphs
    Bottom_Stress_Stack_Layout = QStackedLayout()
    Bottom_Stress_Graphs = []

    for i in range(len(stressBottomByCase)):
        stressBottom = stressBottomByCase[i]
        Bottom_Stress_Graph = plot(lambda: (stations_mm, stressBottom, "Bottom Stress", "x (mm)", "Stress (MPa)"))
        Bottom_Stress_Stack_Layout.addWidget(Bottom_Stress_Graph)
        Bottom_Stress_Graphs.append(Bottom_Stress_Graph)
    grid.addLayout(Bottom_Stress_Stack_Layout,1,1)

    # All Top Stress Garphs 
    Top_Stress_All_Cases_Graph = plot(lambda: (station_mm_per_case, stressTopByCase, "Top Stress All Cases", "x (mm)", "Stress (MPa)"))
    grid.addWidget(Top_Stress_All_Cases_Graph,2,1)



    # All Bottom Stress Garphs
    Bottom_Stress_All_Cases_Graph = plot(lambda: (station_mm_per_case, stressBottomByCase, "Bottom Stress All Cases", "x (mm)", "Stress (MPa)"))
    grid.addWidget(Bottom_Stress_All_Cases_Graph,2,0)

    # Tensile Resistance Envelope Graph
    Tensile_Resistance_Envelope_Graph = plot(lambda: ([stations_mm] * 2, [resistanceTensTopArray, resistanceTensBottomArray], "Tensile Resistance Envelope", "x (mm)", "Stress (MPa)"))
    grid.addWidget(Tensile_Resistance_Envelope_Graph,3,0)

    # Bending Moment Resistance Envelope Graph
    pad_case_length_values = [stations_mm] * 2
    pad_case_moment_values = [resistanceTensTopArray, resistanceTensBottomArray]
    for i in range(len(CASE_NAMES)):
        #
        # code was giving errors when I just copy pasted the ipynb code when calling plot()
        # there is probably a better way to turn the panda csv into a regular list but I have never used numpy or panda
        #
        pad_case_length_values.append(PAD_CASE_LENGTH[i].astype(float).to_numpy().tolist())
        pad_case_moment_values.append(PAD_CASE_MOMENT[i].astype(float).to_numpy().tolist())

    Bending_Moment_Resistance_Envelope_Graph = plot(lambda: (pad_case_length_values, pad_case_moment_values, "Bending Moment Resistance Envelope", "x (mm)", "Max Moment (Nm)"))
    grid.addWidget(Bending_Moment_Resistance_Envelope_Graph,3,1)

    momentResultLabel = QLabel(momentResultsByCase[0])





    resultBoxLayout = QVBoxLayout()
    combobox = QComboBox()
    combobox.addItems(momentResults.keys())
    combobox.currentIndexChanged.connect(lambda i: momentResultLabel.setText(momentResultsByCase[i]))
    combobox.currentIndexChanged.connect(Top_Stress_Stack_Layout.setCurrentIndex)
    combobox.currentIndexChanged.connect(Bottom_Stress_Stack_Layout.setCurrentIndex)




    resultBoxLayout.addWidget(combobox)
    resultBoxLayout.addWidget(momentResultLabel)

    grid.addLayout(resultBoxLayout,1,0)

    return widget


# wrap imported approximation page function into local function object for PAGE_ORDER
def approximation_vol_diff_page():
    widget = QWidget()
    grid = QGridLayout()
    widget.setLayout(grid)

    try:
        results = build_all()
    except Exception as e:
        grid.addWidget(QLabel(f"Failed to run analysis: {e}"), 0, 0)
        return widget

    # prepare data
    try:
        stations = list(results['outer']['station'])
    except Exception:
        stations = list(results['outer']['station'].to_numpy()) if hasattr(results['outer']['station'], 'to_numpy') else list(results['outer']['station'])

    station_centers = [(stations[i] + stations[i + 1]) / 2 for i in range(len(stations) - 1)]
    shear = results.get('shear', [])
    moment = results.get('moment', [])
    stat_mass = results.get('stat_mass', [])
    stat_vol = results.get('stat_vol', [])
  
    # summary
    summary = [
        f"Total Mass: {results.get('canoe_mass', 0):.2f} kg",
        f"Number of Stations: {len(station_centers)}",
        f"Canoe Length: {max(stations) if stations else 0} mm",
        f"Max Moment: {max(map(abs, moment)) if moment else 0:.2f} N⋅m",
    ]
    grid.addWidget(QLabel("\n".join(summary)), 0, 0)

    # Shear and Moment graphs
    shear_graph = plot(lambda: (results['x'], shear, "Shear Force", "x (mm)", "Shear (N)"))
    grid.addWidget(shear_graph, 0, 1)

    moment_graph = plot(lambda: (results['x'], moment, "Bending Moment", "x (mm)", "Moment (N⋅m)"))
    grid.addWidget(moment_graph, 1, 1)

    mass_graph = plot(lambda: (station_centers, stat_mass, "Mass by Station", "x (mm)", "Mass (kg)"))
    grid.addWidget(mass_graph, 1, 0)

    vol_graph = plot(lambda: (station_centers, stat_vol, "Volume by Station", "x (mm)", "Volume (mm³)"))
    grid.addWidget(vol_graph, 2, 0)

    return widget

# --- Array of Page Functions ---
PAGE_ORDER = [
    example_page,
    approximation_vol_diff_page,
    flexural_stress_page,
]
 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Enter date of the files (Inner Gunwale.csv)
        importHull("Oct4", "2025")

        self.setWindowTitle("UWaterloo Concrete Canoe Structural Analysis")
        self.resize(1200, 800)
        tabs = QTabWidget()
        # tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(False)

        # Iterate over the function array and build the tabs
        for page_func in PAGE_ORDER:
            try:
                # 1. Execute the function to get the QWidget object
                content_widget = page_func()
                
                # 2. Use the function's name as the tab title
                # Format: create_name_tab -> Name
                tab_title = page_func.__name__.replace('_', ' ').title()
                
                # 3. Add the dynamically generated widget as a new tab
                tabs.addTab(content_widget, tab_title)
                
            except Exception as e:
                # Fallback in case a function fails to build its widget
                error_widget = QLabel(f"Failed to load tab content: {e}")
                error_widget.setStyleSheet("color: white; background-color: red; padding: 20px;")
                tabs.addTab(error_widget, page_func.__name__.title() + " (ERROR)")


        self.setCentralWidget(tabs)


# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
