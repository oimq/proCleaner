import os
import traceback
import json
from tqdm import tqdm
from datetime import datetime
import pprint
pp = pprint.pprint

from handEl import handEl

class proSweeper() :
    def __init__(self, host, port, cpath, CONF_PATH) :
        self.he             = handEl(host, port)
        self.cpath          = cpath
        self.table          = self.loadJson(cpath) if cpath else None
        self.config         = self.loadJson(os.path.join(CONF_PATH, 'proConfig.json'))['SWEEPER']
        self.dirty_indices  = list()
        self.clean_items    = list()
        self.statime        = datetime.now()
        self.endtime        = datetime.now()

    def __str__(self) :
        sta = self.statime
        end = self.endtime
        delta = end-sta
        reports_text = \
            "\n\n** Reports **\n\n - Total items : {}\n".format(len(self.total_items)) +\
            " - Dirty items : {}\n".format(len(self.dirty_indices)) +\
            " - Clean items : {}\n".format(len(self.clean_items)) +\
            " - Clean/Total Percentages : {:.3f}% \n".format(len(self.clean_items)/len(self.total_items)*100) +\
            " - Cleanning Start : {}. {}. {}. {} : {} : {}.{}.\n".format(
                sta.year, sta.month, sta.day, sta.hour, sta.minute, sta.second, sta.microsecond) +\
            " - Cleanning End   : {}. {}. {}. {} : {} : {}.{}.\n".format(
                end.year, end.month, end.day, end.hour, end.minute, end.second, end.microsecond) +\
            " - Time Deltas : {} days, {}.{} seconds\n".format(
                delta.days, delta.seconds, delta.microseconds)
        print("\n\n");pp(self.dirty_indices)
        print("\n\n");pp(self.total_items)
        print("\n\n");pp(self.clean_items)
        return reports_text

    def picking(self, item, index) :
        rem = dict()
        for ikey in item :
            if ikey in self.config['NULLS']           : continue # Apply nulls
            if type(item[ikey]) == type("") : rem[ikey] = item[ikey]; continue
            if len(item[ikey]) == 0         : rem[ikey] = 'None'
        if rem  : rem['index']=index;  self.dirty_indices.append(rem)
        else    : item['index']=index; self.clean_items.append(item)

    def similaring(self, prop, fprop) :
        if len(fprop) >= 2 :
            for sim in self.config['SIMLS'][prop] :
                if len(set(sim)&set(fprop))==len(fprop) : return fprop
            fprop = "Ambiguous"
            return fprop
        else : return fprop

    def ruling(self, prop, fprop) :
        absorbs = set()
        for upper in self.config['RULES'][prop] :  
            for lower in self.config['RULES'][prop][upper] :
                if len(set([upper, lower])&set(fprop)) >= 2 :
                    absorbs.add(lower)
        for absorb in absorbs : fprop.remove(absorb)
        return fprop

    # find property by contents from item[ref]
    def cleaning(self, prop, refs, item, fuzziness=0) :
        if not refs['refers'] : return list(set(item[prop])) if type(item[prop]) == type([]) else [item[prop]]
        dusts = [item[ref] for ref in refs['refers']]# if type(refs)==type({}) else item[refs]
        self.he.indexing(self.config['TOOLS']['ES']['PREFIX_INDEX']+prop)
        
        for dust in dusts :
            if refs['FT'] :   finedusts = dust
            else          :   finedusts = self.he.tokenize(dust)
            if refs['TOP'] : 
                cleans = list()
                for fdust in finedusts :
                    if self.he.doc(fdust)                        : cleans.append((self.he.result['match_ids'][0], 10))
                    if self.he.match(fdust, fuzziness=fuzziness) : cleans.append((self.he.result['match_ids'][0], self.he.result['match_sco']))
                return [sorted(cleans, key=lambda c : c[1])[-1][0]] if len(cleans) > 0 else []
            else :
                cleans = set()
                for fdust in finedusts :
                    if fdust :
                        if refs['FT'] : 
                            for fd_token in fdust.split() :
                                if self.he.doc(fd_token)  : cleans=cleans.union(self.he.result['match_ids'])
                        elif self.he.doc(fdust)           : cleans=cleans.union(self.he.result['match_ids'])
                        if self.he.match(fdust, fuzziness=fuzziness) : cleans=cleans.union(self.he.result['match_ids'])
            return list(cleans)

    # Remove the stop words
    def stoping(self, prop, words) :
        if type(words) != type([]) : words = [words]
        stoped = list()
        for inx in range(len(words)) :
            for stop in self.config['STOPS'][prop] :
                while stop in words[inx] : 
                    words[inx] = words[inx].replace(stop, "")
            if words[inx] : stoped.append(words[inx])
        return stoped

    # Replace the words
    def replacing(self, prop, words) :
        if type(words) != type([]) : words = [words]
        for rep in self.config['REPLS'][prop] :
            for inx in range(len(words)) : 
                for chg in self.config['REPLS'][prop][rep] :
                    if chg in words[inx] : words[inx] = rep; break
        return words
    
    # Remove the dupcators
    def remduping(self, items) :
        for ikey in items :
            if type(items[ikey]) == type([]) :
                items[ikey] = list(set(items[ikey]))
        return items

    def start(self, cry=True, clean_path=None, dirty_path=None) :
        print("\nCleansing start, refers are belows\n{}.\n".format(list(self.config['REFRS'].keys())))
        try :
            if not self.table : raise Exception("There are no data!")
            if cry : pbar = tqdm(total=len(self.table)) 
            self.statime = datetime.now()
            for tinx in range(len(self.table)) :
                filtered = dict() 
                self.table[tinx] = self.remduping(self.table[tinx])                                                      # Apply remduping
                for prop in self.config['REPLS'] : self.table[tinx][prop] = self.replacing(prop, self.table[tinx][prop]) # Apply replacing
                for prop in self.config['STOPS'] : self.table[tinx][prop] = self.stoping(prop, self.table[tinx][prop])   # Apply stoping
                for prop in self.config['REFRS'] : # Cleansing properties, prop is a reference's key
                    filtered[prop] = self.cleaning(prop, self.config['REFRS'][prop], self.table[tinx])                   # Apply filtering
                for prop in self.config['RULES'] : filtered[prop] = self.ruling(prop, filtered[prop])                    # Apply rules
                for prop in self.config['SIMLS'] : filtered[prop] = self.similaring(prop, filtered[prop])                # Apply similars
                self.picking(filtered, tinx)   
                if cry : pbar.update(1)
            if cry : pbar.close()
            self.endtime = datetime.now()
        except Exception as e :
            self.error(e, "START", True)
        finally :
            self.saveClean(clean_path) if clean_path else self.saveClean(os.path.join("/".join(self.cpath.split('/')[:-1]),"cleans.json"))
            self.saveDirty(dirty_path) if dirty_path else self.saveDirty(os.path.join("/".join(self.cpath.split('/')[:-1]),"dirties.json"))

    def error(self, e, msg="", ex=False) :
        print("ERROR {} : {}".format(msg, e))
        traceback.print_exc() 
        if ex : exit()

    def loadJson(self, cpath) :
        try :
            with open(cpath) as openfile :
                return json.load(openfile)
            print("\Load success. {}\n".format(cpath))
        except Exception as e :
            self.error(e, "LOAD JSON")

    def saveClean(self, cpath) :
        try :
            with open(cpath, 'w') as openfile :
                json.dump(self.clean_items, openfile)
            print("\nSave cleaned data success. {}\n".format(cpath))
        except Exception as e :
            self.error(e, "SAVE JSON")

    def saveDirty(self, cpath) :
        try :
            with open(cpath, 'w') as openfile :
                json.dump(self.dirty_indices, openfile)
            print("\nSave dirty indices success. {}\n".format(cpath))
        except Exception as e :
            self.error(e, "SAVE JSON")