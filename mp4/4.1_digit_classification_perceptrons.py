import os.path as osp
import numpy as np
import linecache as lnc
import math

# CONSTANTS
SMOOTH_CONSTANT = 1.0   # can be any value in range 0.1 and 10, but the higher the better
FEAT_VALUES = 2          # f in {0,1}
IMG_WIDTH = 28
IMG_HEIGHT = 28
NUM_CLASSES = 10
NUM_TRAINING_EXEMPLARS = 5000
NUM_TESTING_EXEMPLARS = 1000

# PATH VARIABLES
digit_data_dpath = osp.dirname(__file__) + 'digitdata/'
train_data_fpath = digit_data_dpath + 'trainingimages.txt'
train_labels_fpath = digit_data_dpath + 'traininglabels.txt'
test_data_fpath = digit_data_dpath + 'testimages.txt'
test_labels_fpath = digit_data_dpath + 'testlabels.txt'

# GLOBAL DATA STRUCTURES
class_train_ct = [0]*NUM_CLASSES       # for digit classes 0-9
class_priors = [0.0]*NUM_CLASSES       # (float) P(class)
weight_vectors = map(np.matrix, [ [[0.0]*IMG_HEIGHT for _ in range(IMG_WIDTH)] ]*NUM_CLASSES)
# P(F_{ij} = f | class)

### HELPER FUNCTIONS ###
def compute_likelihood():
    # cycle through training examples in multiple passes/epochs
    # for each training example
    #   classify with current weights: y' = sgn(w * x)
    #   if classification incorrect, update weights: w ← w +α (y − y') x
    #       α is a learning rate that should decay as a function of epoch t
    #       e.g., 1000/(1000+t)


    # go through the features' counts and calculate their likelihood wrt each class with Laplace smoothing
    for class_index in range(len(class_train_ct)):
        likelihood_matrices[class_index] = (likelihood_matrices[class_index] + SMOOTH_CONSTANT) / float(class_train_ct[class_index] + FEAT_VALUES*SMOOTH_CONSTANT)

    # compute priors
    for class_index in range(len(class_train_ct)):
        class_priors[class_index] = class_train_ct[class_index] / float(NUM_TRAINING_EXEMPLARS)

def print_highest_lowest_MAP_images():
    for digit in range(len(prototypical_img_loc)):
        _, min_MAP_img_idx, _, max_MAP_img_idx = prototypical_img_loc[digit]

        print 'Test example with lowest posterior probability for class %d:' % digit
        for line_no in range(min_MAP_img_idx*IMG_HEIGHT, (min_MAP_img_idx + 1)*IMG_HEIGHT):
            print lnc.getline(test_data_fpath, line_no).strip('\n')

        print 'Test example with highest posterior probability for class %d:' % digit
        for line_no in range(max_MAP_img_idx*IMG_HEIGHT, (max_MAP_img_idx + 1)*IMG_HEIGHT):
            print lnc.getline(test_data_fpath, line_no).strip('\n')

def updateWeights():
    return


