import csv


def curr(val):
    return "{:,}".format(val)


class Member(object):
    def __init__(
        self,
        fut_emp_contrib,
        acc_val,
        total_exp,
        db_fut_emply_contrib,
        db_com_val,
        db_fut_pen_pay,
        aiw,
        cola,
        age,
        earnings,
        retire,
        exp_payout,
        surv_pen,
        ann_pen,
        total_pay,
        mem_get,
        cont_more,
        db_ann_pen,
        db_tot_pay,
    ):
        self.fut_emp_contrib = int(fut_emp_contrib)
        self.acc_val = int(acc_val)
        self.total_exp = int(total_exp)
        self.db_fut_emply_contrib = int(db_fut_emply_contrib)
        self.db_com_val = int(db_com_val)
        self.db_fut_pen_pay = int(db_fut_pen_pay)
        self.aiw = int(aiw)
        self.cola = int(cola)
        self.age = int(age)
        self.earnings = int(earnings)
        self.retire = int(retire)
        self.exp_payout = int(exp_payout)
        self.surv_pen = int(surv_pen)
        self.ann_pen = int(ann_pen)
        self.total_pay = int(total_pay)
        self.mem_get = int(mem_get)
        self.cont_more = int(cont_more)
        self.db_ann_pen = int(db_ann_pen)
        self.db_tot_pay = int(db_tot_pay)

    def plot_a_data(self):
        return [
            self.fut_emp_contrib,
            self.acc_val,
            self.total_exp,
        ]

    def plot_a_labels(self):
        return [
            "Starting Value \nContributions",
            "Accumulated Values of \nContributions",
            "Total Expected \nPayments",
        ]

    def plot_a_desc(self):
        d = self.plot_a_data()

        return [
            f"${curr(d[0])}",
            f"Account balance \n ${curr(d[1])}",
            f"Future \nPayments \n ${curr(d[2])}",
        ]

    def plot_b_data(self):
        return [
            self.db_fut_emply_contrib,
            self.db_com_val,
        ]

    def plot_b_labels(self):
        return [
            "Starting Value \nContributions",
            "Accumulated Values of \nContributions",
        ]

    def plot_b_desc(self):
        d = self.plot_b_data()

        return [
            f"${curr(d[0])}",
            f"Account balance \n ${curr(d[1])}",
        ]

    def plot_c_data(self):
        return [
            self.db_fut_pen_pay,
            self.aiw,
            self.cola,
        ]

    def plot_c_labels(self):
        return [
            "Allocation of assets",
        ]

    def plot_c_desc(self):
        d = self.plot_c_data()
        return [
            f"Tesla \n${curr(d[0])}",
            f"Google ${curr(d[1])}",
            f"Apple ${curr(d[2])}",
        ]


class PlanGroup(object):
    def __init__(self):
        self.members = []

    def create_member(self, r):
        self.members.append(
            Member(
                fut_emp_contrib=r[0],  # ... description
                acc_val=r[1],  # ... description
                total_exp=r[2],  # total expected pension payments
                db_fut_emply_contrib=r[3],  # ... description
                db_com_val=r[4],  # ... description
                db_fut_pen_pay=r[5],  # ... description
                aiw=r[6],  # ... description
                cola=r[7],  # ... description
                age=r[8],  # ... description
                earnings=r[9],  # ... description
                retire=r[10],  # ... description
                exp_payout=r[11],  # ... description
                surv_pen=r[12],  # ... description
                ann_pen=r[13],  # ... description
                total_pay=r[14],  # ... description
                mem_get=r[15],  # ... description
                cont_more=r[16],  # ... description
                db_ann_pen=r[17],  # ... description
                db_tot_pay=r[18],  # ... description
            )
        )


def data_load(csv_path):
    """All data to needed to generate the plot is loaded here
    """
    plan_group = PlanGroup()

    with open(csv_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        next(reader, None)  # skip the headers

        for row in reader:
            plan_group.create_member(r=row)

    return plan_group
