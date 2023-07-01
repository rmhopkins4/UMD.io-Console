import requests


def get_average_gpa(course_id):
    url = f'https://planetterp.com/api/v1/grades?course={course_id}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        total_grades = 0
        total_students = 0

        for semester_data in data:
            grades = semester_data.copy()
            grades.pop('course', None)
            grades.pop('professor', None)
            grades.pop('semester', None)
            grades.pop('section', None)
            grades.pop('Other', None)

            grade_mapping = {
                "A+": 4.0,
                "A": 4.0,
                "A-": 3.7,
                "B+": 3.3,
                "B": 3.0,
                "B-": 2.7,
                "C+": 2.3,
                "C": 2.0,
                "C-": 1.7,
                "D+": 1.3,
                "D": 1.0,
                "D-": 0.7,
                "F": 0.0,
                "W": 0.0,
            }

            for grade, count in grades.items():
                gpa = grade_mapping.get(grade)
                if gpa is not None:
                    total_grades += count * gpa
                    total_students += count

        if total_students > 0:
            average_gpa = total_grades / total_students
            return(f"Average GPA for {course_id}: {average_gpa:.2f}")
        else:
            return(f"No average GPA data available for {course_id}")
    else:
        return(f"Error occurred while fetching average GPA for {course_id}: {response.status_code}")


def get_course_info(*args):
    
    if len(args) == 0:
        print("Invalid command. Try: 'courseinfo <course_id> \n")
        return
    
    # Extract the course code from the arguments
    for course_code in args:
    
        # Fetch the list of semesters using the UMD.io API
        semesters_url = f'https://api.umd.io/v1/courses/semesters'
        semesters_response = requests.get(semesters_url)

        if semesters_response.status_code != 200:
            print('Error occurred while fetching semesters:', semesters_response.status_code)
            return

        semesters = semesters_response.json()

        # Iterate through the semesters in reverse order
        for semester in reversed(semesters):
            semester_code = semester

            # Construct the URL with the appropriate endpoint, course code, semester code, and API key
            url = f'https://api.umd.io/v1/courses/{course_code}?semester={semester_code}'

            # Send the GET request
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract the course information from the response
                course_info = response.json()[0]

                # Print course details
                print(f"Course Information for {course_info['course_id']}:", course_info['name'])
                print("Department:", course_info['department'])
                print("Credits:", course_info['credits'])
                print("Description:", course_info['description'])

                prerequisites = course_info['relationships']['prereqs']
                print("Prerequisites:", prerequisites if prerequisites else 'None')

                gen_ed = course_info['gen_ed']
                print("General Education Requirements:", ", ".join(gen_ed[0]) if gen_ed else 'None')

                credit_granted_for = course_info['relationships']['credit_granted_for']
                print("Credit Granted For:", credit_granted_for if credit_granted_for else 'None')

                # Retrieve the average GPA for the course
                print(get_average_gpa(course_info['course_id']))

                print("Found in Semester:", convert_semester_code(semester))
                print("---")

                break


def convert_semester_code(semester_code):
    semester_code = str(semester_code)
    # Define the mapping of semester codes to names
    semester_mapping = {
        '01': 'Spring',
        '05': 'Summer',
        '08': 'Fall',
        '12': 'Winter'
    }

    # Extract the year and code from the semester code
    year = semester_code[:4]
    code = semester_code[4:6]

    # Check if the code exists in the mapping
    if code in semester_mapping:
        # Get the corresponding semester name
        semester_name = semester_mapping[code]

        # Combine the semester name and year
        semester_year = f"{semester_name} {year}"

        return semester_year

    # If the code is not recognized, return the original semester code
    return semester_code
