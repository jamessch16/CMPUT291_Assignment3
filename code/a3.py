import sqlite3

db_name = "./database/A3.db"


def main():
    
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()

    create_diff_score

    print("Welcome to conference management system")

    # Dropping view if exists and then recreating it
    db_cursor.execute("DROP VIEW IF EXISTS DiffScore;")
    db_cursor.execute("CREATE VIEW DiffScore (pid, ptitle, diff) AS SELECT p1.id, p1.title, ABS(Q3.avg_paper - Q2.avg_area) FROM papers p1, (SELECT AVG(r2.overall) AS avg_area, p2.area AS pa FROM reviews r2, papers p2 WHERE r2.paper = p2.id GROUP BY p2.area) Q2, (SELECT AVG(r3.overall) AS avg_paper, r3.paper AS rp FROM reviews r3 GROUP BY r3.paper) Q3 WHERE p1.id = Q3.rp AND p1.area = Q2.pa;")
    
    user_input = 0
    while user_input != 5:     
        interface()
        user_input = int(input())
        
        if user_input == 1:
            papers_by_area(db_connection, db_cursor)

        elif user_input == 2:
            assigned_papers(db_connection, db_cursor)

        elif user_input == 3:
            check_review(db_connection, db_cursor)

        elif user_input == 4:
            create_diff_score(db_connection, db_cursor)

        elif user_input == 5 :
            pass

        else:
            print("Invalid Input! Try again.")

    db_cursor.close()
    db_connection.close()


def papers_by_area(db_connection, db_cursor):
    # Searches all the Paper that have atleast one review 

    # Get Input
    print("List the titles of accepted papers in a given area, that have at least one review and where area is to be provided at query time, in descending order of their average overall review scores.")
    print("Area:", end=" ")
    s_area = user_input()

    # Perform queries
    db_cursor.execute("SELECT title FROM papers p, reviews r WHERE p.id = r.paper AND p.decision = 'A' AND area = :s_area GROUP BY r.paper ORDER BY AVG(r.overall) DESC;",{"s_area":s_area})
    rows = db_cursor.fetchall()

    # Print results
    print("Accepted papers in this area")
    for x in range(len(rows)):
        print(rows[x][0])
    print("\n\n")

def assigned_papers(db_connection, db_cursor):
    # Searches for all papers that user is assigned to review

    user = input("Input an email: ")

    # Perform queries
    db_cursor.execute("SELECT p.title FROM papers p, reviews r, users u WHERE u.email = :user AND r.reviewer = u.email AND r.paper = p.id ORDER BY id;", {"user":user})
    result = db_cursor.fetchall()
    
    # Print result
    if len(result) == 0:
        print("No paper has been assigned to this reviewer")
    else:
        for row in result:
            print(row[0])


def check_review(db_connection, db_cursor):
    # Searching for paper with overall scores that differ from average overall score by certain percent
    
    # Get Input
    s_percent = float(input("Enter a percent (X %) for which to find inconsistent papers  "))
    print("Searching for paper with overall scores that differ by more than",s_percent,"from their average overall score.")
    print("The following are inconsistent when X =",s_percent,"%")
    s_percent = s_percent/100
    
    # Perform Queries
    db_cursor.execute("SELECT DISTINCT p.id, p.title FROM papers p, reviews r WHERE r.paper = p.id AND :s_percent < ABS(1 - r.overall/( SELECT AVG(r2.overall) FROM reviews r2 WHERE r2.paper = p.id));",{"s_percent" :s_percent})
    rows = db_cursor.fetchall()
    
    # Print result
    for x in range(len(rows)):
        print(rows[x][0], rows[x][1])
    print("\n")


def create_diff_score(db_connection, db_cursor):
    # For a specified interval, prints the users who have reviewed a paper
    # with a grade whose deviation from the area average is within the interval 

    # Get input
    low = float(input("Input X (lower bound): "))
    high = float(input("Input Y (upper bound): "))

    # Perform query
    db_cursor.execute("SELECT DISTINCT u.email, u.name FROM DiffScore d, reviews r, users u WHERE d.diff >= :low AND d.diff <= :high AND d.pid = r.paper AND r.reviewer = u.email;", {"low":low, "high":high})

    # Print results
    result = db_cursor.fetchall()
    for row in result:
        print("Email: %s | Name: %s" % (row[0], row[1]))
    print()

def interface():
    print("Please select an option by entering a number")
    print("1. Find accepted papers")
    print("2. Find papers assigned for interview")
    print("3. Find papers with inconsistent reviews")
    print("4. Find papers according to difference score")
    print("5. Exit\n")
    print("Option: ", end="")

def user_input():
    userInput = input("")
    return userInput
    

if __name__ == "__main__":
    main()
