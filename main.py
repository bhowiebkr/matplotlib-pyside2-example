import sys
import os
from PySide2 import QtWidgets, QtCore

from gui.plot_widget import PlotWidget
from data_loader import data_load


BRYAN_DEBUG = True


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.csv_file_path = None  # path to the csv file being opened

        self.data = None
        self.csv_file_path = None

        if BRYAN_DEBUG:
            self.csv_file_path = os.path.abspath("data.csv")

        self.setWindowTitle("PySide2 with Matplotlab Example")

        # Layouts
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(self.main_layout)

        # Widgets
        self.plot = PlotWidget()
        self.statusBar().showMessage("Ready")
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        # Open action
        open_action = file_menu.addAction("Open CSV File")
        open_action.setStatusTip("Select a CSV file to plot")
        open_action.triggered.connect(self.open_csv_file)

        # Save action
        save_image_action = file_menu.addAction("Save Image")
        save_image_action.setStatusTip("Save the plot to an image")
        save_image_action.triggered.connect(self.save_image)

        # Close action
        close_action = file_menu.addAction("Close")
        close_action.setStatusTip("Close the program")
        close_action.triggered.connect(self.close)

        # Add Widgets
        self.main_layout.addWidget(self.plot)

        # load the pos/scale of the gui
        settings = QtCore.QSettings("foo", "bar")
        try:
            self.restoreGeometry(settings.value("geometry"))
            s = settings.value("splitterSize")
            self.splitter.restoreState(s)
        except AttributeError:
            pass

        if BRYAN_DEBUG:
            self.load_csv()

    def open_csv_file(self):
        self.csv_file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, self.tr("Open CSV"), self.tr("~/Desktop/"), self.tr("CSV (*.csv)"),
        )
        self.load_csv()

    def save_image(self):
        print("saving image")

    def load_csv(self):
        print(f"Loading CSV {self.csv_file_path}")
        self.data = data_load(self.csv_file_path)
        self.plot.update_plot(self.data)

    def closeEvent(self, event):
        self.settings = QtCore.QSettings("foo", "bar")
        self.settings.setValue("geometry", self.saveGeometry())
        QtWidgets.QWidget.closeEvent(self, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
