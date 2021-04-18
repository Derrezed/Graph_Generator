from PyQt5.QtWidgets import QFileDialog


class DataCollector:
    def open_dialog_box(self):
        self.file = QFileDialog.getOpenFileName()
        self.path = self.file[0]
