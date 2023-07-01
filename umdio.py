import requests
from command_sections import get_course_sections
from command_courseinfo import get_course_info
from command_commands import get_commands
from command_major import get_major
from command_map import plot_building_locations
from command_schedule import get_schedule_commands

intro = r"""
Welcome to...
                __  _                           
 __ ____ _  ___/ / (_)__                        
/ // /  ' \/ _  / / / _ \                       
\_,_/_/_/_/\_,_(_)_/\___/                     by            
             __             __    _         ____
  ______ _  / /  ___  ___  / /__ (_)__  ___/ / /
 / __/  ' \/ _ \/ _ \/ _ \/  '_// / _ \(_-<_  _/
/_/ /_/_/_/_//_/\___/ .__/_/\_\/_/_//_/___//_/  
                   /_/                          
"""

outro = r"""        
   |          
   |          
   + \        
   \\.G_.*=.  
    `(H'/.\|  
     .>' (_--.
  _=/d   ,^\  
 ~~ \)-'   '  
    / |       
   '  '   rmh4     
"""

# Create a dictionary that maps commands to their corresponding functions
command_map = {
    'sections': get_course_sections,
    'courseinfo': get_course_info,
    'major': get_major,
    'map': plot_building_locations,
    'schedule': get_schedule_commands,
    'commands': get_commands,
}

print(intro)

# Main program loop
while True:
    # Prompt the user for input
    user_input = input('Enter command: ')

    # Split the input into tokens
    tokens = user_input.split()

    # Check if the input is valid and has at least one token
    if len(tokens) < 1:
        print('Please enter a command.')
        continue

    command = tokens[0]

    # Check if the command is in the command_map
    if command in command_map:
        # Get the corresponding function from the command_map
        command_function = command_map[command]
        # Call the function with the remaining tokens as arguments
        command_function(*tokens[1:])
    elif command == 'end':
        print("Terminating program.", outro)
        break
    else:
        print('Invalid command. \n')
