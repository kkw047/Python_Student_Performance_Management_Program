##################

# 프로그램명: Student Performance Management Program

# 작성자: 소프트웨어학부 / 김건우

# 작성일: 4/11

# 프로그램 설명: 학생 성적정보 프로그램이다.
#              키보드로부터 학번, 이름, 영어점수, C-언어 점수, 파이썬 점수를 입력받아 총점, 평균, 학점, 등수를  계산하는 프로그램
#              값은 범위 내에서만 입력

###################
class GradeManager:
    # 학생 관리 클래스
    # 학생 데이터 관리 및 계산

    # __init__ 메소드/ 생성자
    def __init__(self):
        self.students = []  # Student 객체 리스트
        self.initialized = False  # 초기 설정이 완료되었는지 확인하는 변수

    # 메뉴 출략 메서드
    def display_menu(self):
        print("\n") # 가독성 띄위기
        if not self.initialized:  # 초기 설정 메뉴를 한 번만 표시
            print("0: 초기 설정 (5명 정보 입력)")
        print("1: 성적 출력")
        print("2: 학생 추가")
        print("3: 학생 삭제")
        print("4: 학생 검색")
        print("5: 총점 기준 정렬 및 출력")
        print("6: 평균 80점 이상 학생 수")
        print("7: 종료")

    # 입력받은 값 검사  필수 함수는 아니지만 필요함을 느껴 추가
    def get_correct_score(self, prompt):
        while True:
            # 사용자 입력 받기
            score = input(prompt).strip()

            # 빈 값 검사
            if not score:
                print("입력 오류: 점수는 빈 값일 수 없습니다. 다시 입력하세요.")
                continue

            # 정수 변환 및 범위 검사
            if score.isdigit():
                score = int(score)
                if 0 <= score <= 100:
                    return score  # 올바른 값 반환
                else:
                    print("입력 오류: 점수는 0과 100 사이여야 합니다.")
            else:
                print("입력 오류: 숫자 형식이 아닙니다. 올바른 숫자를 입력하세요.")


    # 초기 학생 입력 메소드 5명을 입력받음 입력함수 부분
    def first_Student_input(self):
        self.students.clear()
        self.initialized = True  # 초기 설정 완료

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
            self.students.append(new_student)
        print("\n초기 학생 입력 완료")

    # 등수 계산 함수
    def rank_students(self):
        sorted_students = sorted(self.students, key=lambda x: x.total_score, reverse=True)
        for rank, student in enumerate(sorted_students, start=1):
            student.rank = rank  # 정렬된 순서를 기준으로 등수 설정
        return sorted_students  # 정렬된 리스트 반환

    # 성적 출력 함수
    def print_students(self, ranking = False):
        if not self.students:
            print("\n출력할 학생 데이터가 없습니다.\n")
            return

        self.rank_students()# 등수계산

        # 1과 5의 차별점을 두기 위한 구분 함수
        if ranking:
            sorted_students = self.rank_students()  # 정렬된 리스트 가져오기
            title = "성적관리 프로그램 (총점 기준 정렬 출력)"
        else:
            sorted_students = self.students  # 입력 순서대로 출력
            title = "성적관리 프로그램 (기본 출력)"

        # 제목 출력
        print(f"\n\n{title:^96}")
        print("=" * 96)
        print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<12}{:<10}{:<10}".format(
            "학번", "이름", "영어", "C-언어", "파이썬", "총점", "평균", "학점", "등수"
        ))
        print("=" * 96)

        # 학생 루프 출력
        for student in sorted_students:
            print("{:<11}{:<11}{:<11}{:<11}{:<11}{:<11}{:<14.2f}{:<11}{:<11}".format(
                student.student_id, student.name, student.english, student.c_language,
                student.python_score, student.total_score, student.average, student.grade, student.rank
            ))
        # 하단 구분선
        print("=" * 96)

    # 삽입함수 (학생 추가 역학)
    def add_student(self):
        student_id = input("학번: ")
        name = input("이름: ")
        english = self.get_correct_score("영어 점수 (0~100): ")
        c_language = self.get_correct_score("C-언어 점수 (0~100): ")
        python_score = self.get_correct_score("파이썬 점수 (0~100): ")

        new_student = Student(student_id, name, english, c_language, python_score)
        new_student.calculate_total_and_average()
        new_student.calculate_grade()

        self.students.append(new_student)
        print(f"{name} 학생 정보 추가 완료\n")

    # 삭제 함수
    def delete_student(self):
        student_id = input("삭제할 학생의 학번을 입력하세요: ")
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                print(f"\n {student.name} 학생 삭제 완료 \n")
                return
        print("\n해당 학번의 학생을 찾을 수 없습니다.\n")

    # 탐색 함수 ( 학번, 이름)
    def search_student(self):
        search_type = input("1: 학번 검색, 2: 이름 검색: ")
        if search_type == "1":
            student_id = input("검색할 학번 입력: ")
            for student in self.students:
                if student.student_id == student_id:
                    print(f"학생 정보: 학번: {student.student_id}, 이름: {student.name}, "
                          f"총점: {student.total_score}, 평균: {student.average:.2f}")
                    return
        elif search_type == "2":
            name = input("검색할 이름 입력: ")
            for student in self.students:
                if student.name == name:
                    print(f"학생 정보: 학번: {student.student_id}, 이름: {student.name}, "
                          f"총점: {student.total_score}, 평균: {student.average:.2f}")
                    return
        print("\n해당 학생을 찾을 수 없습니다.")

    # 80점 이상인 학생
    def count_students_above_80(self):
        count = len([student for student in self.students if student.average >= 80])
        print(f"\n 평균 80점 이상인 학생은 {count}명입니다.")


# Student 클래스
# 학생의 상태 관리
class Student:
    # 기본 생성자
    def __init__(self, student_id, name, english, c_language, python_score):
        self.student_id = student_id
        self.name = name
        self.english = english
        self.c_language = c_language
        self.python_score = python_score

        # 각종 계산 결과
        self.total_score = 0
        self.average = 0.0
        self.grade = ''
        self.rank = 0

    # 총점 및 평균 계산
    def calculate_total_and_average(self):
        self.total_score = self.english + self.c_language + self.python_score
        self.average = self.total_score / 3

    # 학점 계산
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
    while True:
        manager.display_menu()  # 메뉴 출력
        choice = input("메뉴를 선택하세요: ")

        match choice:
            case "0":
                if not manager.initialized:  # 초기 설정이 완료되지 않았을 경우에만 실행
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

            case "7":  # 종료
                print("프로그램을 종료합니다.")
                break

            case _:  # 잘못된 입력 처리
                print("잘못된 입력입니다. 다시 시도하세요.")


if __name__ == "__main__":
    main()  # 프로그램 실행
