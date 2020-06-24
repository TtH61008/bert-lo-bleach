import argparse
import pandas as pd
import csv

from pyknp import Juman
jumanpp = Juman()


result_df = pd.DataFrame()
increment = 0


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('lo_tsv')
parser.add_argument('bleach_tsv')
parser.add_argument('output_dir')
args = parser.parse_args()


with open(args.lo_tsv, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        juman_result = jumanpp.analysis(row[0])
        juman_result_joined = " ".join(map(lambda x: x.midasi, juman_result.mrph_list()))
        print(juman_result_joined)
        result_df = result_df.append({"index":f"data{increment:04}","label":0,"nannka":"*","sentence":juman_result_joined}, ignore_index=True)
        increment += 1

with open(args.bleach_tsv, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        juman_result = jumanpp.analysis(row[0])
        juman_result_joined = " ".join(map(lambda x: x.midasi, juman_result.mrph_list()))
        print(juman_result_joined)
        result_df = result_df.append({"index":f"data{increment:04}","label":1,"nannka":"*","sentence":juman_result_joined}, ignore_index=True)
        increment += 1

result_df["label"] = result_df["label"].astype("int")

random_sorted_df = result_df.sample(frac=1)

train_split_len = int(len(random_sorted_df)*0.6)
dev_split_len = int(len(random_sorted_df)*0.8)

random_sorted_df[:train_split_len].to_csv(args.output_dir+"/train.tsv", sep="\t", header=None,index=None)
random_sorted_df[train_split_len:dev_split_len].to_csv(args.output_dir+"/dev.tsv", sep="\t", header=None,index=None)
random_sorted_df[dev_split_len:][["index", "sentence"]].to_csv(args.output_dir+"/test.tsv", sep="\t", index=None)
