from utils.data_management import init_db, engine, metadata

def create_database():
    print("데이터베이스 생성 중...")
    init_db()
    print("데이터베이스 생성 완료.")

if __name__ == "__main__":
    create_database()