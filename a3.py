import sqlite3

db_name = "./A3.db"

def main():
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()

    # TODO DO STUFF

    db_cursor.close()
    db_connection.close()
    

def papers_by_area(db_connection, db_cursor, s_area):
    db_cursor.execute("         # TODO Comress string
    
        SELECT title
        FROM papers
        WHERE area = s_area     # TODO REPLACE s_area with string
                                # TODO ORDER BY average review score
    ")


def assigned_papers(db_connection, db_cursor, user):
    # Searches for all papers that user is assigned to review
    pass


def check_review(db_connection, db_cursor, review)
    pass


def create_diff_score(db_connection, db_cursor)
    pass


if __name__ == "__main__":
    main()