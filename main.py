import serial
import pygame
import sys
import time
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

# Serial port configuration
SERIAL_PORT = '/dev/ttyUSB0'  # Update this to your Arduino's serial port
BAUD_RATE = 9600

# Image paths
IMAGE_PATHS = {
    '1': ['faculty_images/About Course.png'],
    '2': ['faculty_images/course1.png', 'faculty_images/course2.png', 'faculty_images/course3.png'],
    '3': ['faculty_images/faculty1.png', 'faculty_images/faculty2.png', 'faculty_images/faculty3.png'],
    '4': ['faculty_images/facility1.png', 'faculty_images/facility2.png', 'faculty_images/facility3.png'],
    '5': ['faculty_images/placement.png'],
    '6': ['faculty_images/other_information.png'],
    'front_page': ['faculty_images/Front.png']
}

# Initialize pygame
pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
pygame.display.set_caption('Image Viewer')

def speak_name():
    pygame.mixer.init()
    pygame.mixer.music.load("JSS_Male.mp3")
    pygame.mixer.music.play()

def load_image(image_path):
    """
    Load an image and scale it to fullscreen.
    """
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (infoObject.current_w, infoObject.current_h))
    return image

def display_image(image_path):
    """
    Display an image on the screen.
    """
    image = load_image(image_path)
    screen.blit(image, (0, 0))
    pygame.display.flip()

def main():
    
    # Display the front page initially
    display_image(IMAGE_PATHS['front_page'][0])

    # Dictionary to keep track of the currently displayed image index for buttons 2, 3, and 4
    current_image_indices = {'2': -1, '3': -1, '4': -1}

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        # Display the front page when ESC is pressed
                        display_image(IMAGE_PATHS['front_page'][0])
            
            # time.sleep(2)  # Wait for the connection to establish
            if ser.in_waiting > 0:
                line = ser.read().decode('utf-8').strip()
                print(f"Received: {line}")
                if line == '9':
                    speak_name()
                elif line == '0':
                    print("Motion stopped. Python script acknowledges.")
                elif line == '1':
                    display_image(IMAGE_PATHS['1'][0])
                elif line == '5':
                    display_image(IMAGE_PATHS['5'][0])
                elif line == '6':
                    display_image(IMAGE_PATHS['6'][0])
                elif line in IMAGE_PATHS:
                    if isinstance(IMAGE_PATHS[line], list):
                        # Multiple images
                        button = line
                        current_image_indices[button] = (current_image_indices[button] + 1) % len(IMAGE_PATHS[button])
                        display_image(IMAGE_PATHS[button][current_image_indices[button]])
                else:
                    # Display the front page when button 7 is pressed
                    display_image(IMAGE_PATHS['front_page'][0])

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    finally:
        pygame.quit()
        if 'ser' in locals():  # Check if 'ser' is defined before attempting to close
            ser.close()
        sys.exit()

if __name__ == "__main__":
    main()
