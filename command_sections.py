import requests

api_key = 'YOUR_API_KEY'

def get_course_sections(*args):
    
    if len(args) == 0:
        print("Invalid command. Try: 'sections <course_id> [<semester>]' \n")
        return
    
    # Extract the course code and semester code from the arguments
    course_code = args[0]
    semester_code = args[1] if len(args) > 1 else None

    # Construct the base URL with the appropriate endpoint and parameters
    url = f'https://api.umd.io/v1/courses/{course_code}/sections?api_key={api_key}'

    # If semester_code is provided, add it to the URL as a query parameter
    if semester_code:
        url += f'&semester={semester_code}'

    # Send the GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the section information from the response
        sections = response.json()

        # Print section details
        if sections:
            print(f"Sections for {course_code}{' in ' + semester_code if semester_code else ''}:")
            for section in sections:
                print('Section:', section['section_id'])
                print('Instructors:', ", ".join(section['instructors']) if section['instructors'] else 'TBD')
                print('Meeting Times:')
                for meeting in section['meetings']:
                    print('  Days:', meeting['days'])
                    print('  Room:', meeting['building'], meeting['room'])
                    print('  Start Time:', meeting['start_time'])
                    print('  End Time:', meeting['end_time'])
                    print('---')
        else:
            print("No sections found for the specified course and semester.")

    else:
        print('Error occurred:', response.status_code)
