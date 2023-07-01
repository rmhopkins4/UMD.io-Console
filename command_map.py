import requests
import matplotlib.pyplot as plt
import mplcursors

def plot_building_locations(*args):
        
    
    # Fetch building data from UMD.io API
    buildings_url = 'https://api.umd.io/v1/map/buildings'
    response = requests.get(buildings_url)
    buildings = response.json()

    # Filter out latitude values over 40 and longitude values under -80
    filtered_buildings = [building for building in buildings if building['lat'] <= 40 and building['long'] >= -80]

    # Determine the boundaries of the map
    min_latitude = min(building['lat'] for building in filtered_buildings)
    max_latitude = max(building['lat'] for building in filtered_buildings)
    min_longitude = min(building['long'] for building in filtered_buildings)
    max_longitude = max(building['long'] for building in filtered_buildings)

    # Create empty lists to store latitude and longitude data
    latitude_data = []
    longitude_data = []
    labels = []

    # Extract latitude, longitude, and building names
    for building in filtered_buildings:
        latitude_data.append(building['lat'])
        longitude_data.append(building['long'])
        labels.append(building['name'])

    # Plot the buildings on a scatter plot
    scatter = plt.scatter(longitude_data, latitude_data, marker='.', color='red')

    # Set the x and y axis limits based on the map boundaries
    plt.xlim(min_longitude, max_longitude)
    plt.ylim(min_latitude, max_latitude)

    # Set aspect ratio to 'equal' for 1:1 scale
    plt.gca().set_aspect('equal')

    # Set labels and title for the plot
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Building Locations')

    # Create a cursor object
    cursor = mplcursors.cursor(hover=True)

    # Add annotations to the plotted points
    @cursor.connect("add")
    def on_add(sel):
        index = sel.target.index
        label = labels[index]
        sel.annotation.set_text(label)

    # Display the plot
    plt.show()
