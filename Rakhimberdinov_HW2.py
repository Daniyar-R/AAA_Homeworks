import csv
import operator


def menu():

    """
    Prints a menu that consists of 3 items
    After input it displays one of the options
    """

    def merge_dictionary(dict_1: dict, dict_2: dict):

        """
        Takes two dictionaries as input, merges them.
        If there are identical keys, it creates a list of values.
        :return: merged dictionary
        """

        dict_3 = {**dict_1, **dict_2}
        for key, value in dict_3.items():
            if key in dict_1 and key in dict_2 and isinstance(dict_1[key], list):
                dict_3[key] = [dict_2[key], *dict_1[key]]
            elif key in dict_1 and key in dict_2 and isinstance(dict_1[key], str):
                dict_3[key] = [dict_2[key], dict_1[key]]

        return dict_3

    def choice_one():

        """
        Display the hierarchy of teams, i.e. department and all teams that are part of it
        Uses file 'Corp_Summary.csv' which should be located in same directory
        """

        common_dict = {}

        with open('Corp_Summary.csv') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            csv_list_dicts = list(reader)

        for d in csv_list_dicts:
            common_dict = merge_dictionary(common_dict, d)

        depart_structure = {}

        for dep_name in set(common_dict['Департамент']):
            for d in csv_list_dicts:
                if d['Департамент'] == dep_name:
                    if isinstance(depart_structure.get(dep_name), list):
                        depart_structure[dep_name] = [d['Отдел'], *depart_structure[dep_name]]
                    elif depart_structure.get(dep_name) is None:
                        depart_structure[dep_name] = [d['Отдел']]
            depart_structure[dep_name] = set(depart_structure.get(dep_name))

        for key, val in depart_structure.items():
            print(f'Департамент - {key}\n'
                  f'Отделы: {", ".join(val)}\n')

    def create_pivot():

        """
        create a pivot table by department, salary
        :return: a pivot table
        """

        common_dict = {}

        with open('Corp_Summary.csv') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            csv_list_dicts = list(reader)

        for d in csv_list_dicts:
            common_dict = merge_dictionary(common_dict, d)

        depart_structure = {}

        for dep_name in set(common_dict['Департамент']):
            for d in csv_list_dicts:
                if d['Департамент'] == dep_name:
                    if isinstance(depart_structure.get(dep_name), list):
                        depart_structure[dep_name] = [d['Оклад'], *depart_structure[dep_name]]
                    elif depart_structure.get(dep_name) is None:
                        depart_structure[dep_name] = [d['Оклад']]

        header = ['Название', 'Численность', 'Вилка', 'Средняя зарплата']
        pivot_table_list = [header]

        for key, val in depart_structure.items():
            row_str = [key,
                       len(val),
                       f"{min([int(i) for i in val])} - {max([int(i) for i in val])}",
                       round(sum([int(i) for i in val])/len(val))]
            pivot_table_list.append(row_str)

        return pivot_table_list

    def choice_two():

        """
        Print a summary report by departments:
        name, headcount, "fork" of salaries in the form of min - max, average salary
        """
        # source - https://stackoverflow.com/questions/52520711/how-to-output-csv-data-to-terminal-with-python
        all_rows = create_pivot()

        def pad_col(col: str, max_width: int):
            """
            :param col: a column
            :param max_width: maximum width of a cell in a column
            :return: returns the left-justified string within the given minimum width
            """
            return col.ljust(max_width)

        max_col_width = [0] * len(all_rows[0])
        for row in all_rows:
            for idx, col in enumerate(row):
                max_col_width[idx] = max(len(str(col)), max_col_width[idx])

        for row in all_rows:
            to_print = ""
            for idx, col in enumerate(row):
                to_print += pad_col(str(col), max_col_width[idx]) + " | "
            print("-"*len(to_print))
            print(to_print)

    def choice_three():
        """
        Save the summary report from the previous paragraph as a csv file.
        """

        pivot_csv_list = create_pivot()
        with open('out_pivot.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            for i in pivot_csv_list:
                writer.writerow(i)

    print('Выберите пункт, вводя соответствующее число:\n'
          '1. Вывести в понятном виде иерархию команд\n'
          '2. Вывести сводный отчёт по департаментам\n'
          '3. Сохранить сводный отчёт из предыдущего пункта в виде csv-файла')

    choice_num = int(input())

    if choice_num == 1:
        choice_one()
    elif choice_num == 2:
        choice_two()
    elif choice_num == 3:
        choice_three()
    else:
        raise ValueError('Такого пункта не существует')


if __name__ == '__main__':
    menu()
