import easyocr
import cv2 as cv
import os
import sys
import time


def main(IMG_PATH, name_of_image):
    detected_image0 = cv.imread(os.path.join(
        IMG_PATH, "foundTags", name_of_image))
    detected_image = cv.cvtColor(detected_image0, cv.COLOR_BGR2GRAY)
    reader = easyocr.Reader(['en'])  # , gpu=False
    result = reader.readtext(
        detected_image, allowlist='1234567890', min_size=425, width_ths=1)
    got_before = False
    got_partial_data = False
    detected_wagon_no = ""
    for detection in result:

        # print(detection[1])
        # print(detection[0])

        # detecting box coordinates
        # top_left = tuple(detection[0][0])
        # bottom_right = tuple(detection[0][2])
        # text = str(detection[1])+" : "+str(detection[2])

        # Drawing boxes
        # boxed_texted_image = cv.putText(cv.rectangle(detected_image0, (int(top_left[0]), int(top_left[1])), (int(bottom_right[0]), int(
        # bottom_right[1])), GREEN, 5), text, (int(top_left[0]), int(top_left[1])), FONT, 1, WHITE, 2, cv.LINE_AA)
        gotdata = False
        if len(detection[1]) >= 9 and len(detection[1]) <= 13:
            if detection[2] >= 0.80:
                detected_wagon_no = detected_wagon_no + detection[1]
                gotdata = True
            elif detection[2] < 0.80 and detection[2] >= 0.40:
                detected_wagon_no = detected_wagon_no + detection[1]
                gotdata = True
            elif detection[2] < 0.40:
                continue

        # check1ing for broken 5-6 digit numbers which will be merged to form 11 digit number
        if (len(detection[1]) >= 4 and len(detection[1]) <= 6):
            if got_before is False and detection[2] >= 0.80:
                temp_wagon_no = detection[1]
                temp_wagon_box = detection[0]
                got_before = True
                got_partial_data = True
            elif got_before is False and detection[2] < 0.80 and detection[2] >= 0.40:
                temp_wagon_no = detection[1]
                temp_wagon_box = detection[0]
                got_before = True
                got_partial_data = True
            elif got_before is True:
                # arranging the broken numbers in order(if found)
                if temp_wagon_box[2][1] < detection[0][2][1] and temp_wagon_box[3][1] < detection[0][3][1]:
                    detected_wagon_no = detected_wagon_no + \
                        temp_wagon_no + detection[1]
                elif temp_wagon_box[2][1] > detection[0][2][1] and temp_wagon_box[3][1] > detection[0][3][1]:
                    detected_wagon_no = detected_wagon_no + \
                        detection[1] + temp_wagon_no
                gotdata = True
            elif detection[2] < 0.40:
                continue

        # saving data if detected and writing it in the CSV
        if gotdata is True:
            if len(detected_wagon_no) >= 9 and len(detected_wagon_no) <= 13:
                # print("NUMBER DETECTED: ", detected_wagon_no)
                break
            else:
                gotdata = False
                continue
        if got_partial_data is True:
            # print("PARTIALLY DETECTED: got half of a number from this iteration: ")
            continue
        else:
            # print("NOT DETECTED: didn't get any number from this iteration")
            continue

    return detected_wagon_no


if __name__ == "__main__":
    PATH = os.getcwd()
    name_of_image = sys.argv[1]
    start = time.time()
    print(main(PATH, name_of_image))
    end = time.time()
    print(end - start)
