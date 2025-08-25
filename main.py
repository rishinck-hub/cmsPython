from db.db_connection import DBConnection


def main():
        db = DBConnection()
        conn = db.get_connection()

if __name__=='__main__':
        main()