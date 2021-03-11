import sqlite3

db_name = "./database/A3.db"


def main():
    
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()

    # TODO DO STUFF

    print("Welcome to conference management system")
    
    userInput = 0
    while userInput != 5:     
        interface()
        user_input = int(input("\nOption"))
        
        if user_input == 1:
            papers_by_area(db_connection, db_cursor)

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




def papers_by_area(db_connection, db_cursor):
    print("List the titles of accepted papers in a given area, that have at least one review and where area is to be provided at query time, in descending order of their average overall review scores.")
    print("Area:", end=" ")
    s_area = user_input()
    db_cursor.execute("SELECT title FROM papers p, reviews r WHERE p.id = r.paper AND p.decision = 'A' AND area = :s_area GROUP BY r.paper ORDER BY AVG(r.overall) DESC;",{"s_area":s_area})
    rows = db_cursor.fetchall()
    print("Accepted papers in this area")
    for x in range(len(rows)):
        print(rows[x][0])
    print("\n\n")

def assigned_papers(db_connection, db_cursor, user):
    # Searches for all papers that user is assigned to review
    db_cursor.execute("SELECT p.title FROM papers p, reviews r, users u WHERE u.email = :user AND r.reviewer = u.email AND r.paper = p.id ORDER BY id;", {"user":user})
    result = db_cursor.fetchall()
    
    if len(result) == 0:
        print("No paper has been assigned to this reviewer")
    else:
        for row in result:
            print(row[0])


def check_review(db_connection, db_cursor, acceptable_deviation):
    pass


def create_diff_score(db_connection, db_cursor):
    pass


def interface():
    print("Please select an option by entering a number")
    print("1. Find accepted papers")
    print("2. Find papers assigned for interview")
    print("3. Find papers with inconsistent reviews")
    print("4. Find papers according to difference score")
    print("5. Exit\n")
    print("Option", end=" ")

def user_input():
    userInput = input("")
    return userInput
    

if __name__ == "__main__":
    main()