### MAIN ###
def main():
    ### TRAINING
    with open(train_data_fpath, 'r') as train_images, open(train_labels_fpath, 'r') as train_labels:
        # init weights
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

            # accumulate feat val for each pixel of this class' global data storage structure

            likelihood_matrices[class_num] += train_img_fvals
            class_train_ct[class_num] += 1

    # compute_likelihood()

    '''
    ### TESTING ###
    with open(test_data_fpath, 'r') as test_images:

        for nth_img in range(NUM_TESTING_EXEMPLARS):
            class_MAP = [None]*NUM_CLASSES

            # grab pixel data -> features from this test image
            test_img_fvals = np.matrix([[0]*IMG_HEIGHT for _ in range(IMG_WIDTH)])
            for row_idx in range(IMG_HEIGHT):
                row_data = test_images.readline()
                for col_idx in range(IMG_WIDTH):
                    if row_data[col_idx] == '+' or row_data[col_idx] == '#':
                        test_img_fvals[row_idx, col_idx] = 1

            # figuring out the likelihood that each image belongs to a certain class
            for class_no in range(len(class_train_ct)):
                class_matrix = likelihood_matrices[class_no]

                # to avoid underflow, we work with the log of P(class)*P(f_{1,1}|class)*...*P(f_{28,28}|class)
                posterior_prob = math.log(class_priors[class_no])

                # calculate log P(class)+log P(f_{1,1}|class)+log P(f_{1,2}|class)+...+log P(f_{28,28}|class)
                for row_idx in range(IMG_HEIGHT):
                    for col_idx in range(IMG_WIDTH):
                        if test_img_fvals[row_idx, col_idx] == 1:
                            posterior_prob += math.log(class_matrix[row_idx, col_idx])
                        else:
                            posterior_prob += math.log(1 - class_matrix[row_idx, col_idx])

                # save the MAP prob for each class, determine test label guess based on argmax of values in array
                class_MAP[class_no] = posterior_prob

                # update the most and least "prototypical" instances of each digit class
                class_min_prob, min_idx, class_max_prob, max_idx = prototypical_img_loc[class_no]
                if posterior_prob < class_min_prob:
                    prototypical_img_loc[class_no] = (posterior_prob, nth_img, class_max_prob, max_idx)
                if posterior_prob > class_max_prob:
                    prototypical_img_loc[class_no] = (class_min_prob, min_idx, posterior_prob, nth_img)

            # closely matching test images have MAP ~1.0, which corresponds to (-) near 0 while MAP ~0 -> (-inf)
            class_guess[nth_img] = class_MAP.index(max(class_MAP))

    ### EVALUATION ###
    with open(test_labels_fpath, 'r') as test_labels:
        for nth_lbl in range(NUM_TESTING_EXEMPLARS):
            actual_class = int(test_labels.readline())

            if actual_class == class_guess[nth_lbl]:
                classification_rate[actual_class] += 1

            class_test_ct[actual_class] += 1
            confusion_matrix[actual_class, class_guess[nth_lbl]] += 1

    for idx in range(len(classification_rate)):
        # calculate the percentage of all test images of a given digit correctly classified
        classification_rate[idx] /= float(class_test_ct[idx])

        # entry in row r and column c is the percentage of test images from class r that are classified as class c
        for confusion_col in range(len(class_test_ct)):
            confusion_matrix[idx, confusion_col] /= float(class_test_ct[idx])

    # TO PRINT FOR REPORT, UNCOMMENT THESE:
    np.set_printoptions(precision=3)
    print classification_rate
    print confusion_matrix
    print_highest_lowest_MAP_images()

    def print_odds(matrix):
        for row_idx in range(IMG_HEIGHT):
            for col_idx in range(IMG_WIDTH):
                temp = math.log(matrix[row_idx, col_idx])
                if temp > -0.75 and temp < 1.25: print ' ',
                elif temp > 0: print '+',
                else: print '-',
            print ''

    def print_class(matrix):
        for row_idx in range(IMG_HEIGHT):
            for col_idx in range(IMG_WIDTH):
                temp = math.log(matrix[row_idx, col_idx])
                if temp > -1.1 and temp < -0.9: print ' ',
                elif temp > -1: print '+',
                else: print '-',
            print ''

    ### ODDS RATIO ###
    most_confusing_indices = get_confusing_idx(confusion_matrix)

    # for each pair of the 4 chosen pairs with highest confusion probability
    for c1, c2 in most_confusing_indices:
        class_1 = likelihood_matrices[c1]
        class_2 = likelihood_matrices[c2]
        class_odds = np.matrix([[0.0]*IMG_HEIGHT for _ in range(IMG_WIDTH)])
        for row_idx in range(IMG_HEIGHT):
            for col_idx in range(IMG_WIDTH):
                class_odds[row_idx, col_idx] = class_1[row_idx, col_idx]/class_2[row_idx, col_idx]

        print c1, c2
        print_class(class_1)
        print '\n'
        print_class(class_2)
        print '\n'
        print_odds(class_odds)
        print '\n'

    '''
