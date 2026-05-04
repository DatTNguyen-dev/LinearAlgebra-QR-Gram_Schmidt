import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QTextEdit, QLineEdit, QPushButton,
    QFrame, QSpinBox, QTabWidget, QSplitter, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# ── Styles ────────────────────────────────────────────────────
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

QLabel#panel_title {
    font-size: 12px;
    font-weight: bold;
    color: #424242;
    padding: 2px 0px;
}

QLineEdit#matrix_cell {
    background-color: #FAFAFA;
    border: 1px solid #CCCCCC;
    border-radius: 4px;
    color: #212121;
    font-size: 13px;
    padding: 3px;
}
QLineEdit#matrix_cell:focus {
    border: 1px solid #1976D2;
    background-color: #FFFFFF;
}

QLineEdit#vec_cell {
    background-color: #FFF8F5;
    border: 1px solid #FFCCAA;
    border-radius: 4px;
    color: #E65100;
    font-size: 13px;
    padding: 3px;
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
    min-width: 50px;
}
QSpinBox:focus { border: 1px solid #1976D2; }

QPushButton#btn_primary {
    background-color: #1976D2;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    font-size: 12px;
    font-weight: bold;
    padding: 7px 18px;
}
QPushButton#btn_primary:hover { background-color: #1565C0; }
QPushButton#btn_primary:pressed { background-color: #0D47A1; }

QPushButton#btn_secondary {
    background-color: #FFFFFF;
    color: #1976D2;
    border: 1px solid #1976D2;
    border-radius: 6px;
    font-size: 12px;
    padding: 7px 18px;
}
QPushButton#btn_secondary:hover { background-color: #E3F2FD; }

QPushButton#btn_clear {
    background-color: #FFFFFF;
    color: #757575;
    border: 1px solid #CCCCCC;
    border-radius: 6px;
    font-size: 11px;
    padding: 6px 12px;
}
QPushButton#btn_clear:hover {
    color: #D32F2F;
    border: 1px solid #D32F2F;
}

QTextEdit#output_box {
    background-color: #FAFAFA;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    color: #212121;
    font-size: 12px;
    font-family: 'Consolas', 'Courier New', monospace;
    padding: 8px;
}

QFrame#divider {
    background-color: #DDDDDD;
    max-height: 1px;
    min-height: 1px;
}

QFrame#vdivider {
    background-color: #DDDDDD;
    max-width: 1px;
    min-width: 1px;
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

