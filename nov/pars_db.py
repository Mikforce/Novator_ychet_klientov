import os

import django



os.environ["DJANGO_SETTINGS_MODULE"] = 'nov.settings'
django.setup()


import xml.etree.ElementTree as ET
from datetime import datetime
from django.utils import timezone
from myapp.models import Client, Group, Coach
import random
import string

# # это парсинг для клиентов
#
# def generate_random_card_number():
#     # Генерируем случайное число из 6 цифр
#     return ''.join(random.choices(string.digits, k=6))
#
#
# # Parse the XML file
# tree = ET.parse('_DB/Client.xml')
# client = tree.getroot()
# group_obj = Group.objects.get(id=8)
#
# # Iterate over each 'Item' element in the XML
# for item in client.findall('Item'):
#     last_name_elem = item.find('LastName')
#     name_elem = item.find('Name')
#     middle_name_elem = item.find('MiddleName')
#
#     full_name = ' '.join(part.text for part in [last_name_elem, name_elem, middle_name_elem] if part is not None)
#
#     birth_date_elem = item.find('BirthDate')
#     birth_date_str = birth_date_elem.text if birth_date_elem is not None else None
#     if birth_date_str:
#         try:
#             birth_date = datetime.strptime(birth_date_str, '%d.%m.%Y').date()
#         except ValueError:
#             birth_date = timezone.now().date()  # set default date if format is incorrect
#     else:
#         birth_date = timezone.now().date()
#
#     phone_number_elem = item.find('ParentMobilePhone1')
#     phone_number = phone_number_elem.text if phone_number_elem is not None else None
#
#
#     last_name_elem1 = item.find('ParentLastName')
#     name_elem1 = item.find('ParentName')
#     middle_name_elem1 = item.find('ParentMiddleName')
#
#
#
#     parent_name = ' '.join(part.text for part in [last_name_elem1, name_elem1, middle_name_elem1] if part is not None)
#     address_elem = item.find('ResidenceAddress')
#     address = address_elem.text if address_elem is not None else 'No Address'
#
#     barcode_elem = item.find('Barcode')
#     card_number = barcode_elem.text if barcode_elem is not None else None
#
#     # Check if client with the same card_number already exists
#     # Handle the case when card number element is not found
#     if card_number:
#         # Check if client with the same card_number already exists
#         if Client.objects.filter(card_number=card_number).exists():
#             card_number = generate_random_card_number()
#     else:
#         # Generate a random card number when barcode is missing
#         card_number = generate_random_card_number()
#
#
#     # Create a Client instance
#     new_client = Client(
#         full_name=full_name,
#         birth_date=birth_date,
#         phone_number=phone_number or 'No Phone Number',
#         parent_name=parent_name or 'No Parent Name',
#         address=address,
#         card_number=card_number or 'No Card Number',
#         date_joined=timezone.now().date(),
#         group_obj=group_obj
#     )
#     new_client.save()





# # парсинг для учителей
#
# tree = ET.parse('_DB/Teacher.xml')
# teachers = tree.getroot()
#
# for item in teachers.findall('Item'):
#     # Extract data from XML with error handling
#     last_name = item.find('LastName')
#     name = item.find('Name')
#     middle_name = item.find('MiddleName')
#
#     if last_name is not None and name is not None and middle_name is not None:
#         full_name = f"{last_name.text} {name.text} {middle_name.text}"
#     else:
#         # Handle the case where one of the elements is missing
#         full_name = "Unknown Name"
#     mobile_phone_element = item.find('MobilePhone1')
#     phone_number = mobile_phone_element.text if mobile_phone_element is not None else "Unknown Phone Number"
#     percent = float(item.find('.//VisitPercent').text) if item.find('.//VisitPercent') is not None else 0
#
#     # Creating Coach object
#     coach = Coach(full_name=full_name, phone_number=phone_number, percent=percent)
#     coach.save()
#
#     # Add students (clients) and groups to the coach
#     for client_id in item.findall('.//ID_Client'):
#         client = Client.objects.get(id=client_id.text)
#         coach.students.add(client)
#
#     for group_id in item.findall('.//ID_Group'):
#         group = Group.objects.get(id=group_id.text)
#         coach.groupqs.add(group)
#
#     coach.save()







# парсинг для групп

import xml.etree.ElementTree as ET

# Parse the Style.xml file
style_tree = ET.parse('_DB/Style.xml')
style_root = style_tree.getroot()

# Parse the Group.xml file
group_tree = ET.parse('_DB/Group.xml')
group_root = group_tree.getroot()

# Create a dictionary to store the merged data
merged_data = {}

# Extract data from Style.xml
for style_item in style_root.findall('.//Item'):
    style_id = style_item.find('ID').text
    style_name = style_item.find('Name').text
    merged_data[style_id] = {'Name': style_name}

# Merge data from Group.xml
for group_item in group_root.findall('.//Item'):
    id_style_element = group_item.find('ID_Style')

    if id_style_element is not None:
        id_style = id_style_element.text
        if id_style in merged_data:
            age_element = group_item.find('Age')
            if age_element is not None:
                merged_data[id_style]['Age'] = age_element.text
            else:
                merged_data[id_style]['Age'] = "N/A"

            place_count_element = group_item.find('PlaceCount')
            if place_count_element is not None:
                merged_data[id_style]['PlaceCount'] = place_count_element.text
            else:
                merged_data[id_style]['PlaceCount'] = "N/A"

            # Extract schedule information
            schedule_element = group_item.find('Schedule')
            if schedule_element is not None:
                schedule_data = {}
                for schedule_item in schedule_element.findall('.//Item'):
                    day = schedule_item.find('Day').text
                    time_from = schedule_item.find('.//From').text
                    time_to = schedule_item.find('.//To').text

                    schedule_data[day] = {'Time': f"{time_from} - {time_to}"}

                merged_data[id_style]['Schedule'] = schedule_data

# Printing the merged data
for key, value in merged_data.items():
    print(f"Style ID: {key}")
    for field, val in value.items():
        if field == 'Schedule':
            print("Schedule:")
            for day, times in val.items():
                print(f"  {day}: {times['Time']}")
        else:
            print(f"{field}: {val}")
    print("------------------------")