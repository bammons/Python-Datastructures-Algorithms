from pylab import *
from sys import argv
from skimage import img_as_float
from skimage import filter
from numpy import delete

'''
    Reduce the width of an image without losing quality using
    the seamcarving algorithm.
    @author Bailey Ammons
'''
def dual_gradient_energy(img):
    '''
        Calculate the vertical energy of each pixel
        @return: the energy representation of the img
        x_gradient = r_x**2 + g_x**2 + b_x**2
        y_gradient = r_y**2 + g_y**2 + b_y**2
        energy = x_gradient + y_gradient
    '''
    h, w = img.shape[:2]
    energy = [[0 for i in range(0, w)] for j in range(0, h)]
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    r_y = filter.hsobel(R)
    g_y = filter.hsobel(G)
    b_y = filter.hsobel(B)

    r_x = filter.vsobel(R)
    g_x = filter.vsobel(G)
    b_x = filter.vsobel(B)

    for i in range(0, h):
        for j in range(0, w):
            y_en = (r_y[i][j] ** 2) + (g_y[i][j] ** 2) + (b_y[i][j] ** 2)
            x_en = (r_x[i][j] ** 2) + (g_x[i][j] ** 2) + (b_x[i][j] ** 2)
            energy[i][j] = y_en + x_en
    return energy


def find_seam(img):
    '''
    Finds the minimum intensity seam to remove
    @variable: tracker the map of optimal paths for seams
    @variable: weighted_energy the weight of each path
    @return: the seam to remove
    '''
    row = len(img)
    col = len(img[0])
    tracker = [[0.0 for i in range(0, col)] for j in range(0, row)]
    weighted_energy = [[0.0 for i in range(0, col)] for j in range(0, row)]
    seam = []
    mini = +inf
    index = 0.0

    for i in range(1, row):
        for j in range(1, col - 1):
            left = float('inf')
            center = float('inf')
            right = float('inf')

            center = img[i - 1][j]
            if j == 1:
                right = img[i - 1][j + 1]
            elif j == (col - 2):
                left = img[i - 1][j - 1]
            else:
                right = img[i - 1][j + 1]
                left = img[i - 1][j - 1]

            if i == 1:
                weighted_energy[i][j] = img[i][j]
                tracker[i][j] = j
            else:
                if left <= right and left <= center:
                    weighted_energy[i][j] = img[i][j] + \
                        weighted_energy[i - 1][j - 1]
                    tracker[i][j] = j - 1
                elif center <= left and center <= right:
                    weighted_energy[i][j] = img[i][j] + \
                        weighted_energy[i - 1][j]
                    tracker[i][j] = j
                elif right <= center and right <= left:
                    weighted_energy[i][j] = img[i][j] + \
                        weighted_energy[i - 1][j + 1]
                    tracker[i][j] = j + 1

    for i in range(1, col - 1):
        val = weighted_energy[row - 1][i]
        if val < mini:
            mini = val
            index = i
    seam.insert(0, index)
    index = tracker[row - 1][index]

    for i in range(row - 2, -1, -1):
        seam.insert(0, index)
        index = tracker[i][index]

    return seam


def plot_seam(img, seam):
    '''
    Plot the seam to be removed on the picture
    '''
    red = [255.0, 0.0, 0.0]
    row = len(img)
    for i in range(0, row):
        img[i][seam[i]] = red

    return img


def remove_seam(img, seam):
    '''
    Remove the seam from the picture
    '''
    for i in range(0, len(seam)):
        col = seam[i]
        img[i, 1:col+1, :] = img[i, 0:col, :]

    return delete(img, 0, 1)


def main():
    print argv[1]
    passes = int(argv[2])
    img_seam = img_as_float(imread(argv[1]))
    img_no_change = img_as_float(imread(argv[1]))
    img_seam_carved = img_as_float(imread(argv[1]))

    for i in range(0, passes):
        print 'pass number: ' + str(i)
        energy = dual_gradient_energy(img_seam_carved)
        seam = find_seam(energy)

        img_seam = plot_seam(img_seam, seam)
        img_seam_carved = remove_seam(img_seam_carved, seam)

    figure()

    subplot(1, 3, 1)
    imshow(img_no_change)
    title("Original")

    subplot(1, 3, 2)
    imshow(img_seam)
    title("Seam Plot")

    subplot(1, 3, 3)
    imshow(img_seam_carved)
    title("Seam Carved")

    show()

if __name__ == '__main__':
    main()
