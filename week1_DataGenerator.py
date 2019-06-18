import numpy as np
import csv

FILENAME = 'data2.csv'

def create_cluster(x_loc, x_scale, y_loc, y_scale, z_loc, z_scale, bin, num_points):
    '''
    Creates a gaussian distribution of x, y, and z coordinates with an
    associated binary value. Appends the data of the cluster to the csv
    with FILENAME.
        Args:
            x_loc: Center of the distribution on the x-axis
            x_scale: Standard deviation of x coordinates from the center
            y_loc: Center of the distribution on the y-axis
            y_scale: Standard deviation of y coordinates from the center
            z_loc: Center of the distribution on the z-axis
            z_scale: Standard deviation of z coordinates from the center
            bin: Binary value of data (either 0 or 1)
            num_points: Number of points in the cluster
        Returns:
            None
    '''
    x = np.random.normal(x_loc, x_scale, num_points)
    y = np.random.normal(y_loc, y_scale, num_points)
    z = np.random.normal(z_loc, z_scale, num_points)
    with open(FILENAME, mode = 'a', newline='') as f:
        data_writer = csv.writer(f)
        for i in range(len(x)):
            data_writer.writerow([x[i], y[i], z[i], bin])

def create_file():
    '''
    Creates a csv file with FILENAME. Writes the first line with the
    data names of the csv. Makes calls to create_cluster to generate
    the rest of the data
        Args:
            None.
        Returns:
            None.
    '''
    with open(FILENAME, mode = 'w', newline='') as f:
        data_writer = csv.writer(f)
        data_writer.writerow(['x_coord', 'y_coord', 'z_coord', 'bin'])
    # Creates 9 clusters that follow the shape of the vertices of a cube with
    # another cluster in the middle all with bin value 1. Total 10,000 points.
    create_cluster(0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1, 1000)
    create_cluster(10.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1, 1000)
    create_cluster(0.0, 1.0, 10.0, 1.0, 0.0, 1.0, 1, 1000)
    create_cluster(10.0, 1.0, 10.0, 1.0, 0.0, 1.0, 1, 1000)
    create_cluster(0.0, 1.0, 0.0, 1.0, 10.0, 1.0, 1, 1000)
    create_cluster(10.0, 1.0, 0.0, 1.0, 10.0, 1.0, 1, 1000)
    create_cluster(0.0, 1.0, 10.0, 1.0, 10.0, 1.0, 1, 1000)
    create_cluster(10.0, 1.0, 10.0, 1.0, 10.0, 1.0, 1, 1000)
    create_cluster(5.0, 1.0, 5.0, 1.0, 5.0, 1.0, 1, 2000)
    # Creates 10,000 points normally distributed throughtout the plot to
    # obscure the above clusters with bin value 0.
    create_cluster(5.0, 10.0, 5.0, 10.0, 5.0, 10.0, 0, 10000)

def main():
    create_file()

if __name__ == '__main__':
    main()