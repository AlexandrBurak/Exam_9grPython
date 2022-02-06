import io
import re
import datetime as dt

from typing import List, Union


class Employee:
    empl_id: int
    empl_surname: str
    empl_name: str
    empl_skill: str
    workload_sum: int

    def __init__(self, data_str: str) -> None:
        data: List[str] = data_str.split(';')
        self.empl_id = int(data[0])
        self.empl_surname = data[1]
        self.empl_name = data[2]
        self.empl_skill = data[3]
        self.workload_sum = -1

    def __str__(self):
        if self.workload_sum == -1:
            return f"{self.empl_id};{self.empl_surname};{self.empl_name};{self.empl_skill}"
        return f"{self.empl_id};{self.empl_surname};{self.empl_name};{self.empl_skill};{self.workload_sum}"

    def __repr__(self):
        if self.workload_sum == -1:
            return f"{self.empl_id};{self.empl_surname};{self.empl_name};{self.empl_skill}"
        return f"{self.empl_id};{self.empl_surname};{self.empl_name};{self.empl_skill};{self.workload_sum}"

    def without_skill(self) -> str:
        return f"{self.empl_id};{self.empl_surname};{self.empl_name}"


class Project:
    project_id: int
    project_title: str
    open_positions: int = 0

    def __init__(self, data_str: str) -> None:
        data: List[str] = data_str.split(';')
        self.project_id = int(data[0])
        self.project_title = data[1]

    def __str__(self):
        return f"{self.project_title};{self.open_positions}"

    def __repr__(self):
        return f"{self.project_title};{self.open_positions}"


class Position:
    position_id: int
    prject_id: int
    empl_id: int
    workload: int
    billing_type: str

    def __init__(self, data_str: str) -> None:
        data: List[str] = data_str.split(';')
        self.position_id = int(data[0])
        self.prject_id = int(data[1])
        self.empl_id = int(data[2])
        self.workload = int(data[3])
        self.billing_type = data[4]

    def __str__(self):
        return f"{self.position_id};{self.prject_id};{self.empl_id};{self.workload};{self.billing_type}"

    def __repr__(self):
        return f"{self.position_id};{self.prject_id};{self.empl_id};{self.workload};{self.billing_type}"


class OpenPosition:
    project_id: int
    position_id: int
    open_date: str
    open_date_dt: dt

    def __init__(self, data_str: str) -> None:
        data = data_str.split(';')
        self.project_id = int(data[0])
        self.position_id = int(data[1])
        self.open_date = data[2]
        self.open_date_dt = dt.datetime.strptime(self.open_date, "%d.%m.%Y")

    def __str__(self):
        return f"{self.project_id};{self.position_id};{self.open_date}"

    def __repr__(self):
        return f"{self.project_id};{self.position_id};{self.open_date}"


def get_data(filename: str) -> List[Union[Employee, Project, Position, OpenPosition]]:
    cls: int = int(re.findall('\d', filename)[0])
    reader: io.TextIOWrapper = open(filename)
    data_str: List[str] = reader.read().split('\n')
    if cls == 1:
        return [Employee(obj) for obj in data_str]
    elif cls == 2:
        return [Project(obj) for obj in data_str]
    elif cls == 3:
        return [Position(obj) for obj in data_str]
    elif cls == 4:
        return [OpenPosition(obj) for obj in data_str]


def send_data(filename: str, objects: List) -> None:
    writer: io.TextIOWrapper = open(filename, 'w')
    outtype: int = int(re.findall('\d', filename)[0])
    for i in range(len(objects)):
        if i == len(objects) - 1:
            if outtype == 2:
                writer.write(objects[i].without_skill())
            else:
                writer.write(str(objects[i]))
            break
        if outtype == 2:
            writer.write(objects[i].without_skill() + '\n')
        else:
            writer.write(str(objects[i]) + '\n')
    writer.close()


def tsk1(employees: List[Employee], positions: List[Position]) -> List[Employee]:
    for emp in employees:
        workload_sum: int = -1
        sums: List[int] = [pos.workload for pos in positions if emp.empl_id == pos.empl_id]
        res: int = sum(sums)
        if res != 0:
            workload_sum = res
        emp.workload_sum = workload_sum
        workload_sum = -1
    return sorted([emp for emp in employees if emp.workload_sum > 100], key=lambda x: x.workload_sum, reverse=True)


def tsk2(employees: List[Employee], positions: List[Position]):
    reader: io.TextIOWrapper = open("input8.txt")
    project_id = int(reader.read(2))
    ids: List[Position] = [pos.empl_id for pos in positions if pos.prject_id == project_id]
    return sorted([emp for emp in employees if emp.empl_id in ids], key=lambda emp: emp.empl_id)


def datein(date: dt) -> bool:
    reader: io.TextIOWrapper = open("input6.txt")
    dates: List[str] = reader.readline().split(';')
    date1: dt = dt.datetime.strptime(dates[0], "%d.%m.%Y")
    date2: dt = dt.datetime.strptime(dates[1].split('\n')[0], "%d.%m.%Y")
    if date1 <= date <= date2:
        return True
    return False


def tsk3(projects: List[Project], openpositions: List[OpenPosition]) -> List[Project]:
    reader: io.TextIOWrapper = open("input7.txt")
    project_id: int = int(reader.read(2))
    opnpos: OpenPosition = [pos for pos in openpositions if pos.project_id == project_id and datein(pos.open_date_dt)]
    res_lst: List[Project] = [prj for prj in projects if project_id == prj.project_id]
    res_lst[0].open_positions = len(opnpos)
    return res_lst


def main():
    employees: List[Employee] = get_data("input1.txt")
    projects: List[Project] = get_data("input2.txt")
    positions: List[Position] = get_data("input3.txt")
    openpositions: List[OpenPosition] = get_data("input4.txt")
    send_data('output1.txt', tsk1(employees, positions))
    send_data('output2.txt', tsk2(employees, positions))
    send_data('output3.txt', tsk3(projects, openpositions))


if __name__ == '__main__':
    main()
