from operator import itemgetter
from pprint import pprint
import csv
import re


# читаем адресную книгу в формате CSV в список contacts_list
def read_csv():

    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    pprint(contacts_list)
    return contacts_list


# TODO 1: выполните пункты 1-3 ДЗ
# Разделение ФИО на отдельные элементы
def separate_fio(fio_list):

    fio = " ".join(fio_list)
    return fio.split(' ')[:3]


# Приведение номера телефона к единому формату
def normalisation_phone(phone):

    if phone != '':

        pattern = (r"(\+7|8)\s*((\(\d{3}\))|\d{3})(\s*|\-)(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
                   r"(\s*(\(|)(доб.)\s*\d{4}(\)|)|)")
        check = re.match(pattern, phone)

        if check is not None:

            t = re.sub(r"^8", '+7', phone)
            t1 = re.sub(r" \(| ", '(', t, 1)
            t2 = re.sub(r"\+7\d{3}", f'+7({t1[2:5]})', t1, 1)
            t3 = re.sub(r"\)", ' ', t2)
            t4 = re.sub(r"  | |-", ')', t3, 1)
            t5 = re.sub(r"\)\d{4}", f'){t4[7:10]}-{t4[10]}', t4, 1)
            t6 = re.sub(r"-\d{3}", f'-{t5[11:13]}-{t5[13]}', t5, 1)
            res = re.sub(r" \(доб. | доб. ", f' доб.', t6, 1)

            return [res.rstrip()]
    return ['']


# Удаление дубликатов
def duplicate_delete(dupl_list):

    save_list = sorted(dupl_list, key=itemgetter(0, 1, 2))

    count = 1
    while count != len(save_list)-1:

        if save_list[count][:2] == save_list[count+1][:2]:

            for i in range(2, len(save_list[count])):

                if save_list[count][i] == '':
                    save_list[count][i] = save_list[count+1][i]

            save_list.pop(count+1)
            count -= 1

        count += 1

    return save_list


# Функция обрабатывает данные и приводит их к стандартному виду
def normalisation_data(contacts_list):

    contacts_list_fix = list()

    contacts_list_fix.append(contacts_list[0])
    for item in contacts_list[1:]:
        fio_list = separate_fio(item[:3])
        phone = normalisation_phone(item[5])
        full_info = fio_list+item[3:5]+phone+item[6:7]
        contacts_list_fix.append(full_info)

    return duplicate_delete(contacts_list_fix)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
def write_csv(contacts_list):

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(contacts_list)


if __name__ == '__main__':

    contacts_list = read_csv()
    update_contacts = normalisation_data(contacts_list)
    write_csv(update_contacts)
