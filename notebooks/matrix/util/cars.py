import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.colors import hsv_to_rgb


def draw_car(length, height, car_type, h, s, v):
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.set_xlim(0, length)
    ax.set_ylim(0, height)
    ax.axis('off')
    
    car_color = hsv_to_rgb([h/360, s, v])
    
    # Base car body
    body = plt.Rectangle((length*0.1, height*0.4), length*0.8, height*0.3, color=car_color)
    ax.add_patch(body)
    
    # Wheels
    wheel_radius = height * 0.15
    front_wheel = plt.Circle((length*0.25, height*0.4), wheel_radius, color='black')
    rear_wheel = plt.Circle((length*0.75, height*0.4), wheel_radius, color='black')
    ax.add_patch(front_wheel)
    ax.add_patch(rear_wheel)
    
    if car_type.lower() == 'sedan':
        roof = plt.Rectangle((length*0.3, height*0.7), length*0.4, height*0.2, color=car_color)
        ax.add_patch(roof)
    elif car_type.lower() == 'truck':
        cab = plt.Rectangle((length*0.15, height*0.7), length*0.25, height*0.2, color=car_color)
        ax.add_patch(cab)
        bed = plt.Rectangle((length*0.45, height*0.7), length*0.45, height*0.1, color=car_color)
        ax.add_patch(bed)
    elif car_type.lower() == 'van':
        van_body = plt.Rectangle((length*0.1, height*0.4), length*0.8, height*0.5, color=car_color)
        ax.add_patch(van_body)
    
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)
    return image

def create_distance_matrix_with_cars(df, features):
    X = df[features]

    # Calculate distance matrix
    distances = pdist(X, metric='euclidean')
    distance_matrix = squareform(distances)

    
    # Create figure and axes
    n = len(df)
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Draw the distance matrix
    im = ax.imshow(distance_matrix, cmap='afmhot')

    # Add colorbar
    plt.colorbar(im)
    
    # Draw car images
    for i in range(n):
        car = df.iloc[i]
        car_image = draw_car(car['length'], car['height'], car['type'], car['h'], car['s'], car['v'])
        
        im = OffsetImage(car_image, zoom=0.0002*car['length'])  # Adjust zoom as needed
        ab = AnnotationBbox(im, (-0.5, i), xycoords='data', frameon=False)
        ax.add_artist(ab)
        ab = AnnotationBbox(im, (i, -0.5), xycoords='data', frameon=False)
        ax.add_artist(ab)

    ax.axis('off')
    plt.tight_layout()
    plt.show()
