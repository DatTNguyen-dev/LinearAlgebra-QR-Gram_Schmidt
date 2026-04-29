import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QTextEdit, QLineEdit, QPushButton,
    QFrame, QSpinBox, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


# ── Stylesheet ──────────────────────────────────────────────
STYLESHEET = """
QMainWindow, QWidget {
    background-color: #F5F5F5;
    color: #212121;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}

QFrame#card {
    background-color: #FFFFFF;
    border: 1px solid #DDDDDD;
    border-radius: 8px;
}

QLabel#title {
    font-size: 13px;
    font-weight: bold;
    color: #212121;
}

QLabel#sublabel {
    font-size: 11px;
    color: #757575;
}

QLineEdit#matrix_cell {
    background-color: #FAFAFA;
    border: 1px solid #CCCCCC;
    border-radius: 4px;
    color: #212121;
    font-size: 14px;
    padding: 4px;
}
QLineEdit#matrix_cell:focus {
    border: 1px solid #1976D2;
    background-color: #FFFFFF;
}

QLineEdit#vec_cell {
    background-color: #FAFAFA;
    border: 1px solid #CCCCCC;
    border-radius: 4px;
    color: #E65100;
    font-size: 14px;
    padding: 4px;
}
QLineEdit#vec_cell:focus {
    border: 1px solid #E65100;
    background-color: #FFFFFF;
}

QSpinBox {
    background-color: #FAFAFA;
    border: 1px solid #CCCCCC;
    border-radius: 4px;
    color: #212121;
    padding: 3px 6px;
    min-width: 55px;
}
QSpinBox:focus { border: 1px solid #1976D2; }

QPushButton#btn_primary {
    background-color: #1976D2;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    font-size: 12px;
    font-weight: bold;
    padding: 8px 20px;
}
QPushButton#btn_primary:hover { background-color: #1565C0; }
QPushButton#btn_primary:pressed { background-color: #0D47A1; }

QPushButton#btn_secondary {
    background-color: #FFFFFF;
    color: #1976D2;
    border: 1px solid #1976D2;
    border-radius: 6px;
    font-size: 12px;
    padding: 8px 20px;
}
QPushButton#btn_secondary:hover { background-color: #E3F2FD; }

QPushButton#btn_clear {
    background-color: #FFFFFF;
    color: #757575;
    border: 1px solid #CCCCCC;
    border-radius: 6px;
    font-size: 11px;
    padding: 7px 14px;
}
QPushButton#btn_clear:hover {
    color: #D32F2F;
    border: 1px solid #D32F2F;
}

QTextEdit#output_box {
    background-color: #FAFAFA;
    border: 1px solid #DDDDDD;
    border-radius: 6px;
    color: #212121;
    font-size: 12px;
    font-family: 'Consolas', 'Courier New', monospace;
    padding: 10px;
}

QTabWidget::pane { border: none; background: transparent; }
QTabBar::tab {
    background: #EEEEEE;
    color: #757575;
    padding: 6px 16px;
    border-radius: 4px;
    margin-right: 3px;
    font-size: 11px;
}
QTabBar::tab:selected {
    background: #1976D2;
    color: #FFFFFF;
    font-weight: bold;
}
QTabBar::tab:hover:!selected {
    background: #E0E0E0;
    color: #212121;
}

QFrame#divider {
    background-color: #DDDDDD;
    max-height: 1px;
    min-height: 1px;
}

QScrollBar:vertical {
    background: #F5F5F5;
    width: 7px;
    border-radius: 3px;
}
QScrollBar::handle:vertical {
    background: #BDBDBD;
    border-radius: 3px;
    min-height: 20px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""


# ── Helpers ─────────────────────────────────────────────────
def divider():
    d = QFrame()
    d.setObjectName("divider")
    d.setFrameShape(QFrame.HLine)
    return d

def lbl(text, obj="sublabel", align=Qt.AlignLeft):
    l = QLabel(text)
    l.setObjectName(obj)
    l.setAlignment(align)
    return l

def make_output():
    te = QTextEdit()
    te.setObjectName("output_box")
    te.setReadOnly(True)
    te.setPlaceholderText("Results will be displayed here…")
    return te


# ── Panel 1: Input ───────────────────────────────────────────
class InputPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        self.n = 3
        self.matrix_cells = []
        self.b_cells = []

        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 16)
        lay.setSpacing(10)

        hdr = QHBoxLayout()
        hdr.addWidget(lbl("Input Matrix", "title"))
        hdr.addStretch()
        hdr.addWidget(lbl("Size:", "sublabel"))
        self.spin = QSpinBox()
        self.spin.setRange(2, 6)
        self.spin.setValue(3)
        self.spin.valueChanged.connect(self.rebuild)
        hdr.addWidget(self.spin)
        lay.addLayout(hdr)
        lay.addWidget(divider())

        col_lbl = QHBoxLayout()
        col_lbl.addWidget(lbl("Matrix A", "sublabel"))
        col_lbl.addStretch()
        col_lbl.addWidget(lbl("Vector b", "sublabel"))
        lay.addLayout(col_lbl)

        self.grid_widget = QWidget()
        self.grid = QGridLayout(self.grid_widget)
        self.grid.setSpacing(5)
        lay.addWidget(self.grid_widget)
        lay.addWidget(divider())

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        
        # Đã gỡ bỏ nút Load Example
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setObjectName("btn_clear")
        self.btn_clear.clicked.connect(self.clear_all)
        
        btn_row.addWidget(self.btn_clear)
        btn_row.addStretch()
        lay.addLayout(btn_row)

        self.rebuild(3)

    def rebuild(self, n):
        self.n = n
        while self.grid.count():
            w = self.grid.takeAt(0).widget()
            if w: w.deleteLater()
        self.matrix_cells = []
        self.b_cells = []
        for i in range(n):
            row = []
            for j in range(n):
                c = QLineEdit("0")
                c.setObjectName("matrix_cell")
                c.setFixedSize(52, 34)
                c.setAlignment(Qt.AlignCenter)
                self.grid.addWidget(c, i, j)
                row.append(c)
            self.matrix_cells.append(row)
            sep = QLabel("│")
            sep.setAlignment(Qt.AlignCenter)
            sep.setStyleSheet("color: #BDBDBD; font-size: 18px;")
            self.grid.addWidget(sep, i, n)
            b = QLineEdit("0")
            b.setObjectName("vec_cell")
            b.setFixedSize(52, 34)
            b.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(b, i, n + 1)
            self.b_cells.append(b)

    def clear_all(self):
        for row in self.matrix_cells:
            for c in row: c.setText("0")
        for c in self.b_cells: c.setText("0")

    def get_matrix(self):
        A = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                try: row.append(float(self.matrix_cells[i][j].text()))
                except: row.append(0.0)
            A.append(row)
        return A

    def get_b(self):
        b = []
        for c in self.b_cells:
            try: b.append(float(c.text()))
            except: b.append(0.0)
        return b


# ── Panel 2: Ax = b ──────────────────────────────────────────
class LinearSolvePanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 16)
        lay.setSpacing(10)

        lay.addWidget(lbl("Solve Linear System  Ax = b", "title"))
        lay.addWidget(divider())

        self.tabs = QTabWidget()
        for name in ["Matrix Q", "Matrix R", "Solution x"]:
            w = QWidget()
            v = QVBoxLayout(w)
            v.setContentsMargins(0, 6, 0, 0)
            v.addWidget(make_output())
            self.tabs.addTab(w, name)
        lay.addWidget(self.tabs)

        self.btn_solve = QPushButton("Solve  Ax = b")
        self.btn_solve.setObjectName("btn_primary")
        lay.addWidget(self.btn_solve)

    def _te(self, idx):
        return self.tabs.widget(idx).layout().itemAt(0).widget()

    def set_Q(self, html): self._te(0).setHtml(html)
    def set_R(self, html): self._te(1).setHtml(html)
    def set_solution(self, html):
        self._te(2).setHtml(html)
        self.tabs.setCurrentIndex(2)


# ── Panel 3: Eigenvalue ──────────────────────────────────────
class EigenPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 16)
        lay.setSpacing(10)

        hdr = QHBoxLayout()
        hdr.addWidget(lbl("Eigenvalue  —  QR Iteration", "title"))
        hdr.addStretch()
        hdr.addWidget(lbl("Iterations:", "sublabel"))
        self.iter_spin = QSpinBox()
        self.iter_spin.setRange(1, 200)
        self.iter_spin.setValue(20)
        hdr.addWidget(self.iter_spin)
        lay.addLayout(hdr)
        lay.addWidget(divider())

        self.tabs = QTabWidget()
        for name in ["Eigenvalues λ", "Iteration Log", "Convergence"]:
            w = QWidget()
            v = QVBoxLayout(w)
            v.setContentsMargins(0, 6, 0, 0)
            v.addWidget(make_output())
            self.tabs.addTab(w, name)
        lay.addWidget(self.tabs)

        self.btn_eigen = QPushButton("Find Eigenvalues")
        self.btn_eigen.setObjectName("btn_secondary")
        lay.addWidget(self.btn_eigen)

    def _te(self, idx):
        return self.tabs.widget(idx).layout().itemAt(0).widget()

    def set_eigenvalues(self, html): self._te(0).setHtml(html)
    def set_log(self, html):         self._te(1).setHtml(html)
    def set_convergence(self, html): self._te(2).setHtml(html)


def fmt_matrix(M, title=""):
    rows = "".join(
        "<tr>" + "".join(
            f'<td style="padding:3px 10px; text-align:right; font-family:Consolas;">'
            f'{v:8.4f}</td>' for v in row
        ) + "</tr>"
        for row in M
    )
    return f"<p style='color:#757575; font-size:11px; margin-bottom:4px;'>{title}</p><table>{rows}</table>"

def fmt_vector(vec, title=""):
    rows = "".join(
        f'<tr><td style="padding:3px 12px; font-family:Consolas;">'
        f'x<sub>{i+1}</sub> = {v:.4f}</td></tr>'
        for i, v in enumerate(vec)
    )
    return f"<p style='color:#757575; font-size:11px; margin-bottom:4px;'>{title}</p><table>{rows}</table>"

def run_solve(A, b, panel: LinearSolvePanel):
    #algorithm
    n = len(A)
    
    #algorithm của Đạt
    
   # tính toán 
    Q = [[0.0] * n for _ in range(n)]
    R = [[0.0] * n for _ in range(n)]
    x = [0.0] * n


    panel.set_Q(fmt_matrix(Q, "Matrix Q (orthogonal)"))
    panel.set_R(fmt_matrix(R, "Matrix R (upper triangular)"))
    panel.set_solution(fmt_vector(x, "Solution vector x"))

def run_eigen(A, iters, panel: EigenPanel):
    n = len(A)
    
    #giải eigenvalue

    eigs = [0.0] * n 

    rows = "".join(
        f'<tr><td style="padding:4px 12px; font-family:Consolas;">'
        f'λ<sub>{i+1}</sub> = {v:.6f}</td></tr>'
        for i, v in enumerate(eigs)
    )
    panel.set_eigenvalues(
        f"<p style='color:#757575; font-size:11px;'>After {iters} iterations</p>"
        f"<table>{rows}</table>"
    )
    
    
    panel.set_convergence(
        f"<p style='color:#388E3C; font-size:12px;'>✓ Completed {iters} iterations</p>"
    )


# ── Main Window ──────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Decomposition — Gram–Schmidt")
        self.setMinimumSize(1100, 680)
        self.resize(1280, 780)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 16, 20, 20)
        root.setSpacing(12)

        # Title
        title = QLabel("QR Decomposition  —  Gram–Schmidt")
        title.setStyleSheet("font-size: 17px; font-weight: bold; color: #212121;")
        sub = QLabel("QR Factorization  ·  Linear Solver  ·  Eigenvalue Approximation")
        sub.setStyleSheet("font-size: 11px; color: #757575;")
        root.addWidget(title)
        root.addWidget(sub)
        root.addWidget(divider())

        # Panels
        panels = QHBoxLayout()
        panels.setSpacing(12)
        self.input_panel  = InputPanel()
        self.linear_panel = LinearSolvePanel()
        self.eigen_panel  = EigenPanel()
        self.input_panel.setMaximumWidth(390)
        panels.addWidget(self.input_panel)
        panels.addWidget(self.linear_panel)
        panels.addWidget(self.eigen_panel)
        root.addLayout(panels)

        self.linear_panel.btn_solve.clicked.connect(self.on_solve)
        self.eigen_panel.btn_eigen.clicked.connect(self.on_eigen)

        self.statusBar().showMessage("Ready  ·  Enter matrix A and vector b")
        self.statusBar().setStyleSheet("color: #757575; font-size: 10px;")

    def on_solve(self):
        run_solve(self.input_panel.get_matrix(), self.input_panel.get_b(), self.linear_panel)
        self.statusBar().showMessage("✓  Linear system Ax = b execution completed")

    def on_eigen(self):
        iters = self.eigen_panel.iter_spin.value()
        run_eigen(self.input_panel.get_matrix(), iters, self.eigen_panel)
        self.statusBar().showMessage(f"✓  QR Iteration completed after {iters} iterations")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())