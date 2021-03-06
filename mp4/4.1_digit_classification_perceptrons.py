import os.path as osp
import numpy as np
import linecache as lnc
import math
import random

### CONSTANTS ###
IMG_WIDTH = 28
IMG_HEIGHT = 28
NUM_CLASSES = 10
NUM_TRAINING_EXEMPLARS = 5000
NUM_TESTING_EXEMPLARS = 1000

### PATH VARIABLES ###
digit_data_dpath = osp.dirname(__file__) + 'digitdata/'
train_data_fpath = digit_data_dpath + 'trainingimages.txt'
train_labels_fpath = digit_data_dpath + 'traininglabels.txt'
test_data_fpath = digit_data_dpath + 'testimages.txt'
test_labels_fpath = digit_data_dpath + 'testlabels.txt'

### GLOBAL DATA STRUCTURES ###
# weight_vectors = map(np.matrix, [ [[random.uniform(0.0, 1.0)]*IMG_HEIGHT for _ in range(IMG_WIDTH)] ]*NUM_CLASSES)
weight_vectors = map(np.matrix, [ [[0.0]*IMG_HEIGHT for _ in range(IMG_WIDTH)] ]*NUM_CLASSES)
dot_product = [0.0]*NUM_CLASSES       # temporary storage for digit classes 0-9 for each input img
class_test_ct = [0]*NUM_CLASSES       # for digit classes 0-9
test_guess = [None]*NUM_TESTING_EXEMPLARS
classification_rate = [0.0]*NUM_CLASSES
confusion_matrix = np.matrix([[0.0]*NUM_CLASSES for _ in range(NUM_CLASSES)])    # careful not to bamboozle yourself

### MAIN ###
def main():
    ### TRAINING
    # cycle through training examples in multiple passes/epochs
    for epoch in range(5):
        with open(train_data_fpath, 'r') as train_images, open(train_labels_fpath, 'r') as train_labels:
            # weights initialized originally as matrix of zeros
            for class_lbl in train_labels:
                class_num = int(class_lbl)

                # compute the feature values for this example training image
                train_img_fvals = np.matrix([[0]*IMG_HEIGHT for _ in range(IMG_WIDTH)])
                for row_idx in range(IMG_HEIGHT):
                    row_data = train_images.readline()
                    for col_idx in range(IMG_WIDTH):
                        if row_data[col_idx] == '+' or row_data[col_idx] == '#':
                            train_img_fvals[row_idx, col_idx] = 1
                        # else, feature value remains 0 for background pixel

                # dot product of train_img_fvals with all 0-9 weight vectors
                for class_digit in range(NUM_CLASSES):
                    # dot_product[class_digit] = np.dot(weight_vectors[class_digit].A1, train_img_fvals.A1)
                    dot_product[class_digit] = np.dot(weight_vectors[class_digit].A1, train_img_fvals.A1)

                # get the digit classification via the index of the argmax of this array
                digit_guess = dot_product.index(max(dot_product))

                # compare prediction with class label & update if classification is incorrect
                if digit_guess != class_num:
                    weight_vectors[class_num] = weight_vectors[class_num] + (1/(epoch+1))*train_img_fvals
                    weight_vectors[digit_guess] = weight_vectors[digit_guess] - (1/(epoch+1))*train_img_fvals

    ### TESTING ###
    with open(test_data_fpath, 'r') as test_images:
        for nth_img in range(NUM_TESTING_EXEMPLARS):
            # grab pixel data -> features from this test image
            test_img_fvals = np.matrix([[0]*IMG_HEIGHT for _ in range(IMG_WIDTH)])
            for row_idx in range(IMG_HEIGHT):
                row_data = test_images.readline()
                for col_idx in range(IMG_WIDTH):
                    if row_data[col_idx] == '+' or row_data[col_idx] == '#':
                        test_img_fvals[row_idx, col_idx] = 1

            for class_digit in range(NUM_CLASSES):
                # dot_product[class_digit] = np.dot(weight_vectors[class_digit].A1, train_img_fvals.A1)
                dot_product[class_digit] = np.dot(weight_vectors[class_digit].A1, test_img_fvals.A1)

            test_guess[nth_img] = dot_product.index(max(dot_product))

    ### EVALUATION ###
    with open(test_labels_fpath, 'r') as test_labels:
        for nth_lbl in range(NUM_TESTING_EXEMPLARS):
            actual_class = int(test_labels.readline())

            if actual_class == test_guess[nth_lbl]:
                classification_rate[actual_class] += 1

            class_test_ct[actual_class] += 1
            confusion_matrix[actual_class, test_guess[nth_lbl]] += 1

    classification_rate_avg = 0.0
    for idx in range(len(classification_rate)):
        # calculate the percentage of all test images of a given digit correctly classified
        classification_rate[idx] /= float(class_test_ct[idx])
        classification_rate_avg += classification_rate[idx]

        # entry in row r and column c is the percentage of test images from class r that are classified as class c
        for confusion_col in range(len(class_test_ct)):
            confusion_matrix[idx, confusion_col] /= float(class_test_ct[idx])

    classification_rate_avg /= len(classification_rate)

    # TO PRINT FOR REPORT, UNCOMMENT THESE:
    np.set_printoptions(precision=3)

    print 'The classification rate matrix is as follows: \n{}\n'.format(classification_rate)
    print 'The classification rate average is as follows: {:.5f}\n'.format(classification_rate_avg)
    print 'The confusion matrix is as follows:'
    print confusion_matrix

if __name__ == "__main__":
    main()
