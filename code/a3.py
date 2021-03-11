import sqlite3

db_name = "./database/A3.db"


def main():
    
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()

    # TODO DO STUFF

    print("Welcome to conference management system")
    
    userInput = "0"
    while userInput != "5":     
        interface()
        userInput = user_input()
        # switch case statements


    db_cursor.close()
    db_connection.close()




def papers_by_area(db_connection, db_cursor, s_area):
    db_cursor.execute("SELECT title FROM papers WHERE area = :s_area;", {"s_area":s_area})


def assigned_papers(db_connection, db_cursor, user):
    # Searches for all papers that user is assigned to review
    pass


def check_review(db_connection, db_cursor, review):
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

def user_input():
    userInput = input("Option ")
    return userInput
    


if __name__ == "__main__":
    main()
