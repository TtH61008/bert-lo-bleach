import argparse
from pyknp import Juman
jumanpp = Juman()
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('input_str')
args = parser.parse_args()


juman_result = jumanpp.analysis(args.input_str)
juman_result_joined = " ".join(map(lambda x: x.midasi, juman_result.mrph_list()))
print(juman_result_joined)
