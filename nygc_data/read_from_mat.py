"""

by Hao Xue @ 2/06/18

"""

from scipy import io
import numpy as np


LEN_17_NUM = 14662
TRAIN_NUM = int(LEN_17_NUM * 0.8)
VAL_NUM = int((LEN_17_NUM - TRAIN_NUM) / 2)
# mat_data = io.loadmat('trajectoriesNew.mat')
# print(type(mat_data))
# print(mat_data.keys())
# print(mat_data['trks'].shape)
# print(type(mat_data['trks'][0]))
# print(np.shape(mat_data['trks'][0]))
# print(mat_data['trks'][0][0][2])
# print(np.shape(mat_data['trks'][0][0][2]))


def mat_to_trajectories(mat_file):
    trajectories = []
    mat_data = io.loadmat(mat_file)
    trks = mat_data['trks'][0]

    for i in range(len(trks)):
        x_i = trks[i][0]
        y_i = trks[i][1]
        t_i = trks[i][2]
        traj = np.concatenate((x_i, y_i, t_i), axis=1)
        trajectories.append(traj)

    return trajectories


def process(trajectories):
    output = []
    for traj in trajectories:
        if len(traj) >= (9 + 16) * 10:
            temp = []
            for i in range(len(traj)):
                if i % 10 == 0:
                    temp.append([traj[i][0], traj[i][1], traj[i][2]])
            output.append(temp[0: 9+16])
    print(len(output))
    print(np.shape(np.array(output)))
    print(output[1])
    output = np.reshape(output, [-1, 16+9, 3])
    return output


def write_to_file(trajectories, out_file):
    counter = 0
    with open(out_file, "w") as f:
        for t in trajectories:
            if len(t) > (9+8) * 10 and counter < int(TRAIN_NUM / 9) - 1050:
                counter += 1
                len_counter = 0
                for one_time in t:
                    if one_time[-1] % 10 == 1 and len_counter < 9+8:
                        len_counter += 1
                        f.write(f"{one_time[-1]} {counter} {one_time[0]} {one_time[1]}" + "\n")

    f.close()
    print(counter)
    print(counter == TRAIN_NUM)


def write_val_file(trajectories, val_file):
    counter = 0
    with open(val_file, "w") as f:
        for t in trajectories:
            if len(t) > (9+8) * 10:
                counter += 1
                len_counter = 0
                if TRAIN_NUM <= counter < TRAIN_NUM + VAL_NUM:
                    for one_time in t:
                        if one_time[-1] % 10 == 1 and len_counter < 9+8:
                            len_counter += 1
                            f.write(f"{one_time[-1]} {counter} {one_time[0]} {one_time[1]}" + "\n")

    f.close()
    print(counter)
    print(counter == VAL_NUM)


def write_test_file(trajectories, test_file):
    counter = 0
    with open(test_file, "w") as f:
        for t in trajectories:
            if len(t) > (9+8) * 10:
                counter += 1
                len_counter = 0
                if counter > TRAIN_NUM + VAL_NUM:
                    for one_time in t:
                        if one_time[-1] % 10 == 1 and len_counter < 9+8:
                            len_counter += 1
                            f.write(f"{one_time[-1]} {counter} {one_time[0]} {one_time[1]}" + "\n")

    f.close()
    print(counter)
    print(counter == LEN_17_NUM)


traj = mat_to_trajectories('trajectoriesNew.mat')
write_to_file(traj, out_file="cs_train.txt")
# write_val_file(traj, val_file="cs_val.txt")
# write_test_file(traj, test_file="cs_test.txt")
# data = process(mat_to_trajectories('trajectoriesNew.mat'))
# print(np.shape(data))
# np.save('data_NYGC_p16_time.npy', data)
# a = np.load('data_NYGC_p16_time.npy')
# print(np.shape(a))
