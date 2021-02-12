import PySide2
import requests
from PySide2.QtCore import QFile, QModelIndex
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableWidgetItem, QAbstractItemView


class Query:
    def __init__(self):
        UIFile = QFile("UI/query.ui")
        UIFile.open(UIFile.ReadOnly)
        UIFile.close()
        self.ui = QUiLoader().load(UIFile)

        for i in range(1, 13):
            self.ui.monBox.addItem(str(i))
        self.dayBoxSet31()
        self.ui.bt.clicked.connect(self.Bt)
        self.ui.bt2.clicked.connect(self.Bt2)
        self.ui.monBox.currentIndexChanged.connect(self.daySet)

        self.ui.tb.setColumnWidth(0, 100)
        self.ui.tb.setColumnWidth(1, 300)
        self.ui.tb.setColumnCount(2)
        self.ui.tb.setSelectionBehavior(QAbstractItemView.SelectRows)

    def daySet(self):
        mon = self.ui.monBox.currentText()
        if mon in ["1", "3", "5", "7", "8", "10", "12"]:
            self.dayBoxSet31()
        elif mon == "2":
            self.dayBoxSet28()
        else:
            self.dayBoxSet30()

    def dayBoxSet31(self):
        self.ui.dayBox.clear()
        for i in range(1, 32):
            self.ui.dayBox.addItem(str(i))

    def dayBoxSet30(self):
        self.ui.dayBox.clear()
        for i in range(1, 31):
            self.ui.dayBox.addItem(str(i))

    def dayBoxSet28(self):
        self.ui.dayBox.clear()
        for i in range(1, 29):
            self.ui.dayBox.addItem(str(i))

    def Bt(self):
        self.ui.tb.clearContents()
        m = self.ui.monBox.currentText()
        d = self.ui.dayBox.currentText()
        url = "https://api.jisuapi.com/todayhistory/query?appkey=79e0e0bd1ffe97d0&month=" + m + "&day=" + d
        r = requests.get(url)
        self.data = r.json()["result"]
        self.ui.tb.setRowCount(len(self.data))

        for i in range(len(self.data)):
            line1 = QTableWidgetItem(
                self.data[i]["year"] + "年" + self.data[i]["month"] + "月" + self.data[i]["day"] + "日")
            self.ui.tb.setItem(i, 0, line1)
            line2 = QTableWidgetItem(self.data[i]["title"])
            self.ui.tb.setItem(i, 1, line2)

    def Bt2(self):
        self.ui.showText.clear()
        # index = self.ui.bt.currentRow()
        index = self.ui.tb.selectionModel().currentIndex()
        index_row = index.row()
        self.ui.showText.appendPlainText(self.data[index_row]["content"])


def main():
    app = QApplication([])
    global Query
    q = Query()
    q.ui.show()
    app.exec_()


if __name__ == "__main__":
    main()
