import pymysql.cursors


def print_all_buildings(cursor):
    # 1. Print all buildings
    try:
        sql = "SELECT * FROM buildings"
        cursor.execute(sql)
        result = cursor.fetchall()
        print("-" * 75)
        print('id'.ljust(10), end=' ')
        print('name'.ljust(20), end=' ')
        print('location'.ljust(15), end=' ')
        print('capacity'.ljust(15), end=' ')
        print('assigned'.ljust(15), end=' ')
        print("")
        print("-" * 75)

        if len(result) != 0:
            for i in result:
                b = list(i.values())
                print(str(b[0]).ljust(10), end=' ')
                print(b[1].ljust(20), end=' ')
                print(b[2].ljust(15), end=' ')
                print(str(b[3]).ljust(15), end=' ')
                print(str(b[4]).ljust(15), end=' ')
                print("")
            print("-" * 75)
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def print_all_performances(cursor):
    # 2. Print all performances
    try:
        sql = "SELECT * FROM performances"
        cursor.execute(sql)
        result = cursor.fetchall()
        print("-" * 75)
        print('id'.ljust(10), end=' ')
        print('name'.ljust(20), end=' ')
        print('type'.ljust(15), end=' ')
        print('price'.ljust(15), end=' ')
        print('booked'.ljust(15), end=' ')
        print("")
        print("-" * 75)
        for i in result:
            b = list(i.values())
            print(str(b[0]).ljust(10), end=' ')
            print(b[1].ljust(20), end=' ')
            print(b[2].ljust(15), end=' ')
            print(str(b[3]).ljust(15), end=' ')
            print(str(b[4]).ljust(15), end=' ')
            print("")
            print("-" * 75)
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def print_all_audiences(cursor):
    # 3. Print all audiences
    try:
        sql = "SELECT * FROM audiences"
        cursor.execute(sql)
        result = cursor.fetchall()
        print("-" * 75)
        print('id'.ljust(10), end=' ')
        print('name'.ljust(20), end=' ')
        print('gender'.ljust(15), end=' ')
        print('age'.ljust(15), end=' ')
        print("")
        print("-" * 75)
        for i in result:
            b = list(i.values())
            print(str(b[0]).ljust(10), end=' ')
            print(b[1].ljust(20), end=' ')
            print(b[2].ljust(15), end=' ')
            print(str(b[3]).ljust(15), end=' ')
            print("")
            print("-" * 75)
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def insert_building(cursor):
    # 4. Insert a new building
    try:
        b_name = input("Building name: ")
        b_location = input("Building location: ")
        b_capacity = int(input("Building capacity: "))
        sql = "INSERT INTO buildings (name,location,capacity) VALUES (%s,%s,%s)"
        cursor.execute(sql, (b_name, b_location, b_capacity))
        print("A building is successfully inserted")
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def remove_building(cursor):
    # 5. Remove a building
    try:
        b_id = int(input("Building ID: "))
        sql = "SELECT * FROM buildings WHERE id = %s"
        b = cursor.execute(sql, b_id)
        if b:
            # Delete records from books
            sql1 = "DELETE FROM books WHERE EXISTS(SELECT * FROM performances " \
                   "WHERE books.performance_id = performances.id AND performances.building_id = %s)"
            cursor.execute(sql1, b_id)

            # Update performance records
            sql2 = "UPDATE performances SET booked = 0 WHERE building_id = %s"
            cursor.execute(sql2, b_id)

            # Delete records from buildings
            sql3 = "delete from buildings where id=%s"

            c = cursor.execute(sql3, b_id)
            if c:
                print("The building is successfully deleted")
            else:
                print("Error!")
        else:
            print("The building ID does not exist!")
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def insert_performance(cursor):
    # 6. INSERT INTO a new performance records
    try:
        p_name = input("Performance name: ")
        p_type = input("Performance type: ")
        p_price = int(input("Performance price: "))

        sql = "INSERT INTO performances (name,type,price) values (%s,%s,%s)"
        cursor.execute(sql, (p_name, p_type, p_price))
        print("A performance is successfully inserted")
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def remove_performance(cursor):
    # 7. Remove a performance
    try:
        p_id = int(input("performance ID: "))
        sql = "SELECT * FROM performances WHERE id=%s"
        b = cursor.execute(sql, p_id)
        if b:
            rows = cursor.fetchall()
            b_id = rows[0]['building_id']
            if b_id:
                sql1 = "UPDATE buildings SET assigned = assigned - 1 WHERE id = %s"
                cursor.execute(sql1, b_id)
            sql2 = "DELETE FROM performances WHERE id=%s"
            cursor.execute(sql2, p_id)
            print("The performance is successfully deleted")
        else:
            print("The performance ID does not exist!")
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def insert_audience(cursor):
    # 8. INSERT a new audience records
    try:
        a_name = input("Audience name: ")
        a_gender = input("Audience gender: ")
        a_age = int(input("Audience age: "))

        sql = "INSERT INTO audiences (name,gender,age) VALUES (%s,%s,%s)"
        cursor.execute(sql, (a_name, a_gender, a_age))
        print("An audience is successfully inserted")
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def remove_audience(cursor):
    # 9. Remove an audience
    try:
        a_id = int(input("audience ID: "))
        sql = "SELECT * FROM audiences WHERE id = %s"
        b = cursor.execute(sql, a_id)

        if b:
            sql1 = 'SELECT performance_id, COUNT(*) AS num_seats ' \
                   'FROM audiences JOIN books ON (audiences.id = books.audience_id) ' \
                   'WHERE audiences.id = %s ' \
                   'GROUP BY performance_id '
            cursor.execute(sql1, a_id)

            rows = cursor.fetchall()
            for row in rows:
                sql2 = "UPDATE performances SET booked = booked - %s WHERE id = %s"
                cursor.execute(sql2, (row['num_seats'], row['performance_id']))
            sql3 = "DELETE FROM audiences WHERE id = %s"
            cursor.execute(sql3, a_id)
            print("The audience is successfully deleted")
        else:
            print("The audience ID does not exist!")
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def assign_performance_to_building(cursor):
    # 10. assign a performance to a building
    try:
        b_id = int(input("Building ID: "))
        sql = "SELECT * FROM buildings WHERE id = %s"
        b = cursor.execute(sql, b_id)
        building = cursor.fetchone()
        if b:
            p_id = int(input("performance ID: "))
            sql1 = "SELECT * FROM performances WHERE id = %s"
            c = cursor.execute(sql1, p_id)
            if c:
                sql2 = "SELECT building_id FROM performances WHERE id = %s"
                cursor.execute(sql2, p_id)

                rows = cursor.fetchall()
                if rows[0]['building_id']:
                    print('A building is already assigned to this performance!')

                else:
                    sql3 = "UPDATE buildings SET assigned = assigned + 1 WHERE id = %s"
                    cursor.execute(sql3, b_id)

                    sql4 = "UPDATE performances SET building_id = %s WHERE id = %s"
                    cursor.execute(sql4, (b_id, p_id))

                    # create seats
                    sql5 = "INSERT INTO books(seat_number, performance_id) VALUES(%s, %s)"
                    cursor.executemany(sql5, [[i + 1, p_id] for i in range(building['capacity'])])
                    print("Successfully assigned a performance")
            else:
                print("The performance ID does not exist!")
        else:
            print("The building ID does not exist!")
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def book_performance(cursor):
    # 11. Book a performance
    try:
        p_id = int(input("performance ID: "))
        sql = "SELECT * FROM performances WHERE id = %s"
        a = cursor.execute(sql, p_id)
        performance = cursor.fetchone()
        if a:
            sql1 = "SELECT building_id FROM performances WHERE id = %s"
            cursor.execute(sql1, p_id)

            rows = cursor.fetchall()
            if not rows[0]['building_id']:
                print("There's no building assigned to the performance!")

            else:
                a_id = int(input("Audience ID: "))
                sql2 = "SELECT * FROM audiences WHERE id = %s"
                b = cursor.execute(sql2, a_id)
                if b:
                    seat_numbers = tuple(int(x) for x in input('Seat number: ').split(','))
                    sql3 = "SELECT * FROM books WHERE performance_id = %s AND seat_number IN %s"
                    cursor.execute(sql3, (p_id, seat_numbers))
                    seats = cursor.fetchall()
                    if seats:
                        if not all([seat['audience_id'] is None for seat in seats]):
                            print('The seat is already taken')
                        else:
                            # assign seats to audience
                            sql4 = "UPDATE books SET audience_id = %s WHERE performance_id = %s AND " \
                                   "seat_number = %s "
                            cursor.executemany(sql4, [[a_id, p_id, i] for i in seat_numbers])
                            # increase booked in performance
                            sql5 = "UPDATE performances SET booked = booked + %s WHERE id = %s"
                            cursor.execute(sql5, (len(seat_numbers), p_id))
                            print('Successfully booked a performance')
                            print('Total ticket price is', len(seat_numbers) * performance['price'])
                    else:
                        print('Invalid seat number.')
                else:
                    print("The audience ID does not exist!")
        else:
            print("The performance ID does not exist!")
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def print_performances_assigned_building(cursor):
    # 12. print all performances assigned to a building
    try:
        b_id = int(input("Building ID: "))
        sql = "SELECT * FROM buildings WHERE id = %s"
        a = cursor.execute(sql, b_id)
        if a:
            sql1 = "SELECT * FROM performances WHERE building_id = %s ORDER BY id "
            cursor.execute(sql1, b_id)
            result = cursor.fetchall()
            if result:
                print("-" * 75)
                print('id'.ljust(10), end=' ')
                print('name'.ljust(20), end=' ')
                print('type'.ljust(15), end=' ')
                print('price'.ljust(15), end=' ')
                print('booked'.ljust(15), end=' ')
                print("")
                print("-" * 75)
                for i in result:
                    b = list(i.values())
                    print(str(b[0]).ljust(10), end=' ')
                    print(b[1].ljust(20), end=' ')
                    print(b[2].ljust(15), end=' ')
                    print(str(b[3]).ljust(15), end=' ')
                    print(str(b[4]).ljust(15), end=' ')
                    print("")
                    print("-" * 75)
            else:
                print("There's no performance assigned to the building.")
        else:
            print("The building ID does not exist!")
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def print_audiences_booked_performance(cursor):
    # 13. print all audiences who booked for a performance
    try:
        p_id = int(input("Performance ID: "))
        sql = "SELECT * FROM performances WHERE id = %s"
        a = cursor.execute(sql, p_id)
        if a:
            sql1 = "SELECT DISTINCT a.* FROM audiences a JOIN books b ON(a.id = b.audience_id) " \
                   " WHERE b.performance_id = %s ORDER BY a.id "
            cursor.execute(sql1, p_id)
            result = cursor.fetchall()
            if result:
                print("-" * 75)
                print('id'.ljust(10), end=' ')
                print('name'.ljust(20), end=' ')
                print('gender'.ljust(15), end=' ')
                print('age'.ljust(15), end=' ')
                print("")
                print("-" * 75)
                for i in result:
                    b = list(i.values())
                    print(str(b[0]).ljust(10), end=' ')
                    print(b[1].ljust(20), end=' ')
                    print(b[2].ljust(15), end=' ')
                    print(str(b[3]).ljust(15), end=' ')
                    print("")
                    print("-" * 75)
        else:
            print("The performance ID does not exist!")
    except ValueError:
        print("The value you entered is invalid. Please try again.")


