import sys
from PyQt6.QtWidgets import *
import pyqtgraph as pg

# IMPORT YOUR PAGE HERE!
import app_pages.example as example

# YOU CAN IGNORE THESE! Just click on the arrow to the left of "#region" on the line below this to hide this section.
#region Helper Functions
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
        except Exception as e:
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
            except Exception as e:
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

def page_2():
    # Someone replace this with your page so people see the pattern lol
    return QWidget()

# --- Array of Page Functions ---
PAGE_ORDER = [
    example_page,
    page_2,
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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
