import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import test as TestFile
import Structural_Analysis.pyscripts.example as example

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

# You choose the function name. This will determine the name of the page in the array and on the tab layout.
def example_page():
    widget = QWidget()
    layout = QVBoxLayout()
    
    # Text
    myText = example.
    
    fig = Figure(figsize=(300, 300), dpi=100)
    axes = fig.add_subplot(111)
    axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40]) # Example data
    canvas = FigureCanvas(fig)
    
    layout.addWidget(QLabel("Graph 1:"))
    layout.addWidget(canvas)

    widget.setLayout(layout)
    return widget

def testpage():
    
    label = QLabel(TestFile.test_function())
    
    return label

def longitudal_2_paddler():
    widget = QWidget()
    
    layout = QHBoxLayout()
    layout.addWidget(QLabel("Centre of Mass:"))
    layout.addWidget(QLabel(str(example.center_of_mass())))
    
    widget.setLayout(layout)
    return widget
    


# --- Array of Page Functions ---
PAGE_CONFIG = [
    longitudal_2_paddler,
    testpage,
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UWaterloo Concrete Canoe Structural Analysis")
        self.resize(800, 600)
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(False)

        # Iterate over the function array and build the tabs
        for page_func in PAGE_CONFIG:
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