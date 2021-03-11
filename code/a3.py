import sqlite3

db_name = "./database/A3.db"


def main():
    
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()

    print("Welcome to conference management system")
    
    userInput = 0
    while userInput != 5:     
        interface()
        user_input = int(input("\nOption"))
        
        if user_input == 1:
            arg_input = input("Input an area: ")
            papers_by_area(db_connection, db_cursor, arg_input)

        if user_input == 2:
            arg_input = input("Input an email: ")
            assigned_papers(db_connection, db_cursor, arg_input)

        if user_input == 3:
            arg_input = int(input("Input an acceptable deviation: "))
            check_review(db_connection, db_cursor, arg_input)

        if user_input == 4:
            create_diff_score(db_connection, db_cursor)

    db_cursor.close()
    db_connection.close()


def papers_by_area(db_connection, db_cursor, s_area):
    db_cursor.execute("SELECT title FROM papers WHERE area = :s_area;", {"s_area":s_area})


def assigned_papers(db_connection, db_cursor, user):
    # Searches for all papers that user is assigned to review
    db_cursor.execute("SELECT p.title FROM papers p, reviews r, users u WHERE u.email = :user AND r.reviewer = u.email AND r.paper = p.id ORDER BY id;", {"user":user})
    result = db_cursor.fetchall()
    
    if len(result) == 0:
        print("No paper has been assigned to this reviewer")
    else:
        for row in result:
            print(row[0])


def check_review(db_connection, db_cursor, accepted_deviation):
    pass


def create_diff_score(db_connection, db_cursor):
    pass


def interface():
    print("Please select an option by entering a number")
    print("1. Find accepted papers")
    print("2. Find papers assigned for review")
    print("3. Find papers with inconsistent reviews")
    print("4. Find papers according to difference score")
    print("5. Exit\n")


if __name__ == "__main__":
    main()