guide = '''
안녕하세요. 이미지 다운로더입니다.
필요한 건 crawlCat 으로부터 저장된 JSON 형식의 파일과 해당 파일에서 어떤 필드가 이미지를 지목하고 있는 지 알려줘야 합니다.

이미지 파일 이름 형식은 다음과 같습니다.
{이미지 URL}.jpg  (단, /는 @로 대체되어 저장됩니다.)
image-field 는 이미지 주소가 있는 필드를 지정해야 합니다.

Option description
 *  -lp :   show only progress bar.
 *  -wt :   decide the wait times in seconds.

System arguments
<usage> <input> <output> <image-field> <option>

'''

import os
import sys
import traceback
import requests
from time import sleep
from random import randint as rint
import pprint
pp = pprint.pprint

from tqdm import tqdm
from jSona import jSona

class ImagesDownloader :
    def __init__(self, cpath) :
        self.jso = jSona()
        self.table = self.jso.loadJson(cpath)

    def error(self, e, msg="", ex=True) :
        print("ERROR {} : {}".format(msg, e))
        traceback.print_exc() 
        if ex : exit()

    def downloading(self, field, opath='./images/', cry=True, sleep_time=0) :
        if not os.path.exists(opath) : os.makedirs(opath)
        if cry : pbar = tqdm(total=len(self.table))
        try :
            for inx in range(len(self.table)) :
                if field not in self.table[inx] : raise Exception("There are no field : {}".format(field))
                for url in self.table[inx][field] :
                    try :
                        if 'jpg' in url :
                            r = requests.get(url)
                            if r.status_code == 200 :
                                save_path = os.path.join(opath, (url.replace('/', '@')+'.jpg')[-254:])
                                with open(save_path, 'wb') as openfile :
                                    openfile.write(r.content)
                            if sleep_time > 0 : sleep(rint(int(sleep_time*500), int(sleep_time*1500))*0.001)
                        else : continue
                    except Exception as e :
                        self.error(e, "DOWNLOADING", False)
                        continue
                if cry : pbar.update(1)
        except Exception as e :
            self.error(e, "READ", True)
        finally :
            if cry : pbar.close()
                    
if __name__=='__main__' :
    if set(["-help", "-h"]) & set(sys.argv) :     
        print(guide); exit()
    
    sleep_time = float(sys.argv[sys.argv.index('-wt')+1]) if '-wt' in sys.argv else 0 
    cry        = '-lp' in sys.argv
    print(sys.argv)
    data_path = sys.argv[1]
    idl = ImagesDownloader(data_path)
    idl.downloading(sys.argv[3], sys.argv[2], cry, sleep_time)