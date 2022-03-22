from pprint import pprint
import csv
import re

  # читаем адресную книгу в формате CSV в список contacts_list
def open_file(file):
  with open(file, encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
  pprint(contacts_list)
  print()
  return contacts_list



  # Разбиваем словосочетания на слова с помощью регулярых выражений
def get_words(text):
  pattern = r"\w+"
  word_list = re.findall(pattern, text)
  return word_list

  # Правин номера телефонов в один формат с помощью регулярых выражений
def edit_mum_ph(number):
  pattern = r"(\+7|8)?(\s*)?(\()?(\d{3})?(\))?(-|\s+)?(\d{3})?(-|\s+)?(\d{2})?(-|\s+)?(\d{2})?(\s*)?(\(*)?(доб.\s*\d+)?(\))?"
  if number == 'phone':
    result = 'phone'
  elif number == '':
    result = ''
  else:
    result = re.sub(pattern, r"+7 (\4) \7-\9-\11 \14", number, 1)
  return result

  # Проверка на дубли
def check_double(check_contacts_list, contacts_list_new, new_contact):
  try:
    double_lastname = check_contacts_list.index(new_contact[0]) + 1
    len_str = len(new_contact)
    if new_contact[1] == contacts_list_new[double_lastname // len_str][1]:
      if new_contact[2] == contacts_list_new[double_lastname // len_str][2]:
        print("Возможный дубль. Такое имя есть в списке:", new_contact[0] + ' ' + new_contact[1] + ' ' + new_contact[2], '\nСтрока:', contacts_list_new[double_lastname // len_str], "\nВы хотите объедиить с новым контактом? Новый контакт:\n", new_contact)
      else:
        print("Возможный дубль. Такое имя есть в списке:", new_contact[0] + ' ' + new_contact[1], '\nСтрока:', contacts_list_new[double_lastname // len_str], "\nВы хотите объедиить с новым контактом? Новый контакт: \n", new_contact)
    else:
      print("Возможный дубль. Такая фамиля есть в списке:", new_contact[0], '\nСтрока:', contacts_list_new[double_lastname // len_str], "\nВы хотите объедиить с новым контактом? Новый контакт: \n", new_contact)
    print()
    try:
      choose_var = int(input("\"1\" - Объединить, \"0\" - Оставить, как есть. Введите нужное начение: "))
    except: return [2]
    return [choose_var, double_lastname // len_str]
  except: return [0]

  # Объединяем задвоенные контакты
def merging_lists(list_1, list_2, index_str):
  new_list = []
  for i in range(len(list_2)):
    if list_1[index_str][i] != list_2[i]:
      if list_1[index_str][i] == "":
        new_list.append(list_2[i])
      elif list_2[i] == "":
        new_list.append(list_1[index_str][i])
      else: new_list.append(f"{list_1[index_str][i]} / {list_2[i]}")
    else: new_list.append(list_2[i])
  return new_list


def repair_contact_list(contacts_list):
  contacts_list_new = []
  check_list = []
  for string in contacts_list:
    new_string = get_words(string[0])
    if get_words(string[1]) != "":
      new_string += get_words(string[1])
    if get_words(string[2]) != "":
      new_string += get_words(string[2])
    # Если нет имени либо имени и отчества, змаменяем пустыми ячейками
    quantity = 3 - len(new_string)
    new_string += [''] * quantity

    new_string.append(string[3])
    new_string.append(string[4])
    new_string.append(edit_mum_ph(string[5]))
    new_string.append(string[6])

    check_d = check_double(check_list, contacts_list_new, new_string)
    if check_d[0] == 0:
      check_list += new_string
      contacts_list_new.append(new_string)
    elif check_d[0] == 1:
      contacts_list_new[check_d[1]] = merging_lists(contacts_list_new, new_string, check_d[1])

      n = 0
      for j in range(check_d[1] * len(new_string), check_d[1] * len(new_string) + len(new_string)):
        check_list[j] = contacts_list_new[check_d[1]][n]
        n += 1
      print("Строки объединины")
    else:
      print("Неверное значение")
      repair_contact_list(contacts_list)

  return contacts_list_new

  # код для записи файла в формате CSV
def upload_file(contacts_list_new):
  with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list_new)
    print("Файл успешно загружен")


if __name__ == "__main__":
  contacts_list = open_file("phonebook_raw.csv")
  contacts_list_new = repair_contact_list(contacts_list)
  print()
  print("")
  for i in contacts_list_new:
    print(i)
  if int(input("Для записи контактов в файл, введите \"1\": ")) == 1:
    upload_file(contacts_list_new)



