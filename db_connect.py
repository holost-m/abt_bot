import sqlite3

con = sqlite3.connect("abt_db.db")

# получаем курсор
cursor = con.cursor()



class Children:
    # вернуть список всех tg_id
    @staticmethod
    def get_all_tg_id():
        cursor.execute("SELECT tg_id FROM Children")
        res = list(map(lambda x: x[0], cursor.fetchall()))
        return res


    # Добавить участника
    @classmethod
    def add_children(cls, tg_id, name, lastname, age, group_abt):
        if tg_id not in cls.get_all_tg_id():
            children = (tg_id, name, lastname, age, group_abt)
            cursor.execute("INSERT INTO Children (tg_id, name, lastname, age, group_abt) VALUES (?, ?, ?, ?, ?)", children)
            con.commit()
            return True
        return False

    # Получить список всех участников
    @classmethod
    def get_all_children(cls):
        cursor.execute("SELECT * FROM Children")
        res = list(cursor.fetchall())
        return res

    # Получить список участников отряда
    @classmethod
    def get_children_by_group(cls, group_abt):
        cursor.execute("SELECT * FROM Children WHERE group_abt=?", (group_abt,))
        res = list(cursor.fetchall())
        return res

    # Удалить участника по id
    @classmethod
    def delete_children_by_id(cls, id):
        cursor.execute("DELETE FROM Children WHERE id=?", (id,))
        con.commit()

    # Удалить все из Children
    @classmethod
    def delete_all(cls):
        cursor.execute('DELETE from Children')
        con.commit()

    # Получить id по имени и фамилии
    @classmethod
    def get_id_by_name(cls, name, lastname):
        cursor.execute("SELECT id FROM Children WHERE name=? AND lastname=?", (name, lastname))
        res = cursor.fetchone()

        return res[0]

    # Получить имя и фамилию по tg_id
    @classmethod
    def get_name_lastname_by_tg_id(cls, tg_id):
        cursor.execute("SELECT name, lastname FROM Children WHERE tg_id=?", (tg_id,))
        res = cursor.fetchone()
        return res

    # Получить tg_id по id
    @classmethod
    def get_tg_id_by_id(cls, id):
        cursor.execute("SELECT tg_id FROM Children WHERE id=? ", (id,))
        res = cursor.fetchone()
        return res[0]

    # Получить id по tg_id
    @classmethod
    def get_id_by_tg_id(cls, tg_id):
        cursor.execute("SELECT id FROM Children WHERE tg_id=? ", (tg_id,))
        res = cursor.fetchone()
        return res[0]



class Marks:
    # Проверить все имена значков
    @classmethod
    def __get_all_name(cls):
        cursor.execute("SELECT name FROM Marks")
        res = list(map(lambda x: x[0], cursor.fetchall()))
        return res

    # Добавить значок
    @classmethod
    def add_mark(cls, name, description, photo_name, level=0):
        if level in (1, 2) and name not in cls.__get_all_name():
            mark = (name, description, photo_name, level)
            cursor.execute("INSERT INTO Marks (name, description, photo_name, level) VALUES (?, ?, ?, ?)",
                           mark)
            con.commit()
            return True
        return False

    # Получить список всех значков
    @classmethod
    def get_all_marks(cls):
        cursor.execute("SELECT * FROM Marks")
        res = list(cursor.fetchall())
        return res

    # Получить список всех значков
    @classmethod
    def get_all_marks_name(cls):
        cursor.execute("SELECT name FROM Marks")
        res = list(cursor.fetchall())
        return res


    # Получить информацию по значку по его имени (id, name, description, photo_name, level)
    @classmethod
    def get_one_mark(cls, name):
        cursor.execute("SELECT * FROM Marks WHERE name=?", (name,))
        res = cursor.fetchone()
        return res

    # Удалить значок по имени
    @classmethod
    def delete_mark(cls, name):
        cursor.execute("DELETE FROM Marks WHERE name=?", (name,))
        con.commit()

    # Удалить все из Marks
    @classmethod
    def delete_all(cls):
        cursor.execute('DELETE from Marks')
        con.commit()

    # Получить id по имени значка
    @classmethod
    def get_id_by_name(cls, name):
        cursor.execute("SELECT id FROM Marks WHERE name=?", (name,))
        res = cursor.fetchone()
        return res[0]


class Admins:
    # вернуть список всех tg_id
    @staticmethod
    def get_all_tg_id():
        cursor.execute("SELECT tg_id FROM Admins")
        res = list(map(lambda x: x[0], cursor.fetchall()))

        return res

    # Добавить члена ОК
    @classmethod
    def add_admin(cls, tg_id, name, lastname, level, super=0):
        if tg_id not in cls.get_all_tg_id():
            admin = (tg_id, name, lastname, level, super)
            cursor.execute("INSERT INTO Admins (tg_id, name, lastname, level, super) VALUES (?, ?, ?, ?, ?)", admin)
            con.commit()
            return True
        return False

    # Получить список всех членов ОК
    @classmethod
    def get_all_admins(cls):
        cursor.execute("SELECT * FROM Admins")
        res = list(cursor.fetchall())
        return res

    # Удалить члена ОК по id
    @classmethod
    def delete_admin_by_id(cls, id):
        cursor.execute("DELETE FROM Admins WHERE id=?", (id,))
        con.commit()

    # Удалить все из Admins
    @classmethod
    def delete_all(cls):
        cursor.execute('DELETE from Admins')
        con.commit()

    # Получить id по th_id
    @classmethod
    def get_id_by_tg_id(cls, tg_id):
        cursor.execute("SELECT id FROM Admins WHERE tg_id=?", (tg_id,))
        res = cursor.fetchone()
        return res[0]

    # Получить имя по id
    @classmethod
    def get_name_lastname_by_id(cls, id):
        cursor.execute("SELECT name, lastname FROM Admins WHERE id=?", (id,))
        res = cursor.fetchone()
        return res


