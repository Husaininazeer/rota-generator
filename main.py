from datetime import date
from csv import DictWriter


from src.page_splittings import surah_start_ayah
from src.ayah_data import ayah_count_for_each_surah
# gets the week number
week = date.today().isocalendar()[1]

# Finding what the start page will be
print("\n\n\n﷽ \n\n\n") 
print("Answer the following\nand press enter/return.\n")
start_page = int(input("What *page* did\nthe class finish\nin the last lesson? "))


# Finding the number of pages to cover
number_of_students = int(input("\nHow many students\nare reading?: ")) + 1
pages_per_student = int(input("\nHow many pages\nwill most students read?: "))
pages_to_cover = number_of_students * pages_per_student


page_increments = [i for i in range(0,pages_to_cover,pages_per_student)]

# adding the start surahs and ayahs to dictionary

student_id = 0
student_dict = {}
for page_increment in page_increments:
    start_index = surah_start_ayah[start_page + page_increment]
    student_dict[student_id] =  {
        # "start index":start_index,
        "starting_surah": start_index[0],
        "starting_ayah": start_index[1],
        "start": f"{start_index[0]}:{start_index[1]}"
    }
    student_id += 1

# the logic for the end ayahs and surahs
for student in student_dict:
    if student == number_of_students - 1:
        student_dict.pop(student)
        break
    next_student = student_dict[student + 1]
    current_student = student_dict[student]
    if current_student["starting_surah"] == next_student["starting_surah"]:
        current_student["ending_surah"] = current_student["starting_surah"]
        current_student["ending_ayah"] = next_student["starting_ayah"] - 1
    elif current_student["starting_surah"] != next_student["starting_surah"]:
        current_student["ending_surah"] = next_student["starting_surah"]
        current_student["ending_ayah"] = next_student["starting_ayah"] - 1
        if current_student["ending_ayah"] == 0:
            current_student["ending_surah"] = next_student["starting_surah"] - 1
            current_student["ending_ayah"] =  ayah_count_for_each_surah.get(current_student["ending_surah"]) #current_student["max_ayah_number_for_start_surah"]
    current_student["end"] = f"{current_student['ending_surah']}:{current_student['ending_ayah']}"

# converting to list from dict for writing (looping)
# from pprint import pprint
# pprint(student_dict)
for key in student_dict:
    student_dict[key].pop("starting_surah")
    student_dict[key].pop("starting_ayah")
    student_dict[key].pop("ending_ayah")
    student_dict[key].pop("ending_surah")
student_list_to_csv = [*student_dict.values()]
# pprint(student_list_to_csv)

# writing csv
with open(f'Rota for week {week}.csv', mode='w') as f:
    fieldnames = [
        'start',
        'end',
        # 'starting_surah',
        # 'starting_ayah', 
        # 'ending_surah', 
        # 'ending_ayah', 
        ]
    writer = DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for item in student_list_to_csv:
        writer.writerow(item)

# with open(f'Rota for week {week}.csv', mode='r') as f:
#   reader = reader(f, delimiter= ',')
#   for row in reader:
#     print(row)
