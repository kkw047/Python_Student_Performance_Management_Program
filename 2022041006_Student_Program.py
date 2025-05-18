##################

# 프로그램명: Student Performance Management Program

# 작성자: 소프트웨어학부 / 김건우

# 작성일: 4/11

# 프로그램 설명: 학생 성적정보 프로그램이다.
#              키보드로부터 학번, 이름, 영어점수, C-언어 점수, 파이썬 점수를 입력받아 총점, 평균, 학점, 등수를  계산하는 프로그램
#              값은 범위 내에서만 입력
#              DB 추가

###################
import pymysql

#db 설정 - > 사용자에 따라 다름
db_host = 'localhost'
db_user = 'root'
db_password = 'woohaha4361!'
db_name = 'student'
db_charset = 'utf8mb4'  # 문자 인코딩 설정

# GradeManager 클래스 (수정됨)
class GradeManager:
    def __init__(self):
        self.students = []
        self.initialized = False
        self.conn = None  # 데이터베이스 연결 객체
        self.cursor = None  # 커서 객체

    #DB 연동
    def connect_db(self):
        """데이터베이스 연결"""
        try:
            self.conn = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name,
                                        charset=db_charset)
            self.cursor = self.conn.cursor()
            print("데이터베이스 연결 성공")
        except pymysql.MySQLError as e:
            print(f"데이터베이스 연결 오류: {e}")
            exit()  # 연결 실패 시 프로그램 종료

    def disconnect_db(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("데이터베이스 연결 종료")

    def create_table(self):
        """students 테이블 생성 (생성 되어있으면 무시)"""
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS students (
                student_id VARCHAR(20) PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                english_score INTEGER NOT NULL CHECK (english_score BETWEEN 0 AND 100),
                c_language_score INTEGER NOT NULL CHECK (c_language_score BETWEEN 0 AND 100),
                python_score INTEGER NOT NULL CHECK (python_score BETWEEN 0 AND 100),
                total_score INTEGER,
                average REAL,
                grade VARCHAR(2),
                `rank` INTEGER 
            )
            """
            #db 에서는 정렬을 rank로 사용함 따라서 `` 을 추가해서 그 테이블 이름으로 알아먹게함
            self.cursor.execute(sql)
            self.conn.commit()
            print("students 테이블 생성 (이미 존재하는 경우 무시)")
        except pymysql.MySQLError as e:
            print(f"테이블 생성 오류: {e}")

    def get_correct_score(self, prompt):
        while True:
            score = input(prompt).strip()
            if not score:
                print("입력 오류: 점수는 빈 값일 수 없습니다. 다시 입력하세요.")
                continue
            if score.isdigit():
                score = int(score)
                if 0 <= score <= 100:
                    return score
                else:
                    print("입력 오류: 점수는 0과 100 사이여야 합니다.")
            else:
                print("입력 오류: 숫자 형식이 아닙니다. 올바른 숫자를 입력하세요.")

    def first_Student_input(self):
        self.students.clear()
        self.initialized = True

        for i in range(5):
            print(f"\n{i + 1}번째 학생 정보 입력:")
            student_id = input("학번: ")
            name = input("이름: ")
            english = self.get_correct_score("영어 점수 (0~100): ")
            c_language = self.get_correct_score("C-언어 점수 (0~100): ")
            python_score = self.get_correct_score("파이썬 점수 (0~100): ")

            new_student = Student(student_id, name, english, c_language, python_score)
            new_student.calculate_total_and_average()
            new_student.calculate_grade()

            self.insert_student_to_db(new_student)  # DB에 학생 정보 삽입
            self.students.append(new_student)

        print("\n초기 학생 입력 완료")

    def insert_student_to_db(self, student):
        """학생 정보를 데이터베이스에 삽입"""
        try:
            sql = """
            INSERT INTO students (student_id, name, english_score, c_language_score, python_score, total_score, average, grade, `rank`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (student.student_id, student.name, student.english, student.c_language, student.python_score,
                      student.total_score, student.average, student.grade, student.rank)
            self.cursor.execute(sql, values)
            self.conn.commit()
            print(f"{student.name} 학생 정보 DB에 삽입 완료")
        except pymysql.MySQLError as e:
            print(f"DB 삽입 오류: {e}")

    def rank_students(self):
        sorted_students = sorted(self.students, key=lambda x: x.total_score, reverse=True)
        for rank, student in enumerate(sorted_students, start=1):
            student.rank = rank
        return sorted_students

    def print_students(self, ranking=False):
        # 데이터베이스에서 학생 정보를 가져오도록 수정
        self.students = self.get_all_students_from_db()  # 최신으로 업데이트
        if not self.students:
            print("\n출력할 학생 데이터가 없습니다.\n")
            return

        self.rank_students()

        if ranking:
            sorted_students = self.rank_students()
            title = "성적관리 프로그램 (총점 기준 정렬 출력)"
        else:
            sorted_students = self.students
            title = "성적관리 프로그램 (기본 출력)"

        print(f"\n\n{title:^96}")
        print("=" * 96)
        print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<12}{:<10}{:<10}".format(
            "학번", "이름", "영어", "C-언어", "파이썬", "총점", "평균", "학점", "등수"
        ))
        print("=" * 96)

        for student in sorted_students:
            print("{:<11}{:<11}{:<11}{:<11}{:<11}{:<11}{:<14.2f}{:<11}{:<11}".format(
                student.student_id, student.name, student.english, student.c_language,
                student.python_score, student.total_score, student.average, student.grade, student.rank
            ))
        print("=" * 96)

    def get_all_students_from_db(self):
        """DB에서 모든 학생 정보를 가져옴"""
        student_list = []
        try:
            sql = "SELECT * FROM students"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()

            for row in results:
                student = Student(row[0], row[1], row[2], row[3], row[4])
                student.total_score = row[5]
                student.average = row[6]
                student.grade = row[7]
                student.rank = row[8]
                student_list.append(student)
        except pymysql.MySQLError as e:
            print(f"DB에서 학생 정보 불러오기 오류: {e}")
        return student_list

    def add_student(self):
        student_id = input("학번: ")
        name = input("이름: ")
        english = self.get_correct_score("영어 점수 (0~100): ")
        c_language = self.get_correct_score("C-언어 점수 (0~100): ")
        python_score = self.get_correct_score("파이썬 점수 (0~100): ")

        new_student = Student(student_id, name, english, c_language, python_score)
        new_student.calculate_total_and_average()
        new_student.calculate_grade()

        self.insert_student_to_db(new_student)  # DB에 학생 정보 삽입
        self.students.append(new_student)

        print(f"{name} 학생 정보 추가 완료\n")

    def delete_student(self):
        student_id = input("삭제할 학생의 학번을 입력하세요: ")
        try:
            sql = "DELETE FROM students WHERE student_id = %s"
            self.cursor.execute(sql, (student_id,))
            if self.cursor.rowcount > 0:
                self.conn.commit()
                print(f"학번 {student_id} 학생 정보 삭제 완료")
                # self.students 리스트에서도 삭제 (선택 사항)
                self.students = [student for student in self.students if student.student_id != student_id]
            else:
                print("해당 학번의 학생을 찾을 수 없습니다.")
        except pymysql.MySQLError as e:
            print(f"DB 삭제 오류: {e}")

    def search_student(self):
        search_type = input("1: 학번 검색, 2: 이름 검색: ")
        search_term = input("검색어 입력: ")

        try:
            if search_type == "1":  # 학번 검색
                sql = "SELECT * FROM students WHERE student_id = %s"
            elif search_type == "2":  # 이름 검색
                sql = "SELECT * FROM students WHERE name = %s"
            else:
                print("잘못된 검색 유형입니다.")
                return

            self.cursor.execute(sql, (search_term,))
            result = self.cursor.fetchone()

            if result:
                student = Student(result[0], result[1], result[2], result[3], result[4])
                student.total_score = result[5]
                student.average = result[6]
                student.grade = result[7]
                student.rank = result[8]
                print(f"학생 정보: 학번: {student.student_id}, 이름: {student.name}, "
                      f"총점: {student.total_score}, 평균: {student.average:.2f}")
            else:
                print("해당 학생을 찾을 수 없습니다.")

        except pymysql.MySQLError as e:
            print(f"DB 검색 오류: {e}")

    def count_students_above_80(self):
        count = len([student for student in self.students if student.average >= 80])
        print(f"\n 평균 80점 이상인 학생은 {count}명입니다.")

    def display_menu(self):
        print("\n")
        if not self.initialized:
            print("0: 초기 설정 (5명 정보 입력)")
        print("1: 성적 출력")
        print("2: 학생 추가")
        print("3: 학생 삭제")
        print("4: 학생 검색")
        print("5: 총점 기준 정렬 및 출력")
        print("6: 평균 80점 이상 학생 수")
        print("7: 종료")


