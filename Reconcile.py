import os
import sys
from argparse import ArgumentParser
from glob import glob
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import gzip
import traceback
 

def getargs():
   parser = ArgumentParser()
   parser.add_argument("-gzf", "--gzfile",help="starts parsing the directory")
   args = parser.parse_args()
   
   if args.gzfile is None or not (os.path.exists(args.gzfile)):
      pprint(f" File Passed  ⛔ {args.gzfile} does not exist    ")
      sys.exit()
   return args

def pprint(text):
   size = os.get_terminal_size()
   print(text.center(size.columns),"\n")

def process(gzfile):
    try:
        df = pd.DataFrame(columns = ['Object','Added', 'Subtracted','Difference'])
        with gzip.open( gzfile, 'rb') as f:
            for line in f:
                if isinstance(line, (bytes, bytearray)):
                    line = line.decode("utf-8")
                if (("OBJTN_TRC" in line) and ("Object" in line)):
                    ob =  line.split("Object")
                    if (len(ob) <= 1):
                        continue
                else:
                    continue
                ob_name = ob[1].split()[0]
                ob_name = ob_name.split(".",1)[1]
                if (df.isin([ob_name]).any().any()):
                    if "added" in ob[1]: 
                        df.loc[df['Object'] == ob_name, 'Added'] = df.loc[df.Object==ob_name, 'Added'].values[0] +1
                    if "subtracted" in ob[1]: 
                        df.loc[df['Object'] == ob_name, 'Subtracted'] = df.loc[df.Object==ob_name, 'Subtracted'].values[0] +1 
                else:
                    added = 0
                    subtracted = 0
                    if "added" in ob[1]:
                        added = 1
                    if "subtracted" in ob[1]:
                        subtracted = 1
                    df = df.append({'Object' : ob_name, 'Added' : added, 'Subtracted': subtracted},ignore_index = True)
        df['Difference'] = df.apply(lambda x: "NO" if x['Added'] == x['Subtracted']  else "YES", axis=1)
        df.index = np.arange(1, len(df) + 1)
        df.to_excel("Reconcile.xls")
        pprint("Successfully Processed ✌️")
    except Exception as e:
        pprint(f"Exception 😭 {e}")
        traceback.print_exc()
                          
if __name__ == "__main__":
   os.system('clear')
   pprint("##################################")
   pprint("##### RECONCILE  TABLE ####")
   pprint("##################################")
   args = getargs()
   pprint(f"➡️ FILE TO BE PARSED  :{args.gzfile} \n")
   process(args.gzfile)
   sys.exit()
