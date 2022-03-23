import sys
import requests
import os
import argparse
import _thread
import time
import subprocess
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

print("==============> Welcome today's demo (03/18/2022) <===================")

correct_map = {
'test_00' : 'Paul',
'test_01' : 'Emily',
'test_02' : 'Bob',
'test_03' : 'German',
'test_04' : 'Emily',
'test_05' : 'Gerry',
'test_06' : 'Gerry',
'test_07' : 'Ranil',
'test_08' : 'Bill',
'test_09' : 'Wang',
'test_10' : 'Paul',
'test_11' : 'Emily',
'test_12' : 'Bob',
'test_13' : 'German',
'test_14' : 'Emily',
'test_15' : 'Gerry',
'test_16' : 'Gerry',
'test_17' : 'Ranil',
'test_18' : 'Bill',
'test_19' : 'Wang',
'test_20' : 'Paul',
'test_21' : 'Emily',
'test_22' : 'Bob',
'test_23' : 'German',
'test_24' : 'Emily',
'test_25' : 'Gerry',
'test_26' : 'Gerry',
'test_27' : 'Ranil',
'test_28' : 'Bill',
'test_29' : 'Wang',
'test_30' : 'Paul',
'test_31' : 'Emily',
'test_32' : 'Bob',
'test_33' : 'German',
'test_34' : 'Emily',
'test_35' : 'Gerry',
'test_36' : 'Gerry',
'test_37' : 'Ranil',
'test_38' : 'Bill',
'test_39' : 'Wang',
'test_40' : 'Paul',
'test_41' : 'Emily',
'test_42' : 'Bob',
'test_43' : 'German',
'test_44' : 'Emily',
'test_45' : 'Gerry',
'test_46' : 'Gerry',
'test_47' : 'Ranil',
'test_48' : 'Bill',
'test_49' : 'Wang',
'test_50' : 'Paul',
'test_51' : 'Emily',
'test_52' : 'Bob',
'test_53' : 'German',
'test_54' : 'Emily',
'test_55' : 'Gerry',
'test_56' : 'Gerry',
'test_57' : 'Ranil',
'test_58' : 'Bill',
'test_59' : 'Wang',
'test_60' : 'Paul',
'test_61' : 'Emily',
'test_62' : 'Bob',
'test_63' : 'German',
'test_64' : 'Emily',
'test_65' : 'Gerry',
'test_66' : 'Gerry',
'test_67' : 'Ranil',
'test_68' : 'Bill',
'test_69' : 'Wang',
'test_70' : 'Paul',
'test_71' : 'Emily',
'test_72' : 'Bob',
'test_73' : 'German',
'test_74' : 'Emily',
'test_75' : 'Gerry',
'test_76' : 'Gerry',
'test_77' : 'Ranil',
'test_78' : 'Bill',
'test_79' : 'Wang',
'test_80' : 'Paul',
'test_81' : 'Emily',
'test_82' : 'Bob',
'test_83' : 'German',
'test_84' : 'Emily',
'test_85' : 'Gerry',
'test_86' : 'Gerry',
'test_87' : 'Ranil',
'test_88' : 'Bill',
'test_89' : 'Wang',
'test_90' : 'Paul',
'test_91' : 'Emily',
'test_92' : 'Bob',
'test_93' : 'German',
'test_94' : 'Emily',
'test_95' : 'Gerry',
'test_96' : 'Gerry',
'test_97' : 'Ranil',
'test_98' : 'Bill',
'test_99' : 'Wang',
}


parser = argparse.ArgumentParser(description='Upload images')
parser.add_argument('--num_request', type=int, help='one image per request')
parser.add_argument('--url', type=str, help='URL to the backend server, e.g. http://3.86.108.221/xxxx.php')
parser.add_argument('--image_folder', type=str, help='the path of the folder where images are saved on your local machine')
args = parser.parse_args()
url = args.url

# These are global variables
correct_count = 0
received_count = 0
wrong_dict = {}


def send_one_request(image_path):
    # To check the correctness of the result, it will modify the following variables
    global correct_count, received_count, wrong_dict

    # Define http payload, "myfile" is the key of the http payload
    file = {"myfile": open(image_path,'rb')} 
    r = requests.post(url, files=file)

    if r.status_code != 200:
        print('sendErr: '+r.url)
    else:
        # The document requirement says that:
        # For example, the user uploads an image named “test_00.jpg”.
        # For the above request, the output should be “Paul” in plain text. 
        # So image_path shoud be "XXX/test_00.jpg", and r.text shoud be "Paul"
        image_name = image_path.strip().split("/")[-1] # "test_00.jpg"
        image_name_key = image_name.replace('.jpg', '') # "test_00"
        output = r.text # "Paul"
        output = output.strip()
        print(f"\n{image_name} uploaded!")
        print(f"\nClassification result: {output}")

        correct_result = (correct_map[image_name_key])
        if correct_result == output:
            correct_count += 1
        else:
            wrong_dict[image_name] = output
        received_count += 1
        

start_time = time.time()

num_request = args.num_request
image_folder = args.image_folder
num_max_workers = 100
image_path_list = []
for i, name in enumerate(os.listdir(image_folder)):
    if i == num_request:
        break
    image_path_list.append(image_folder + name)

with ThreadPoolExecutor(max_workers = num_max_workers) as executor:
    executor.map(send_one_request, image_path_list)


while 1:
   print(".")
   time.sleep(1)
   
   end_time = (time.time()-start_time)
   if received_count == num_request or end_time > 900:
       print(f"Total time: {end_time}s")
       
       if correct_count == num_request:
           print(f"{num_request} requests are sent. {correct_count} responses are correct.")
       else:
           print(f"{num_request} requests are sent. {correct_count} responses are correct.")
           print(f"Following results are wrong:")
           for k, v in wrong_dict.items():
               print(f"{k}: {v}")
       break