# Student 클래스
class Student:
    def __init__(self, student_id, name, english, c_language, python_score):
        self.student_id = student_id
        self.name = name
        self.english = english
        self.c_language = c_language
        self.python_score = python_score
        self.total_score = 0
        self.average = 0.0
        self.grade = ''
        self.rank = 0

    def calculate_total_and_average(self):
        self.total_score = self.english + self.c_language + self.python_score
        self.average = self.total_score / 3

    def calculate_grade(self):
        if self.average >= 95:
            self.grade = "A+"
        elif self.average >= 90:
            self.grade = "A"
        elif self.average >= 85:
            self.grade = "B+"
        elif self.average >= 80:
            self.grade = "B"
        elif self.average >= 75:
            self.grade = "C+"
        elif self.average >= 70:
            self.grade = "C"
        elif self.average >= 65:
            self.grade = "D+"
        elif self.average >= 60:
            self.grade = "D"
        else:
            self.grade = "F"


# 메인 함수
def main():
    manager = GradeManager()
    manager.connect_db()  # DB 연결
    manager.create_table()  # 테이블 생성

    try:
        while True:
            manager.display_menu()
            choice = input("메뉴를 선택하세요: ")

            match choice:
                case "0":
                    if not manager.initialized:
                        manager.first_Student_input()
                    else:
                        print("이미 초기 설정이 완료되었습니다.")

                case "1":  # 성적 출력
                    manager.print_students(ranking=False)
                case "2":  # 학생 추가
                    manager.add_student()
                case "3":  # 학생 삭제
                    manager.delete_student()
                case "4":  # 학생 검색
                    manager.search_student()
                case "5":  # 총점 기준 정렬 및 출력
                    manager.print_students(ranking=True)
                case "6":  # 평균 80점 이상 학생 수 출력
                    manager.count_students_above_80()
                case "7":
                    print("프로그램을 종료합니다.")
                    break
                case _:
                    print("잘못된 입력입니다. 다시 시도하세요.")
    finally:
        manager.disconnect_db()  # DB 연결 종료


if __name__ == "__main__":
    main()
