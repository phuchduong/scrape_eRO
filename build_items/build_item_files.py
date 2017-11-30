#!/usr/bin/env python.
'''
    File name: build_item_files.py
    Date created: November 29, 2017
    Python version: 3.6.1
    Purpose:
        Rebuild the eRO item database by...
        - Merge the two webscraped TSV files together obtained from:
            - tamsinwhitfield
            - web archive (the way back machine)
        - Join with and insert into the item_db.txt
        - Join with and insert into iteminfo
        - Validate sprite files

    Author: Phuc H Duong
    Website: phuchduong.io
    Linkedin: https://www.linkedin.com/in/phuchduong/
'''


def main():
    ###############
    # file system #
    ###############

    # your repo directory should look like this
    #
    # /repo root (essencero_restoration)
    #   /web_scrape_tamsinwhitfield
    #       /old_essence_item_db.txt
    #   /web_scrape_web_archive
    #       /item_db_web_archive.tsv
    repo_dir = "D:/repos/essencero_restoration"  # change this to your own

    # data webscraped from tamsinwhitfield
    tw_dir = "/web_scrape_tamsinwhitfield/old_essence_item_db.txt"  # tab deliminated

    # data webscraped from web archive (the way back machine)
    wa_dir = "/web_scrape_web_archive/item_db_web_archive.tsv"

    ##################
    # old eRO fields #
    ##################
    # List of item ids of items that are being left behind and not integrated into the new server.
    # Treatment: These item should be skipped during the merge.
    old_ero_ignore_list = [
        20631,  # Drooping Aria
        20522,  # Drooping Aria Stark
        20524,  # Drooping Biomaster
        20194,  # Drooping Cebalrai
        20521,  # Drooping Doctor Wyrd
        20568,  # Drooping Eike
        20525,  # Drooping Eileithyia
        20633,  # Drooping Faustus
        20154,  # Drooping Gazel
        20557,  # Drooping Mokona
        20755,  # Drooping Mulder
        20128,  # Drooping Neko
        20508,  # Drooping Nora Stark
        20634,  # Drooping Okale
        20754,  # Drooping Paradox924X
        20165,  # Drooping Pikachu
        20635,  # Drooping Praetor
        20558,  # Drooping Saproling
        20506,  # Drooping Skwipe
        20576,  # Drooping Super Scope
        20513,  # Drooping Takara
        20507,  # Drooping Tony Stark
        20514,  # Drooping Vhaidra
        20552,  # Drooping Windii
        20517,  # Drooping Xackery
        20799,  # Drooping Yami
        20502,  # Drooping Yosh
        20581,  # Drooping Zhao
    ]

    ######################
    # tamsinwhitfield db #
    ######################
    # Read in tamsinwhitfield as a dictionary by item_id as the key, remaining line as values
    # Ignores any item in the ignore list.
    with open(file=repo_dir + tw_dir, mode="r") as tw:
        print("Opening... " + repo_dir + tw_dir)
        tw_header = tw.readline()  # header
        tw_dict = parse_item_scrape_tsv(file_reader=tw, ignore_list=old_ero_ignore_list)
        print("Found... " + str(len(tw_dict)) + " items...")

    ##################
    # web archive db #
    ##################
    # Read in webarchive as a dictionary by item_id as the key, remaining line as values
    # Ignores any item in the ignore list.
    with open(file=repo_dir + wa_dir, mode="r") as wa:
        print("Opening... " + repo_dir + wa_dir)
        wa_header = wa.readline()  # header
        wa_dict = parse_item_scrape_tsv(file_reader=wa, ignore_list=old_ero_ignore_list)
        print("Found... " + str(len(wa_dict)) + " items...")

    ##################################################
    # Combine both old item db dictionaries together #
    ##################################################

    # Combines both item keys togther into a set that is sorted
    item_ids_all = list(wa_dict.keys()) + list(tw_dict.keys())  # Adds both item lists together
    item_ids_all = set(item_ids_all)  # removes duplicate item_ids
    item_ids_all = sorted(item_ids_all)  # sorts the keys

    for item_id in item_ids_all:
        # parse tw items
        if item_id in tw_dict:
            tw_item = tw_dict[item_id]
        else:
            # Item does not exist in tw_item_db
            print()

        # parse wa items
        if item_id in wa_dict:
            wa_item = wa_dict[item_id]
        else:
            # Item does not exist in wa_item_db
            print()

    # # finds item_ids that exist in both lists
    # item_id_both_exists = set(tw_dict.keys()).intersection(wa_dict.keys())
    # item_id_both_exists = sorted(item_id_both_exists)
    # print("Fusing item lists... " + )

    # # finds item_ids that only exists exclusively in tamsinwhitfield_db (tw_dict)
    # tw_exclusive = [x for x in tw_dict.keys() if x not in wa_dict.keys()]

    # # finds item_ids that only exists exclusively in web_archive_db (wa_dict)
    # wa_exclusive = [x for x in wa_dict.keys() if x not in tw_dict.keys()]


# Parses a TSV and returns a dictionary.
# Grabs the first item in the TSV on each line as the key, converts
#   key to integer.
# The remaining line becomes the value of the key.
# Ex. "a\tb\tc\td\te\t\n" input would return
# {
#   "a": "b\tc\td\te\t\n"   
# }
# Takes in a list of keys to ignore and skip
def parse_item_scrape_tsv(file_reader, ignore_list):
    tsv_dict = {}
    for line in file_reader:  # body
        item_id = int(line.split("\t")[0])
        if item_id not in ignore_list:
            # skip items in the ignore list
            item_body = line[len(str(item_id)) + 1:]  # grabs everything after the item_id
            tsv_dict[item_id] = item_body
    return tsv_dict

def refractor_this():
    wa_keys = sorted([int(x) for x in wa_dict.keys()])  # converts keys to int
    wa_keys = [x for x in wa_keys if x not in old_ero_ignore_list]  # Remove ignore list

    # Combine tamsinwhitfield and web archive lists, filtering ignored items

    # build a master key list of item ids in both lists
    both_exists = set(tw_dict.keys()).intersection(wa_dict.keys())  # finds items that exist in both lists
    both_exists = [int(x) for x in both_exists]  # converts all elements to integer from string
    both_exists = sorted(both_exists)  # sorts keys

    # tw_exclusive = [x for x in tw_dict.keys() not in both_exists]  # items that only appear in tw
    # wa_exclusive = [x for x in wa_dict.keys() not in both_exists]  # items that only appear in wa

    # for item in tw_dict.keys():
    #     print(item)

main()