def print_ticket_booking_status(cursor):
    # 14. print ticket booking status of a performance
    try:
        p_id = int(input("Performance ID: "))
        sql = "SELECT * FROM performances WHERE id = %s"
        a = cursor.execute(sql, p_id)
        if a:
            sql1 = "SELECT building_id FROM performances WHERE id = %s"
            cursor.execute(sql1, p_id)

            rows = cursor.fetchall()
            if not rows[0]['building_id']:
                print("There's no building assigned to the performance!")
            else:
                print("-" * 75)
                print('seat_number'.ljust(10), end=' ')
                print('audience_id'.ljust(20), end=' ')
                print("")
                print("-" * 75)
                sql2 = "SELECT seat_number, audience_id FROM books WHERE performance_id = %s"
                cursor.execute(sql2, p_id)
                result = cursor.fetchall()
                for i in result:
                    b = list(i.values())
                    print(str(b[0]).ljust(10), end=' ')
                    print(str(b[1]).ljust(20), end=' ')
                    print("")
                    print("-" * 75)
        else:
            print("The performance ID does not exist!")
    except ValueError:
        print("The value you entered is invalid. Please try again.")


if __name__ == "__main__":
    print("=======================================================================================")
    print("1. print all buildings")
    print("2. print all performances")
    print("3. print all audiences")
    print("4. insert a new building")
    print("5. remove a building")
    print("6. insert a new performance")
    print("7. remove a performance")
    print("8. insert a new audience")
    print("9. remove an audience")
    print("10. assign a performance to a building")
    print("11. book a performance")
    print("12. print all performances assigned to a building")
    print("13. print all audiences who booked for a performance")
    print("14. print ticket booking status of a performance")
    print("15. exit")
    print("=======================================================================================")
    connection = pymysql.connect(
        host='astronaut.snu.ac.kr',
        user='BDE-2018-30',
        password='a2004b6fd8e6',
        db='BDE-2018-30',
        charset='utf8',
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    n = None
    try:
        while n != 15:
            n = int(input("Select your action: "))
            if n == 1:
                print_all_buildings(cursor)
            elif n == 2:
                print_all_performances(cursor)
            elif n == 3:
                print_all_audiences(cursor)
            elif n == 4:
                insert_building(cursor)
            elif n == 5:
                remove_building(cursor)
            elif n == 6:
                insert_performance(cursor)
            elif n == 7:
                remove_performance(cursor)
            elif n == 8:
                insert_audience(cursor)
            elif n == 9:
                remove_audience(cursor)
            elif n == 10:
                assign_performance_to_building(cursor)
            elif n == 11:
                book_performance(cursor)
            elif n == 12:
                print_performances_assigned_building(cursor)
            elif n == 13:
                print_audiences_booked_performance(cursor)
            elif n == 14:
                print_ticket_booking_status(cursor)
            elif n == 15:
                print("Bye!")
            else:
                print("Invalid input! You must type a number between 1 and 15")
    except ValueError:
        print("The value you entered is invalid. Please try again.")

    cursor.close()
    connection.close()