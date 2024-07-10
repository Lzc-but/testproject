import numpy as np


class Channel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Void:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def load_voids_channels_from_file(filename_cavd):
    """
    Read interstices and channel segments from net file calculated by cavd
    :param filename_cavd: NET filename
    :return: dict, interstices and channel segments
    """
    voids_dict = {}
    channels_dict = {}
    flag_p = 0
    flag_n = 0
    file = open(filename_cavd, "r")
    for line in file.readlines():
        if "Interstitial" in line:
            flag_p = 1
            flag_n = 0
            continue
        if "Connection" in line:
            flag_p = 0
            flag_n = 1
            continue
        if flag_p == 1:
            line = line.split()
            if len(line) > 3:
                void = Void()
                void.id = int(line[0])
                void.label = int(line[1])
                void.coord = np.array(
                    [np.float64(line[2]), np.float64(line[3]), np.float64(line[4])]
                )
                void.radii = np.float64(line[5])
                voids_dict[void.id] = void
        if flag_n == 1:
            line = line.split()
            if len(line) > 4:
                channel = Channel()
                channel.start = int(line[0])
                channel.end = int(line[1])
                channel.phase = [int(line[2]), int(line[3]), int(line[4])]
                channel.coord = np.array(
                    [np.float64(line[5]), np.float64(line[6]), np.float64(line[7])]
                )
                channel.radii = np.float64(line[8])
                channels_dict[(channel.start, channel.end)] = channel
    return voids_dict, channels_dict


def getperinputfile(filecavd):
    voids_dict, channels_dict = load_voids_channels_from_file(filecavd)
    indextable = {}
    for index, value in enumerate(voids_dict):
        indextable[value] = index + 1
    with open("icsd_155912per.txt", "w") as f:
        f.writelines(str(len(voids_dict)) + "\n")
        for channel_id, channel in channels_dict.items():
            line = (
                str(indextable[channel_id[0]])
                + ","
                + str(indextable[channel_id[1]])
                + ","
                + str(channel.phase[0])
                + ","
                + str(channel.phase[1])
                + ","
                + str(channel.phase[2])
                + ",3,1\n"
            )
            f.writelines(line)
    print("ss")


getperinputfile(
    r"C:\Users\33389\Desktop\ciffile\icsd_LiLaTiO-pubowei-240510\icsd_165480modify_transport.net"
)
print("ss")
