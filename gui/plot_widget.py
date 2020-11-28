from PySide2 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse, BoxStyle

from data_loader import curr


class PlotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.data = None

    def update_plot(self, data):

        # python data object
        self.data = data

        # data is currently setup where members == rows
        member = self.data.members[0]  # get the first member

        # plot A
        plot_a_data = member.plot_a_data()
        plot_a_labels = member.plot_a_labels()
        plot_a_desc = member.plot_a_desc()

        # plot B
        plot_b_data = member.plot_b_data()
        plot_b_labels = member.plot_b_labels()
        plot_b_desc = member.plot_b_desc()

        # plot C
        plot_c_data = member.plot_c_data()
        plot_c_labels = member.plot_c_labels()
        plot_c_desc = member.plot_c_desc()

        # The instance
        fig = Figure(
            figsize=(7, 5),
            dpi=65,
            facecolor=(1, 1, 1),
            edgecolor=(0, 0, 0),
            tight_layout=True,
        )

        # create a grid for our layout
        widths = [3, 2, 1]
        heights = [1, 100]
        gs = fig.add_gridspec(2, 3, width_ratios=widths, height_ratios=heights)

        # Is the area onto which the figure is drawn (our backend)
        self.canvas = FigureCanvas(fig)

        # layout wrappers to contain this widget
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.canvas)

        # add subplots using the grid
        sp1 = fig.add_subplot(gs[1, 0],)
        sp2 = fig.add_subplot(gs[1, 1], sharey=sp1)
        sp3 = fig.add_subplot(gs[1, 2], sharey=sp1)
        title = fig.add_subplot(gs[0, :])
        title.spines["bottom"].set_visible(False)
        title.axes.get_xaxis().set_visible(False)
        title.axes.get_yaxis().set_visible(False)

        # Hide some default matplotlib elements
        for sp in [sp1, sp2, sp3, title]:
            sp.spines["left"].set_visible(False)
            sp.spines["right"].set_visible(False)
            sp.spines["top"].set_visible(False)
            sp.get_yaxis().set_visible(False)
            sp.tick_params(width=0, labelsize=12)  # ticks gone, text slightly bigger

        bar1, *_ = sp1.bar(plot_a_labels, plot_a_data, width=0.95, color="#006595")
        bar2, *_ = sp2.bar(plot_b_labels, plot_b_data, width=0.95, color="#6cb33f")

        line, *_ = sp1.plot(
            plot_a_labels, plot_a_data, linewidth=10, zorder=10, color="#a6217c"
        )

        sp1.plot()

        # reorganize the data to arrays of single values
        stack_data = [[plot_c_data[0]], [plot_c_data[1]], [plot_c_data[2]]]

        # stack bottom
        p1 = sp3.bar(plot_c_labels, stack_data[0], width=0.95, color="#006595",)

        # stack mid
        p2 = sp3.bar(
            plot_c_labels,
            stack_data[1],
            bottom=stack_data[0],
            width=0.95,
            color="#6cb33f",
        )

        # stack top NOTE see how we add the bottom 2 stacks to get the starting place
        p3 = sp3.bar(
            plot_c_labels,
            stack_data[2],
            bottom=plot_c_data[1] + plot_c_data[0],
            width=0.95,
            color="#a6217c",
        )

        # helper func
        def add_text(sp, x, y, s, c="white"):
            sp.text(
                x=x,
                y=y,
                s=s,
                horizontalalignment="center",
                verticalalignment="center",
                color=c,
                weight="bold",
            )

        # helper func
        def gen_descs(sp, data, desc, custom_height=None, color="white"):
            for i in range(len(desc)):
                add_text(sp, i, data[i] / 2, desc[i], color)

        # add text to the first 2 bar charts
        gen_descs(sp=sp1, data=plot_a_data, desc=plot_a_desc)
        gen_descs(sp=sp2, data=plot_b_data, desc=plot_b_desc, color="white")

        h = [
            plot_c_data[0] / 2,
            plot_c_data[0] + (plot_c_data[1] / 2),
            plot_c_data[0] + plot_c_data[1] + plot_c_data[2] / 2,
        ]

        # add text the the stack plot
        add_text(sp3, 0, h[0], plot_c_desc[0])
        add_text(sp3, 0, h[1], plot_c_desc[1])
        add_text(sp3, 0, h[2], plot_c_desc[2])

        height_offset = -20

        # block of text
        title.text(
            x=0.095,
            y=height_offset,
            s=f"Index: {member.age} \nPrice: ${curr(member.earnings)} \nScore: {member.retire} \nFunds: {member.exp_payout} years",
            color="white",
            bbox=dict(facecolor="gray", edgecolor="gray", boxstyle="round,pad=2"),
            horizontalalignment="left",
            verticalalignment="center",
            size=14,
        )

        # block of text with round bounding box
        title.text(
            x=0.25,
            y=height_offset,
            s=f"Start With \nMX indexed annuity: \nOld Value: ${curr(member.ann_pen)} \nNew Value: ${curr(member.total_pay)}",
            color="white",
            bbox=dict(facecolor="gray", edgecolor="gray", boxstyle="round,pad=2"),
            horizontalalignment="left",
            verticalalignment="center",
            size=14,
        )

        # block of text with arrow
        title.text(
            x=0.42,
            y=height_offset,
            s=f"Starting ${curr(member.mem_get)}\nmore for \ncontributing ${curr(member.cont_more)}\neach year",
            color="white",
            bbox=dict(facecolor="gray", edgecolor="gray", boxstyle="round,pad=2"),
            horizontalalignment="left",
            verticalalignment="center",
            size=14,
        )

        # block of text with round bounding box
        title.text(
            x=0.63,
            y=height_offset,
            s=f"End With \nTDI and indexed benefit: \nAnnual Rate: ${curr(member.db_ann_pen)} \nTotal Payout: ${curr(member.db_tot_pay)}",
            color="white",
            bbox=dict(facecolor="gray", edgecolor="gray", boxstyle="round,pad=2"),
            horizontalalignment="left",
            verticalalignment="center",
            size=14,
        )

        self.canvas.draw()
