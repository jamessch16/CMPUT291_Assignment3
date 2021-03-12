import sqlite3

db_name = "./A3.db"

def main():
    
    # Connect to database
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()


    # Create DiffScore view
    db_cursor.execute("DROP VIEW IF EXISTS DiffScore;")
    db_cursor.execute("CREATE VIEW DiffScore (pid, ptitle, diff) "
                        "AS SELECT p1.id, p1.title, ABS(Q3.avg_paper - Q2.avg_area) "
                        "FROM papers p1, "
                          "(SELECT AVG(r2.overall) AS avg_area, p2.area AS pa "
                          "FROM reviews r2, papers p2 "
                          "WHERE r2.paper = p2.id GROUP BY p2.area) Q2, "
                        "(SELECT AVG(r3.overall) AS avg_paper, r3.paper AS rp "
                          "FROM reviews r3 GROUP BY r3.paper) Q3 "
                        "WHERE p1.id = Q3.rp "
                        "AND p1.area = Q2.pa;")
    
    # User interface
    print("Welcome to the conference management system")

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
            outlier_papers(db_connection, db_cursor)

        elif user_input == 5 :
            pass

        else:
            print("Invalid Input! Try again.")

    db_cursor.close()
    db_connection.close()


def papers_by_area(db_connection, db_cursor):
    # Lists every paper in a given area that has at least one review 

    # Get Input
    print("List the titles of accepted papers in a given area, that have at least one review and where area is to be provided at query time, in descending order of their average overall review scores.")
    s_area = input("Area: ")



    # Perform queries
    db_cursor.execute("SELECT title "
                      "FROM papers p, reviews r "
                      "WHERE p.id = r.paper "
                      "AND p.decision = 'A' "
                      "AND area = :s_area "
                      "GROUP BY r.paper "
                      "ORDER BY AVG(r.overall) DESC;",
                      {"s_area":s_area})

    result = db_cursor.fetchall()

    # Print results
    print("\nAccepted papers in this area:")
    for row in result:
        print(row[0])
    print()

def assigned_papers(db_connection, db_cursor):
    # Searches for all papers that user is assigned to review

    print("Search for all papers assigned to a reviewer given their email")
    user = input("Input an email: ")

    # Perform queries
    db_cursor.execute("SELECT p.title "
                      "FROM papers p, reviews r, users u "
                      "WHERE u.email = :user "
                      "AND r.reviewer = u.email "
                      "AND r.paper = p.id "
                      "ORDER BY id;", 
                      {"user":user})

    result = db_cursor.fetchall()
    
    # Print result
    if len(result) == 0:
        print("No paper has been assigned to this reviewer")
    else:
        print("Papers assigned to %s:" % user)
        for row in result:
            print(row[0])
    print()


def check_review(db_connection, db_cursor):
    # Searching for paper with overall scores that differ from average overall score by certain percent
    
    # Get Input
    valid_input = False
    s_percent = -1
    while not valid_input:
        s_percent = float(input("Enter a percent (X%) for which to find inconsistent: "))

        if s_percent >= 0:
            valid_input = True
        else:
            print("Invalid input")

    print("\nSearching for paper with a review whose overall score differs by more than", s_percent, "from the average overall score.")
    print("The following are inconsistent when X = "+ str(s_percent) + "%")
    s_percent = s_percent/100
    
    # Perform Queries
    db_cursor.execute("SELECT DISTINCT p.id, p.title "
                      "FROM papers p, reviews r "
                      "WHERE r.paper = p.id "
                      "AND :s_percent < ABS(1 - r.overall/("
                        "SELECT AVG(r2.overall) "
                        "FROM reviews r2 "
                        "WHERE r2.paper = p.id)"
                      ");",
                      {"s_percent" :s_percent})

    result = db_cursor.fetchall()
    
    # Print result
    for row in result:
        print(result[0], result[1])
    print("\n")


def outlier_papers(db_connection, db_cursor):
    # For a specified interval, prints the users who have reviewed a paper
    # with a grade whose deviation from the area average is within the interval 

    # Get input
    print("Find all papers whose average differs from the area average by a value within [X, Y]")

    valid_input = False
    low = -1
    high = -1
    while not valid_input:
        low = float(input("Input X (lower bound): "))

        if low >= 0:
            valid_input = True
        else:
            print("Invalid Input")

    valid_input = False
    while not valid_input:
        high = float(input("Input Y (upper bound): "))

        if high >= low:
            valid_input = True
        else:
            print("Invalid Input")

    # Perform query
    db_cursor.execute("SELECT DISTINCT u.email, u.name "
                      "FROM DiffScore d, reviews r, users u "
                      "WHERE d.diff >= :low AND d.diff <= :high "
                      "AND d.pid = r.paper "
                      "AND r.reviewer = u.email;",
                      {"low":low, "high":high})

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
    

if __name__ == "__main__":
    main()
