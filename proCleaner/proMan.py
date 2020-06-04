from handEl import handEl
import json
import pprint
import traceback
from tqdm import tqdm
pp = pprint.pprint

class proMan :
    def __init__(self, host, port, index="default") :
        self.handel = handEl(host, port, index)
        self.index = index
        self.table  = None

    def indexing(self, index) :
        self.index = index

    def make(self, fpath=None, fname=None, cpath=None, d=None) :
        if fpath and fname or cpath :
            try :
                with open((cpath if cpath else fpath+fname)) as openfile :
                    self.table = json.load(openfile)
            except Exception as e :
                self.error(e, "JSON")
                return False
        elif d :
            self.table = d
        else :  return False
        return True
        
    # akeyalias : Aliasing document properties columns
    # overturn  : Delete the all exists data
    def proper(self, ikey, akey, akeyalias=None, overturn=False, cry=True) :
        if self.table and type(self.table) == type(list()):
            if cry : pbar = tqdm(total = len(self.table))
            self.handel.indexing(self.index)
            try :
                for pvals in self.table :
                    properties = {
                        (akeyalias[key].lower() if akeyalias else key.lower()) :\
                        (pvals[key].lower() if type(pvals[key]) == type("") else pvals[key]) \
                        for key in akey
                    }
                    self.handel.prope(pvals[ikey].lower(), properties, overturn)
                    if cry : pbar.update(1)
            except Exception as e:
                self.error(e, "PROPERTY-EXTRA")
            if cry : pbar.close()
        else : 
            print("Table is not available.")
            return

    def error(self, e, msg="") :
        print("ERROR {} : {}\n".format(msg, e))
        traceback.print_exc()
        self.table = None