class Children_marks:
    # Добавить значок
    @classmethod
    def add_mark(cls, children_id, marks_id, date_mark, admin_id):
        mark_info = (children_id, marks_id, date_mark, admin_id)
        cursor.execute("INSERT INTO Children_marks (children_id, marks_id, date_mark, admin_id) VALUES (?, ?, ?, ?)", mark_info)
        con.commit()
        return True

    # Удалить значок участнику
    @classmethod
    def delete_mark_by_id(cls, id):
        cursor.execute("DELETE FROM Children_marks WHERE id=?", (id,))
        con.commit()

    # Вернуть все значки из таблицы
    @classmethod
    def get_all_children_marks(cls):
        cursor.execute("SELECT * FROM Children_marks")
        res = list(cursor.fetchall())
        return res

    # Вернуть все значки с информацией
    @classmethod
    def get_all_children_marks_info(cls):
        cursor.execute('''SELECT Children_marks.id, Children_marks.date_mark, Children.id,  Children.name, Children.lastname,
       Children.age, Children.group_abt, 
       Marks.id, Marks.name, Admins.id, Admins.name, Admins.lastname
       
                          FROM Children_marks
                          LEFT JOIN Children ON Children_marks.children_id = Children.id
                          LEFT JOIN Marks ON Marks.id = Children_marks.marks_id
                          LEFT JOIN Admins ON Admins.id = Children_marks.admin_id''')
        res = list(cursor.fetchall())
        return res

    # сколько поставили в день
    @classmethod
    def count_of_marks(cls, id_admin, date_mark):
        cursor.execute("SELECT COUNT(id) FROM Children_marks WHERE admin_id=? AND date_mark=?", (id_admin, date_mark))
        res = cursor.fetchone()
        if res:
            res = res[0]
        else:
            res = 0
        return res

    # Удалить все из Children_marks
    @classmethod
    def delete_all(cls):
        cursor.execute('DELETE from Children_marks')
        con.commit()

    # Мои значки
    @classmethod
    def my_marks(cls, id):
        cursor.execute('''SELECT Marks.name FROM Children_marks LEFT JOIN Marks ON Marks.id = Children_marks.marks_id WHERE Children_marks.children_id=?''', (id,) )
        res = list(cursor.fetchall())
        return res

class Timetable:
    # Добавить расписание на день
    @classmethod
    def add_timetable(cls, date_table, photo_name):
        timetable_info = (date_table, photo_name)
        cursor.execute("INSERT INTO Timetable (date_table, photo_name) VALUES (?, ?)",
                       timetable_info)
        con.commit()
        return True

    # Вернуть расписание на день
    @classmethod
    def get_timetable_by_day(cls, date_table):
        cursor.execute("SELECT * FROM Timetable WHERE date_table=?", (date_table,))
        res = cursor.fetchone()
        return res

    # Вернуть все расписания
    @classmethod
    def get_timetable(cls):
        cursor.execute("SELECT * FROM Timetable")
        res = list(cursor.fetchall())
        return res

    # Удалить все из Timetable
    @classmethod
    def delete_all(cls):
        cursor.execute('DELETE from Timetable')
        con.commit()

class Dayinfo:
    # Добавить информацию по дню
    @classmethod
    def add_dayinfo(cls, date_day, info):
        dayinfo = (date_day, info)
        cursor.execute("INSERT INTO Dayinfo (date_day, info) VALUES (?, ?)",
                       dayinfo)
        con.commit()
        return True

    # Вернуть информацию по дню
    @classmethod
    def get_dayinfo_by_day(cls, date_day):
        cursor.execute("SELECT * FROM Dayinfo WHERE date_day=?", (date_day,))
        res = cursor.fetchone()
        return res

    # Удалить инфу по дате
    @classmethod
    def delete_day(cls, date_day):
        cursor.execute('DELETE from Dayinfo WHERE date_day=?', (date_day,))
        con.commit()

    # Удалить все из Dayinfo
    @classmethod
    def delete_all(cls):
        cursor.execute('DELETE from Dayinfo')
        con.commit()




def drop_all_info_db():
    # Dayinfo.delete_all()
    Timetable.delete_all()
    Children_marks.delete_all()
    Admins.delete_all()
    # Marks.delete_all()
    Children.delete_all()


# Children_marks.add_mark(1, 1, '2024-08-01', 2)
# print(Children_marks.get_all_children_marks_info())