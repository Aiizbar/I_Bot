import sqlite3


class SnowRace():
    def __init__(self, name_db):
        con = sqlite3.connect(name_db)
        self.cur = con.cursor()

    def race_members(self, data, start):
        members = []
        name = []
        result = self.cur.execute(f"""SELECT trip_id FROM trips
                    WHERE start_point = '{start}' and start_date = '{data}'""").fetchall()
        for i in result:
            x = self.cur.execute(f"""SELECT person_id FROM members
                        WHERE trip_id = {i[0]}""").fetchall()
            for j in x:
                members.append(j[0])
        for i in members:
            x = self.cur.execute(f"""SELECT surname, name FROM participants
                        WHERE '{i}' = id""").fetchall()
            for j in x:
                name.append(j[0]+' '+j[1])
        return name

    def visited(self, family):
        members = []
        citys = []
        trip_id = self.cur.execute(f"""SELECT id FROM participants
                    WHERE surname = '{family}'""").fetchall()
        for i in trip_id:
            members.append(self.cur.execute(f"""SELECT trip_id FROM members
                        WHERE person_id = {i[0]}""").fetchall())
        for i in members:
            a = self.cur.execute(f"""SELECT start_point, end_point FROM trips
                        WHERE trip_id = {i[0]}""").fetchall()
            if a[0] not in citys:
                citys.append(a[0])
            if a[1] not in citys:
                citys.append(a[1])
        return citys.sort()


sr = SnowRace("race.db")
print(*sr.visited("Fogg"), sep="\n")