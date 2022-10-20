import os
import sys
from argparse import ArgumentParser
from glob import glob
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import gzip

 

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
        df = pd.DataFrame(columns = ['Object','Raised', 'Dropped'])
        with gzip.open( gzfile, 'rb') as f:
            for line in f:
                if isinstance(line, (bytes, bytearray)):
                    line = line.decode("utf-8")
                ob =  line.split("object")
                pprint(ob)
                ob_name = ob[1].split()[0]
                if (df.isin([ob_name]).any().any()):
                    if "raised" in ob[1]: 
                        df.loc[df['Object'] == ob_name, 'Raised'] = df.loc[df.Object==ob_name, 'Raised'].values[0] +1
                    if "dropped" in ob[1]: 
                        df.loc[df['Object'] == ob_name, 'Dropped'] = df.loc[df.Object==ob_name, 'Dropped'].values[0] +1 
                else:
                    raised = 0
                    dropped = 0
                    if "raised" in ob[1]:
                        raised = 1
                    if "dropped" in ob[1]:
                        dropped = 1
                    df = df.append({'Object' : ob_name, 'Raised' : raised, 'Dropped': dropped},ignore_index = True)
        df['Difference'] = df.apply(lambda x: "YES" if x['Raised'] == x['Dropped']  else "NO", axis=1)
        df.index = np.arange(1, len(df) + 1)
        df.to_excel("Reconcile.xls")
        pprint("Successfully Processed ✌️")
    except Exception as e:
        pprint(f"Exception 😭 {e}")
                          
if __name__ == "__main__":
   os.system('clear')
   pprint("##################################")
   pprint("##### RECONCILE  TABLE ####")
   pprint("##################################")
   args = getargs()
   pprint(f"➡️ FILE TO BE PARSED  :{args.gzfile} \n")
   process(args.gzfile)
   sys.exit()
