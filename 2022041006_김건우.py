#5명의 학생의 세개의 교과목 (영어, C-언어, 파이썬)에 대하여  키보드로부터 입력받아 총점, 평균, 학점, 등수를 계산하는 프로그램 작성
# 함수를 입력, 총점 과 평균, 학점, 등수, 메인  5개로 진행
# 점수가 0~100 까지 검수하는 과정 추가
# isdihit을 이용하면 문자까지 분류 가능한것을 알아 추가
#입력 함수, 총점/평균 계산 함수,  학점계산 함수, 등수계산 함수, 출력 함수로 나누어 구현
#입력 형식 학번: 이름: 영어 : C-언어: 파이썬:

def correct_check(score,subject_name): # 값을 받을때까지 무한반복 #제시 함수에서는 없었지만 필요할것 같아 유지
    while True:
        if score.isdigit():
            score = int(score)  # 정수로 변환
            if 0 <= score <= 100:  # 점수가 0~100 사이인지 확인
                return score  # 끝
            else:
                print("0~100의 숫자를 입력해주세요.")
        else:
            print("올바른 숫자를 입력해주세요.")
        score = input(subject_name + "의 점수를 다시 입력하세요: ")


def student_info(): # 입력 함수  기존 점수 입력 함수를 학생 정보 함수로 변경
    Hakbun = input("학번 : ")
    name = input("이름 : ")
    E_score = correct_check(input("영어 : "),"영어")
    C_score = correct_check(input("C-언어 : "),"C-언어")
    P_score = correct_check(input("파이썬 : "),"파이썬")
    return  [Hakbun,name,E_score,C_score,P_score] #리스트로 반환

def total_average(Students): #총점 및 평점 계산함수
    totals = []
    averages = []
    for i in Students:
        total = i[2]+ i[3]+ i[4]
        average = total/3
        totals.append(total)
        averages.append(average)

    return totals,averages


def grade(average): # 학점 계간 함수
    if (average >= 95):
        return "A+"
    elif (average >= 90):
        return "A"
    elif average >= 85:
        return "B+"
    elif average >= 80:
        return "B"
    elif average >= 75:
        return "C+"
    elif average >= 70:
        return "C"
    elif average >= 65:
        return "D+"
    elif average >= 60:
        return "D"
    else:
        return "F"

def rank(totals): #등수 계산 함수 #겹치는거를 생각하면 1에서 천천히 들어나는식으로
    ranks = [1]*len(totals)
    for i in  range(len(totals)):
        for j in range(len(totals)):
            if totals[j] > totals[i]:
                ranks[i] += 1
    return ranks

def result_print(Students, totals, averages, grades, ranks): #출력함수 # C언어에서 쓰던 %포멧팅을 사용려 했지만 정렬이 힘들어 변경 str.format()이용
    print("\n\n{:^96}".format("성적관리 프로그램"))  # 오른쪽 정렬로 제목 출력 (C++의 setw와 유사)
    print("=" * 96)
    print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<12}{:<10}{:<10}".format(  "학번", "이름", "영어", "C-언어", "파이썬", "총점", "평균", "학점", "등수"   ))
    print("=" * 96)
    for i in range(len(Students)):
        student = Students[i]
        print("{:<11}{:<11}{:<11}{:<11}{:<11}{:<11}{:<14.2f}{:<11}{:<11}".format(student[0], student[1], student[2], student[3], student[4], totals[i], averages[i], grades[i], ranks[i]))
print("=" * 96)


def main() :
    Student_number = 5
    Students = []

    for i in range(Student_number):#입력되어아 하는 값이 많으니 리스트에 저장
        Students.append(student_info()) # return 값은 입력받는 학번, 이름 영어점수, C 점수 ,파이썬 점수 # [[학번,이름...],[학번,이름...],[],[],] 로 저장
        print("=============================================") # 구별이 힘들어 구별선

    totals,averages = total_average(Students) # [학생1,학생2,..]
    grades = [grade(avg) for avg in averages]# ["학생1 성적","학생2 성적","학생3 성적"...]
    ranks = rank(totals) #grades와 동일

    result_print(Students,totals,averages,grades,ranks)

   
        # 메인 함수 호출
main()
