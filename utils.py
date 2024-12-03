# utils.py

import csv
from PIL import Image, ImageDraw
from io import BytesIO

# Function to draw bounding boxes on the image
def draw_bounding_boxes(image, predictions, original_width, original_height):
    draw = ImageDraw.Draw(image)
    
    for pred in predictions:
        # Get the bounding box for the 640x640 image
        x, y, width, height = pred.x, pred.y, pred.width, pred.height
        
        # Rescale the bounding box to the original image size
        x1 = int(x * original_width / 640)
        y1 = int(y * original_height / 640)
        x2 = int((x + width) * original_width / 640)
        y2 = int((y + height) * original_height / 640)
        
        # Draw the bounding box on the image
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
    
    return image

# Function to update prediction list based on prices
def update_predictions(prediction_list, prices):
    for prediction in prediction_list:
        # Iterate over the keys in prices and check if the classe is contained in any of the keys
        for price_item in prices:
            if prediction.classe.lower() in price_item.lower():
                # Update the price_ex_vat and price_inc_vat for the first matching classe
                prediction.price_ex_vat = prices[price_item]['price_ex_vat']
                prediction.price_inc_vat = prices[price_item]['price_inc_vat']
                break  # Break after the first match is found
    
    return prediction_list
# Function to calculate the total price from predictions
def calculate_total_price(predictions, prices):
    total_price = 0
    for pred in predictions:
        class_name = pred.classe
        
        # Look for a matching class name in the CSV prices
        matched_class = None        
        for csv_class in prices.keys():
            if class_name.lower() in csv_class.lower():  # Case-insensitive matching
                matched_class = csv_class
                break
        
        if matched_class:
            total_price += prices[matched_class]['price_ex_vat']
        else:
            print(f"Price for class '{class_name}' not found.")
    return total_price

import csv

# Load the prices from the CSV file into a dictionary
def load_prices(csv_file='./files/PRICES.csv'):
    prices = {}
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                class_name = row['ITEM']
                
                # Parse both 'PRICE EX VAT' and 'PRICE INC VAT'
                price_ex_vat = float(row['PRICE EX VAT'][2:])  # Remove currency symbol (assuming it's at the start)
                price_inc_vat = float(row['PRICE INC VAT'][2:])  # Remove currency symbol (assuming it's at the start)
                
                # Store both prices in a dictionary for each item
                prices[class_name] = {
                    'price_ex_vat': price_ex_vat,
                    'price_inc_vat': price_inc_vat
                }
                
        return prices
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return {}



# Function to preprocess the image
def preprocess(path):
    try:
        # Open the image using PIL
        image = Image.open(path)
        
        # Get original dimensions (width and height)
        original_width, original_height = image.size

        # Resize the image to 640x640
        image = image.resize((640, 640))  # Resize to 640x640

        # Save the resized image to the current path as 'image.jpg'
        image.save('image.jpg', format='JPEG')

        # Save the image back to a byte buffer for sending to the API
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        # Return the byte buffer and original dimensions
        return img_byte_arr, original_width, original_height

    except Exception as e:
        # Return None and the error message if processing fails
        return None, None, str(e)
    # Function to draw YOLO bounding boxes on the image
def draw_bounding_boxes_org(image, predictions, original_width, original_height):
    draw = ImageDraw.Draw(image)
    
    for pred in predictions:
        # Get the bounding box for YOLO format (center x, center y, width, height as ratios)
        x_center, y_center, width_ratio, height_ratio = pred.x, pred.y, pred.width, pred.height
        
        # Convert the YOLO relative coordinates to absolute pixel values
        box_width = int(width_ratio * original_width)
        box_height = int(height_ratio * original_height)
        x1 = int((x_center * original_width) - (box_width / 2))
        y1 = int((y_center * original_height) - (box_height / 2))
        x2 = x1 + box_width
        y2 = y1 + box_height
        
        # Draw the bounding box on the image
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
    
    return draw
