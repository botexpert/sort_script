#!/usr/bin/python3
'''Usage ./picture.py base_folder
prerequisites: You need to have 2 folders in base_folder. 
1st one named 'known_faces' that contains faces with name of people as filename
2nd one with pictures with different people that need to be sorted '''

import face_recognition
import os
import sys
import shutil
from os import path

def recognize(known_face_encoding,unknown_face_picture_path):
    '''Funkcija uporedjuje poznata i nepoznata lica i vraca niz boolean vrednosti za svako nepoznato lice 
    koje poznato lice je pronadjeno'''

    print("UKF PATH:{}".format(unknown_face_picture_path))
    
    unknown_face_picture = face_recognition.load_image_file(unknown_face_picture_path)
    unknown_face_encoding = face_recognition.face_encodings(unknown_face_picture)
    
    result = []
    res = None
    for encoding in unknown_face_encoding:
        result.append(face_recognition.compare_faces(known_face_encoding,encoding,tolerance=0.60))
    
    for x in result:
        try:
            res = x.index(True)
        except:
            continue    
    return res

def main(argv):
    base_dir = sys.argv[1]
    known_folder = path.join(base_dir,'known_faces')
    unknown_folder = path.join(base_dir,'to_sort')

    # known_folder = '/home/botexpert/Downloads/input'
    # unknown_folder = '/home/botexpert/Downloads/output'

    no_face_path = path.join(base_dir,'no_face') 
    if not os.path.exists(no_face_path):
        os.makedirs(no_face_path)
    
    newpath = path.join(base_dir,'unknown') 
    
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    dir_known_files = os.listdir(known_folder)
    dir_unknown_files = os.listdir(unknown_folder)
    
    known_faces = []
    known_map = dict()

    map_index=0
    for kf in dir_known_files:
        '''Dobijanje niza poznatih lica'''
        
        known_path = path.join(known_folder,kf)
        
        try:
            known_face_picture = face_recognition.load_image_file(known_path)
            known_faces.append(face_recognition.face_encodings(known_face_picture)[0])

            filename,extension = path.splitext(kf)
            known_map[map_index] = filename
            map_index += 1
            new_folder_for_sorted= path.join(base_dir,filename)
            if not os.path.exists(new_folder_for_sorted):     #kreira folder za svaku pozantu facu
                os.makedirs(new_folder_for_sorted)
        
        except(IndexError):
            shutil.move(known_path,no_face_path)
            continue


    for ukf in dir_unknown_files:
        unknown_path = path.join(unknown_folder,ukf)
        found_faces = recognize(known_faces,unknown_path)
        print(found_faces)   
        if found_faces != None:
            where = path.join (base_dir,known_map.get(found_faces))
            print(where)

            shutil.copy(unknown_path,where)
        else:
            shutil.copy(unknown_path,path.join(base_dir,'unknown'))

if __name__ == "__main__":
    main(sys.argv)
    print("DONE !!!!!!!!!!")
    pass