from sys import argv
import subprocess as sp
import hashlib
import filecmp
import os
import time
import datetime
import glob

def gen_image_hash(image_path):

    with open(image_path, "rb") as file:
        data = file.read()
        md5_hash = hashlib.md5(data).hexdigest()

    return md5_hash


def main():

    reference_input_images_hash = ["31f59c26374e3880b11988a2519b8139",
                                   "a6c85ca8cde857524249b061dd68f319",
                                   "f509e9a66b4bb82d5830c52dca128be1",
                                   "cd69ea435e2314f7773b281e62a6c46d",                    
                                   "ea2c8074064e2381798eba192ffe07fb",
                                   "54252cfb0eac45bd2f523fc978ea8d71",
                                   "68d679d6f6ac71d8e57e6180ee12f2a6",
                                   "1c8adcb4a34105f80b54dcba1cdb12a5"]

    reference_output_images_hash = ["e4bb24ec5be3057ad23afa5246279e75",
                                    "e57879c4e0c348fc062e525736e8e4ac",
                                    "a5243da825af4f616d8a1d4ecca2f5f4",
                                    "b4565e7a36690f6f908743e1fe0da3fe",                    
                                    "29f737ee006ce969967c020df101ecb8",
                                    "047d04ade761bde62c658556a082b548",
                                    "273d34b485bebeca688bf8da7ca33a4f",
                                    "08f3e9d2c44e5e4ff9ddfd738ef8528a"]

    main_path = os.getcwd()
    results_path = main_path + "/sets_of_output_vectors"

    for subdir, dirs, files in os.walk(results_path):
        break

    total_images = 0
    nb_images = [0, 0, 0, 0, 0, 0, 0, 0]
    mismatch_images = [0, 0, 0, 0, 0, 0, 0, 0]
    crash_images = 0
    list_mismatch_images = []
    for ld in dirs:
        #print(d)
        #dir_path = results_path + "/" + d
        #for ld in os.listdir(dir_path):
            if ld[0:5] == "fifo1":
                total_images = total_images + 1
                image_path = results_path + "/" + ld + "/*.jpg"                
                if len(glob.glob(image_path)) == 1:
                    image = int(glob.glob(image_path)[0][-5])
                    image_path = results_path + "/" + ld + "/" + str(image) + ".jpg"
                    
                    nb_images[image] = nb_images[image] + 1
                    if gen_image_hash(image_path) != reference_output_images_hash[image]:
                        mismatch_images[image] = mismatch_images[image] + 1
                        list_mismatch_images.append(image_path)
                else:
                    crash_images = crash_images + 1

    print("-------------------------------")
    print("----------- SUMMARY -----------")
    total_mismatch_images = sum(mismatch_images)
    total_err_images = crash_images + total_mismatch_images
    total_corrected_images = total_images - total_err_images
    perc_err_images = 100 * total_err_images / total_images
    print("Total images:", total_images)
    print("Nb of campaigns:", len(dirs))
    print("Nb of corrected images:", total_corrected_images)
    print("Nb of mismatch images:", total_mismatch_images)
    print("Nb of crash images:", crash_images)
    print("Nb of error images (mismatch + crash):", total_err_images)
    print("Perc. of corrected images:", str('{0:.2f}'.format(100-perc_err_images)) + "%")
    print("Perc. of error images:", str('{0:.2f}'.format(perc_err_images)) + "%")
    print("-------------------------------")
    print("--- LIST OF MISMATCH IMAGES ---")
    for i in list_mismatch_images:
        print(i)
    print("-------------------------------")


if __name__ == "__main__":
    main()
