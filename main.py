import sys
import matplotlib
import numpy as np

matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=12, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(qtw.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.data = {'Frequency': [300, 600, 900, 313, 1607],
            'Amplitude': [100, 40, 10, 10, 77],
            'Phase': [0, 0, 0, 0, 0]}

        self.colors = ["red", "blue", "gray", "green", "magenta", "black"]

        self.canvas_timedomain = MplCanvas(self, width=8, height=4, dpi=100)
        toolbar_timedomain = NavigationToolbar(self.canvas_timedomain, self)
        self.canvas_frequencydomain = MplCanvas(self, width=8, height=4, dpi=100)
        toolbar_frequencydomain = NavigationToolbar(self.canvas_frequencydomain, self)

        ### create polar diagramm
        self.figure_3 = Figure(figsize=(6,4))
        self.canvas_polar = FigureCanvas(self.figure_3)
        self.toolbar_polar = NavigationToolbar(self.canvas_polar, self)
        self.ax_polar = self.figure_3.add_subplot(1, 1, 1, projection='polar')

        self.btn_update = qtw.QPushButton("Update")
        self.btn_reset = qtw.QPushButton("Reset")
        self.le_input_1 = qtw.QLineEdit("10000")
        self.le_input_2 = qtw.QLineEdit("2")
        self.table = qtw.QTableWidget()
        self.text_output = qtw.QPlainTextEdit()

        layout = qtw.QHBoxLayout()

        vlayout_left = qtw.QVBoxLayout()
        vlayout_left.addWidget(self.btn_update)
        vlayout_left.addWidget(self.btn_reset)
        vlayout_left.addWidget(self.le_input_1)
        vlayout_left.addWidget(self.le_input_2)
        vlayout_left.addWidget(self.table)
        vlayout_left.addWidget(self.text_output)
        layout.addLayout(vlayout_left)

        vlayout_mid = qtw.QVBoxLayout()
        vlayout_mid.addWidget(self.canvas_timedomain)
        vlayout_mid.addWidget(toolbar_timedomain)
        vlayout_mid.addWidget(self.canvas_frequencydomain)
        vlayout_mid.addWidget(toolbar_frequencydomain)
        layout.addLayout(vlayout_mid)

        vlayout_right = qtw.QVBoxLayout()
        vlayout_right.addWidget(self.canvas_polar)
        vlayout_right.addWidget(self.toolbar_polar)
        layout.addLayout(vlayout_right)

        self.widget = qtw.QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)

        self.btn_update.clicked.connect(self.update_all)
        self.btn_reset.clicked.connect(self.reset)
        self.le_input_1.editingFinished.connect(self.update_all)
        self.update_table()

        self.setGeometry(100, 100, 1800, 800)
        self.show()

        self.table.keyPressEvent = self.tableKeyPressEvent

    def tableKeyPressEvent(self, event):
        # call the base implementation, do *not* use super()!
        qtw.QTableWidget.keyPressEvent(self.table, event)
        if event.key() in (qtc.Qt.Key_Return, qtc.Qt.Key_Enter):
            current = self.table.currentIndex()
            nextIndex = current.sibling(current.row() + 1, current.column())
            if nextIndex.isValid():
                self.table.setCurrentIndex(nextIndex)
                self.table.edit(nextIndex)


            self.update_all()



    def update_table(self):
        frequencies = self.data["Frequency"]
        amplitudes = self.data["Amplitude"]
        phases = self.data["Phase"]

        rows = len(frequencies)
        cols = 3
        self.table.setColumnCount(cols)
        self.table.setRowCount(rows)

        for row, _ in enumerate(frequencies):
            self.table.setItem(row, 0, qtw.QTableWidgetItem(f"{frequencies[row]}"))
            self.table.setItem(row, 1, qtw.QTableWidgetItem(f"{amplitudes[row]}"))
            self.table.setItem(row, 2, qtw.QTableWidgetItem(f"{phases[row]}"))

        self.table.setHorizontalHeaderLabels(self.data.keys())

    def reset(self):
        self.data = {
            'Frequency': [300, 600, 900, 313, 1607],
            'Amplitude': [100, 40, 10, 10, 77],
            'Phase': [0, 0, 0, 0, 0]}
        self.le_input_1.setText("10000")
        self.le_input_2.setText("2")
        self.update_table()
        self.update_plot()
        self.update_plot_spectrum()
        self.print_textoutput()

    def print_textoutput(self):
        txt = self.txt
        self.text_output.clear()
        self.text_output.insertPlainText(txt)

    def update_all(self):
        self.update_data()
        self.update_table()

        self.update_plot()
        self.update_plot_spectrum()
        self.update_plot_polar()

        self.print_textoutput()

    def update_plot(self):

        fs = float(self.le_input_1.text())
        self.dt = 1 / fs
        periods = float(self.le_input_2.text())
        frequencies = np.array(self.data["Frequency"])
        lowest_freq = np.min(frequencies[np.nonzero(frequencies)])
        T = 2 / lowest_freq
        highest_freq = max(frequencies)

        time = np.arange(0, T * periods, self.dt)

        self.txt = ""
        self.txt += f"T={T:.5e} s\n"
        self.txt += f"Periods={periods}\n"
        self.txt += f"dt={self.dt:.5e} s\n"
        self.txt += f"Ns={len(time)}\n"
        self.txt += f"fs={fs:.1f} Hz\n"
        self.txt += f"min(f)={lowest_freq} Hz\n"
        self.txt += f"max(f)={highest_freq} Hz\n"

        signal = time * 0

        self.canvas_timedomain.axes.cla()  # Clear the canvas.
        for idx, freq in enumerate(frequencies):
            amp = float(self.data["Amplitude"][idx])
            phase = np.deg2rad(self.data["Phase"][idx])

            sig = amp * np.sin(2 * np.pi * freq * time + phase)
            self.canvas_timedomain.axes.plot(time, sig, color=self.colors[idx], linewidth=2, label=f"F={freq}Hz")
            signal += sig

        self.time = time
        self.signal = signal
        self.canvas_timedomain.axes.plot(time, signal, 'r')
        self.canvas_timedomain.draw()

    def update_plot_spectrum(self):
        signal = self.signal

        X = np.fft.fft(signal) / len(signal) * 2
        X[0] /= 2
        freq = np.fft.fftfreq(signal.size, d=self.dt)

        self.X = X

        self.canvas_frequencydomain.axes.cla()  # Clear the canvas.
        self.canvas_frequencydomain.axes.plot(freq, np.abs(X), 'r')
        self.canvas_frequencydomain.axes.plot(self.data["Frequency"], self.data["Amplitude"], linestyle="None", marker='x')
        self.canvas_frequencydomain.axes.set_xlim(0, max(self.data["Frequency"]) * 1.5)
        self.canvas_frequencydomain.axes.set_ylim(0, max(self.data["Amplitude"]) * 1.1)
        self.canvas_frequencydomain.draw()

    def update_plot_polar(self):
        self.ax_polar.clear()

        ## input data
        radius = np.array(self.data["Amplitude"])
        angle = np.deg2rad(self.data["Phase"])
        for idx, _ in enumerate(radius):
            self.ax_polar.plot(angle[idx], radius[idx], color=self.colors[idx], linestyle="None", marker='x')

        ### From Timedomain
        radius = np.abs(self.X)
        angle = np.angle(self.X)
        self.ax_polar.plot(angle, radius, color='red', linestyle="None", marker='o')

        self.canvas_polar.draw()

    def update_data(self):
        frequencies = []
        amplitudes = []
        phases = []

        rows = self.table.rowCount()
        cols = self.table.columnCount()
        for row in range(rows):
            frequencies.append(float(self.table.item(row, 0).text()))
            amplitudes.append(float(self.table.item(row, 1).text()))
            phases.append(float(self.table.item(row, 2).text()))

        self.data = {
            "Frequency": frequencies,
            "Amplitude": amplitudes,
            "Phase": phases
        }


def main(args):
    app = qtw.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main(sys.argv)