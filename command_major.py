
import requests

# Replace 'YOUR_API_KEY' with your actual UMD.io API key
api_key = 'YOUR_API_KEY'

def get_major(*args):
    
    if len(args) == 0:
        print("Invalid command. Try 'major {<major_name or major_id>} \n")
        return
    
    # Fetch the list of majors using the UMD.io API
    majors_url = f'https://api.umd.io/v1/majors/list?api_key={api_key}'
    majors_response = requests.get(majors_url)
    
    failed = False
    
    if majors_response.status_code != 200:
        print('Error occurred while fetching majors:', majors_response.status_code)
        return

    majors_list = majors_response.json()

    for major in args:
        # Search for the requested major in the majors list
        major_info = next((m for m in majors_list if m['name'].replace(" ", "").lower() == major.lower()), None)
        
        if major_info:
            # Print major details
            print(f"Major Information for major {major_info['major_id']}:", major_info['name'])
            print("College:", major_info['college'])
            print("URL:", major_info['url'])
            print("---")
        else:
            print(f"No information found for major: {major}")
            failed = True
            
    if failed:
        print("\nMake sure your requested majors are one word. Ex: 'major computerscience' NOT 'major computer science'")
        