QSplitter::handle {
    background-color: #DDDDDD;
}
QSplitter::handle:horizontal { width: 5px; }
QSplitter::handle:vertical   { height: 5px; }
"""


def divider(vertical=False):
    d = QFrame()
    if vertical:
        d.setObjectName("vdivider")
        d.setFrameShape(QFrame.VLine)
    else:
        d.setObjectName("divider")
        d.setFrameShape(QFrame.HLine)
    return d

def lbl(text, obj="sublabel", align=Qt.AlignLeft):
    l = QLabel(text)
    l.setObjectName(obj)
    l.setAlignment(align)
    return l

def make_output(placeholder="Results will appear here…"):
    te = QTextEdit()
    te.setObjectName("output_box")
    te.setReadOnly(True)
    te.setPlaceholderText(placeholder)
    return te


# ──Input ────────────────────────────────────
class InputPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        self.m = 3  
        self.n = 3  
        self.matrix_cells = []
        self.b_cells = []

        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 12, 14, 14)
        outer.setSpacing(8)

        # Header
        hdr = QHBoxLayout()
        hdr.addWidget(lbl("Input Matrix", "title"))
        hdr.addStretch()

        hdr.addWidget(lbl("m:", "sublabel"))
        self.spin_m = QSpinBox()
        self.spin_m.setRange(2, 7)
        self.spin_m.setValue(3)
        self.spin_m.setToolTip("Number of rows m")
        hdr.addWidget(self.spin_m)

        hdr.addWidget(lbl("n:", "sublabel"))
        self.spin_n = QSpinBox()
        self.spin_n.setRange(2, 7)
        self.spin_n.setValue(3)
        self.spin_n.setToolTip("Number of columns n  (n ≤ m)")
        hdr.addWidget(self.spin_n)

        self.spin_m.valueChanged.connect(self._on_spin)
        self.spin_n.valueChanged.connect(self._on_spin)

        outer.addLayout(hdr)
        outer.addWidget(divider())

        # Column labels
        col_info = QHBoxLayout()
        col_info.addWidget(lbl("Matrix A  (m × n)", "sublabel"))
        col_info.addStretch()
        col_info.addWidget(lbl("Vector b  (m × 1)", "sublabel"))
        outer.addLayout(col_info)

        # Input grid
        self.grid_widget = QWidget()
        self.grid = QGridLayout(self.grid_widget)
        self.grid.setSpacing(4)
        outer.addWidget(self.grid_widget)
        outer.addStretch()
        outer.addWidget(divider())

        # Buttons
        btn_row = QHBoxLayout()
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setObjectName("btn_clear")
        self.btn_clear.clicked.connect(self.clear_all)
        btn_row.addWidget(self.btn_clear)
        btn_row.addStretch()
        outer.addLayout(btn_row)

        self.rebuild(3, 3)

    def _on_spin(self):
        m = self.spin_m.value()
        n = self.spin_n.value()
        # Ensure n ≤ m
        if n > m:
            self.spin_n.blockSignals(True)
            self.spin_n.setValue(m)
            self.spin_n.blockSignals(False)
            n = m
        self.rebuild(m, n)

    def rebuild(self, m, n):
        self.m = m
        self.n = n
        while self.grid.count():
            w = self.grid.takeAt(0).widget()
            if w:
                w.deleteLater()
        self.matrix_cells = []
        self.b_cells = []

        cell_w = max(38, min(52, 260 // n))
        cell_h = 30

        for i in range(m):
            row = []
            for j in range(n):
                c = QLineEdit("0")
                c.setObjectName("matrix_cell")
                c.setFixedSize(cell_w, cell_h)
                c.setAlignment(Qt.AlignCenter)
                self.grid.addWidget(c, i, j)
                row.append(c)
            self.matrix_cells.append(row)

            sep = QLabel("│")
            sep.setAlignment(Qt.AlignCenter)
            sep.setStyleSheet("color: #BDBDBD; font-size: 16px;")
            self.grid.addWidget(sep, i, n)

            # Vector b
            b = QLineEdit("0")
            b.setObjectName("vec_cell")
            b.setFixedSize(46, cell_h)
            b.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(b, i, n + 1)
            self.b_cells.append(b)

    def clear_all(self):
        for row in self.matrix_cells:
            for c in row:
                c.setText("0")
        for c in self.b_cells:
            c.setText("0")

    def get_matrix(self):
        A = []
        for i in range(self.m):
            row = []
            for j in range(self.n):
                try:
                    row.append(float(self.matrix_cells[i][j].text()))
                except:
                    row.append(0.0)
            A.append(row)
        return A

    def get_b(self):
        b = []
        for c in self.b_cells:
            try:
                b.append(float(c.text()))
            except:
                b.append(0.0)
        return b


# ── QR Decomposition ───────────────────
class QRPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 12, 14, 14)
        lay.setSpacing(0)

        # Title
        lay.addWidget(lbl("Matrix Q  and  R", "title"))
        lay.addSpacing(6)
        lay.addWidget(divider())
        lay.addSpacing(6)

        splitter = QSplitter(Qt.Vertical)
        splitter.setHandleWidth(6)

        # Q pane
        w_q = QWidget()
        v_q = QVBoxLayout(w_q)
        v_q.setContentsMargins(0, 0, 0, 0)
        v_q.setSpacing(4)
        v_q.addWidget(lbl("Matrix Q  (orthogonal)", "sublabel"))
        self.te_q = make_output("Q will appear here…")
        v_q.addWidget(self.te_q)
        splitter.addWidget(w_q)

        # R pane
        w_r = QWidget()
        v_r = QVBoxLayout(w_r)
        v_r.setContentsMargins(0, 0, 0, 0)
        v_r.setSpacing(4)
        v_r.addWidget(lbl("Matrix R  (upper triangular)", "sublabel"))
        self.te_r = make_output("R will appear here…")
        v_r.addWidget(self.te_r)
        splitter.addWidget(w_r)

        splitter.setSizes([200, 200])
        lay.addWidget(splitter, 1)
        lay.addSpacing(8)
        lay.addWidget(divider())
        lay.addSpacing(6)

        self.btn_decompose = QPushButton("Compute QR Decomposition")
        self.btn_decompose.setObjectName("btn_primary")
        lay.addWidget(self.btn_decompose)

    def set_Q(self, html): self.te_q.setHtml(html)
    def set_R(self, html): self.te_r.setHtml(html)


# ──Solve Ax=b ───────────────────────────
class SolutionPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 12, 14, 14)
        lay.setSpacing(8)

        hdr = QHBoxLayout()
        hdr.addWidget(lbl("Solve  Ax = b", "title"))
        hdr.addStretch()
        lay.addLayout(hdr)
        lay.addWidget(divider())

        self.te = make_output("Solution x will appear here…")
        lay.addWidget(self.te, 1)
        lay.addWidget(divider())

        self.btn_solve = QPushButton("Solve  Ax = b")
        self.btn_solve.setObjectName("btn_primary")
        lay.addWidget(self.btn_solve)

    def set_solution(self, html): self.te.setHtml(html)


# ── Eigenvalue ───────────────────────────
class EigenPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("card")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 12, 14, 14)
        lay.setSpacing(8)

        hdr = QHBoxLayout()
        hdr.addWidget(lbl("Eigenvalues  —  QR Iteration", "title"))
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
        lay.addWidget(self.tabs, 1)
        lay.addWidget(divider())

        self.btn_eigen = QPushButton("Find Eigenvalues")
        self.btn_eigen.setObjectName("btn_secondary")
        lay.addWidget(self.btn_eigen)

    def _te(self, idx):
        return self.tabs.widget(idx).layout().itemAt(0).widget()

    def set_eigenvalues(self, html): self._te(0).setHtml(html)
    def set_log(self, html):         self._te(1).setHtml(html)
    def set_convergence(self, html): self._te(2).setHtml(html)



# ── Formatters ────────────────────────────────────────────────

def fmt_matrix(M, title=""):
    lines = [title] if title else []
    for row in M:
        lines.append("  ".join(f"{v:8.4f}" for v in row))
    return "<pre>" + "\n".join(lines) + "</pre>"

def fmt_vector(vec, title=""):
    lines = [title] if title else []
    for i, v in enumerate(vec):
        lines.append(f"  x{i+1} = {v:.4f}")
    return "<pre>" + "\n".join(lines) + "</pre>"


# ── Algorithms ────────────────────────────────────────────────

def run_decompose(A, qr_panel):
    m = len(A)
    n = len(A[0])

    #decomposition algorithm here

    Q = [[0.0] * n for _ in range(m)]   
    R = [[0.0] * n for _ in range(n)]   
    qr_panel.set_Q(fmt_matrix(Q, f"Matrix Q  ({m} × {n})  — not yet implemented"))
    qr_panel.set_R(fmt_matrix(R, f"Matrix R  ({n} × {n})  — not yet implemented"))


def run_solve(A, b, qr_panel, sol_panel):
    m = len(A)
    n = len(A[0])

    #algorithm solve Ax = b

    Q = [[0.0] * n for _ in range(m)]  
    R = [[0.0] * n for _ in range(n)]  
    x = [0.0] * n                      
    qr_panel.set_Q(fmt_matrix(Q, f"Matrix Q  ({m} × {n})  — not yet implemented"))
    qr_panel.set_R(fmt_matrix(R, f"Matrix R  ({n} × {n})  — not yet implemented"))
    sol_panel.set_solution(fmt_vector(x, "Solution x  — not yet implemented"))


def run_eigen(A, iters, panel):
    n = len(A)

    #QR iteration

    if len(A[0]) != n:
        panel.set_eigenvalues(
            "<p style='color:#D32F2F;'>⚠ Eigenvalues require a square matrix.</p>"
        )
        panel.set_log("")
        panel.set_convergence("")
        return

    panel.set_eigenvalues(
        "<p style='color:#757575; font-size:11px;'>Not yet implemented</p>"
    )
    panel.set_log("")
    panel.set_convergence(
        f"<p style='color:#757575; font-size:12px;'>Pending — {iters} iterations requested</p>"
    )



# ── Main Window ──────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Decomposition — Gram–Schmidt")
        self.setMinimumSize(1050, 680)
        self.resize(1280, 780)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(18, 14, 18, 18)
        root.setSpacing(10)

        # Title
        title = QLabel("QR Decomposition  —  Gram–Schmidt")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #212121;")
        sub = QLabel("Matrix m × n  (m ≥ n)  ·  Linear Solver  ·  Eigenvalue Approximation")
        sub.setStyleSheet("font-size: 11px; color: #757575;")
        root.addWidget(title)
        root.addWidget(sub)
        root.addWidget(divider())

        #allignment
        self.input_panel    = InputPanel()
        self.solution_panel = SolutionPanel()
        self.qr_panel       = QRPanel()
        self.eigen_panel    = EigenPanel()

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.input_panel,    0, 0)
        grid.addWidget(self.qr_panel,       0, 1)
        grid.addWidget(self.solution_panel, 1, 0)
        grid.addWidget(self.eigen_panel,    1, 1)

        grid.setColumnStretch(0, 430)
        grid.setColumnStretch(1, 820)
        grid.setRowStretch(1, 1)

        root.addLayout(grid, 1)

        # Connect buttons
        self.qr_panel.btn_decompose.clicked.connect(self.on_decompose)
        self.solution_panel.btn_solve.clicked.connect(self.on_solve)
        self.eigen_panel.btn_eigen.clicked.connect(self.on_eigen)

        self.statusBar().showMessage("Ready  ·  Enter matrix A and vector b")
        self.statusBar().setStyleSheet("color: #757575; font-size: 10px;")

    def on_decompose(self):
        A = self.input_panel.get_matrix()
        run_decompose(A, self.qr_panel)
        m, n = self.input_panel.m, self.input_panel.n
        self.statusBar().showMessage(f"✓  QR Decomposition complete  ({m}×{n})")

    def on_solve(self):
        A = self.input_panel.get_matrix()
        b = self.input_panel.get_b()
        run_solve(A, b, self.qr_panel, self.solution_panel)
        self.statusBar().showMessage("✓  Ax = b solved")

    def on_eigen(self):
        A = self.input_panel.get_matrix()
        iters = self.eigen_panel.iter_spin.value()
        run_eigen(A, iters, self.eigen_panel)
        self.statusBar().showMessage(f"✓  Eigenvalue search complete after {iters} iterations")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())