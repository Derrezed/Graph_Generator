from PyQt5.QtWidgets import QApplication
import sys
from PlotCanvas import PlotCanvas

app = QApplication(sys.argv)
win = PlotCanvas()
win.show()
sys.exit(app.exec_())
