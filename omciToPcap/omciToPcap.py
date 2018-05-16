import os

ether_packet_header = "00000000000100000000000288b5"


# it is used for proper alignment such as fro 0000 to 00 00
def add_space(line):
    for i in range(2, 64, 3):
        line = line[:i] + " " + line[i:]
    return line


# make proper alignment
def make_align(omci_line):
    align_list = []

    # add the ethernet packet header to each captured line
    omci_line = ether_packet_header + omci_line

    # use these values for adding 0000 0010 0020 and 0030 for each 16-byte segment start
    align_str = "0000"
    align_number = 0

    start_index = 0

    for i in range(32, 129, 32):

        # add to list 16 bytes segment such as 0000 ether_packet_header with spaces and after then the original message
        align_list.append(align_str + " " + add_space(omci_line[start_index:i]))
        start_index = i

        # for 0010 0020 0030
        align_number += 10
        align_str = align_str[:2] + str(align_number)

    return align_list


def write_to_file(d):
    try:
        f = open("omciForPcap.txt", "w+")
        for value_list in d.values():
            for line in value_list:
                f.write(line + "\n")
            f.write("\n\n")
        f.close()
        print("omciForPcap.txt is written")
    except IOError as e:
        print ("IOError while writing proper omci messages", e)


# read the line and make proper alignments
def read_the_file(opened_file):
    # find the lines that include "capture:" and get the capture part of the line
    captured_lines = map(lambda cline: cline.split("capture:")[1].strip(),
                         filter(lambda line: "capture:" in line, opened_file.readlines()))

    # for each line, make the proper alignment and assign them to a dictionary
    # the dictionary is like {0: [16-byte-segment \n , 16-byte-segment \n]
    d = {}
    for count, line in enumerate(captured_lines):
        d[count] = make_align(line)
    return d


# get the file path from user
# for example: /home/gamzeab/omci-log.msg
def get_file_path():
    return raw_input("Please enter the file path of OMCI log file:")


# open the file for the given path
def open_file(file_path):
    try:
        return open(file_path, "r")
    except IOError as e:
        print ("IOError is occurred while reading the file:", e)


if __name__ == "__main__":
    file_path = get_file_path()
    opened_file = open_file(file_path)

    d = read_the_file(opened_file)
    write_to_file(d)
    opened_file.close()

    os.system("text2pcap omciForPcap.txt omci.pcap")