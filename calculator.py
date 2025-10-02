import math
from PyQt4 import QtCore, QtGui
class Button(QtGui.QToolButton):
    def __init__(self, text, parent=None):
        super(Button, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Preferred)
        self.setText(text)
    def sizeHint(self):
        size = super(Button, self).sizeHint()
        size.setHeight(size.height() + 20)
        size.setWidth(max(size.width(), size.height()))
        return size
class Calculator(QtGui.QDialog):
    NumDigitButtons = 10
      def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        self.sumInMemory = 0.0
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.waitingForOperand = True
        self.display = QtGui.QLineEdit('0')
        self.display.setReadOnly(False)
        self.display.setAlignment(QtCore.Qt.AlignRight)
        self.display.setMaxLength(15)
        font = self.display.font()
        font.setPointSize(font.pointSize() + 8)
        self.display.setFont(font)
        self.digitButtons = []
                for i in range(Calculator.NumDigitButtons):
            self.digitButtons.append(self.createButton(str(i), self.digitClicked))
        self.pointButton = self.createButton(".", self.pointClicked)
        self.changeSignButton = self.createButton("\261", self.changeSignClicked)
        self.backspaceButton = self.createButton("Temizle", self.backspaceClicked)
        # Checkbox
        self.combo = QtGui.QComboBox(self)
        self.combo.addItem("radyan")
        self.combo.addItem("derece")
        self.combo.addItem("grad")
        self.deger = 'radyan'
        self.combo.activated[str].connect(self.onActivated)
        self.sinButton = self.createButton("Sin", self.unaryOperatorClicked)
        self.cosButton = self.createButton("Cos", self.unaryOperatorClicked)
        self.tanButton = self.createButton("Tan", self.unaryOperatorClicked)
        self.divisionButton = self.createButton("\367", self.multiplicativeOperatorClicked)
        self.timesButton = self.createButton("\327", self.multiplicativeOperatorClicked)
        self.minusButton = self.createButton("-", self.additiveOperatorClicked)
        self.plusButton = self.createButton("+", self.additiveOperatorClicked)
        self.squareRootButton = self.createButton(u"Kok", self.unaryOperatorClicked)
        self.powerButton = self.createButton("Karesi", self.unaryOperatorClicked)
        self.reciprocalButton = self.createButton("Tersi", self.unaryOperatorClicked)
        self.equalButton = self.createButton("=", self.equalClicked)
        mainLayout = QtGui.QGridLayout()
        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        mainLayout.addWidget(self.display, 0, 0, 1, 6)
        mainLayout.addWidget(self.backspaceButton, 1, 0, 1, 2)
        mainLayout.addWidget(self.combo, 2, 0) 
        mainLayout.addWidget(self.sinButton, 3, 0)
        mainLayout.addWidget(self.cosButton, 4, 0)
        mainLayout.addWidget(self.tanButton, 5, 0)
        for i in range(1, Calculator.NumDigitButtons):
            row = ((9 - i) / 3) + 2
            column = ((i - 1) % 3) + 1
            mainLayout.addWidget(self.digitButtons[i], row, column)
        mainLayout.addWidget(self.digitButtons[0], 5, 1)
        mainLayout.addWidget(self.pointButton, 5, 2)
        mainLayout.addWidget(self.changeSignButton, 5, 3)
        mainLayout.addWidget(self.divisionButton, 2, 4)
        mainLayout.addWidget(self.timesButton, 3, 4)
        mainLayout.addWidget(self.minusButton, 4, 4)
        mainLayout.addWidget(self.plusButton, 5, 4)
        mainLayout.addWidget(self.squareRootButton, 2, 5)
        mainLayout.addWidget(self.powerButton, 3, 5)
        mainLayout.addWidget(self.reciprocalButton, 4, 5)
        mainLayout.addWidget(self.equalButton, 5, 5)
        self.setLayout(mainLayout)
        self.setWindowTitle("Hesaplama Araci")
    def digitClicked(self):
        clickedButton = self.sender()
        digitValue = int(clickedButton.text())
        if self.display.text() == '0' and digitValue == 0.0:
            return
        if self.waitingForOperand:
            self.waitingForOperand = False
        self.display.setText(self.display.text() + str(digitValue))
    def unaryOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
        if clickedOperator == u"Kok":
            if operand < 0.0:
                self.abortOperation()
                return
            result = math.sqrt(operand)
        elif clickedOperator == "Karesi":
            result = math.pow(operand, 2.0)
        elif clickedOperator == "Tersi":
            if operand == 0.0:
                self.abortOperation()
                return
            result = 1.0 / operand
        elif clickedOperator == "Sin":
            if self.deger == 'radyan':
                result = math.sin(operand)
            elif self.deger == 'derece':
                result = math.sin(operand/180*math.pi)
            elif self.deger == 'grad':
                result = math.sin(operand/200*math.pi)
        elif clickedOperator == "Cos":
            if self.deger == 'radyan':
                result = math.cos(operand)
            elif self.deger == 'derece':
                result = math.cos(operand/180*math.pi) 
            elif self.deger == 'grad':
                result = math.cos(operand/200*math.pi)     
        elif clickedOperator == "Tan":
            if self.deger == 'radyan':
                result = math.tan(operand)
            elif self.deger == 'derece':
                result = math.tan(operand/180*math.pi)
            elif self.deger == 'grad':
                result = math.tan(operand/200*math.pi)
        self.display.setText(str(result))
        self.waitingForOperand = True
    def additiveOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.factorSoFar))
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''
        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.sumSoFar))
        else:
            self.sumSoFar = operand
        self.pendingAdditiveOperator = clickedOperator
        self.waitingForOperand = True
    def multiplicativeOperatorClicked(self):
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.factorSoFar))
        else:
            self.factorSoFar = operand
        self.pendingMultiplicativeOperator = clickedOperator
        self.waitingForOperand = True
    def equalClicked(self):
        operand = float(self.display.text())
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''
        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            self.pendingAdditiveOperator = ''
        else:
            self.sumSoFar = operand
        self.display.setText(str(self.sumSoFar))
        self.sumSoFar = 0.0
        self.waitingForOperand = True
    def pointClicked(self):
        if self.waitingForOperand:
            self.display.setText('0')
        if "." not in self.display.text():
            self.display.setText(self.display.text() + ".")
        self.waitingForOperand = False
    def changeSignClicked(self):
        text = self.display.text()
        value = float(text)
        if value > 0.0:
            text = "-" + text
        elif value < 0.0:
            text = text[1:]
        self.display.setText(text)
    def backspaceClicked(self):
        if self.waitingForOperand:
            return
        text = self.display.text()[:-1]
        if not text:
            text = '0'
            self.waitingForOperand = True
        self.display.setText(text)
        self.display.setText('0')
        self.waitingForOperand = True
    def createButton(self, text, member):
        button = Button(text)
        button.clicked.connect(member)
        return button
    def abortOperation(self):
        self.display.setText("Error")
    def calculate(self, rightOperand, pendingOperator):
        if pendingOperator == "+":
            self.sumSoFar += rightOperand
        elif pendingOperator == "-":
            self.sumSoFar -= rightOperand
        elif pendingOperator == "\327":
            self.factorSoFar *= rightOperand
        elif pendingOperator == "\367":
            if rightOperand == 0.0:
                return False
            self.factorSoFar /= rightOperand
        return True
    def onActivated(self, text):
        self.deger = text
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    calc = Calculator()
    sys.exit(calc.exec_())