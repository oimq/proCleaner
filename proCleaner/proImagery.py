import requests
from jSona import jSona
import pprint
pp = pprint.pprint

class proImagery :
    def __init__(self, CONF_PATH) :
        self.jso  = jSona()
        self.headers = {'json':{'Content-Type':'application/json; charset=utf-8'}}
        self.config = self.jso.loadJson(CONF_PATH)['IMAGERY']
        self.lower  = {color['id']:color for color in self.jso.loadJson(self.config['COLOR']['PATH'])}
        
    def post(self, data) :
        return requests.post(url=self.post_url, data=self.jso.dumps(data, False), headers=self.headers['json'])

    def connect(self, addr, port) :
        self.url = "{}:{}/".format(addr, port)
        self.post_url = self.url
        temp_data = {'hello':'world'}
        res = self.post(temp_data)
        return 'success' in res.content.decode()
    
    def segcolor(self, img_url, img_name='default.jpg', options='-d') :
        self.post_url = self.url+'segcolor'
        data = {'path' : img_url, 'name' : img_name, 'options' : options} 
        res = self.post(data)
        return self.jso.loads(res.content.decode(), False)

    def ambcolor(self, colors, threshold=0.1) :
        colors = {color[0]:color[1] for color in colors}
        ambics = dict()
        for cid in colors : # brightgrayyellow
            if cid in self.lower :
                new_cid = self.lower[cid]['u']
                if new_cid in ambics : ambics[new_cid] += colors[cid]
                else                 : ambics[new_cid]  = colors[cid]
            else :
                if     cid in ambics : ambics[cid] += colors[cid]
                else                 : ambics[cid]  = colors[cid]
        return list(filter(lambda c : c[1]>threshold, ambics.items()))

    def start(self, img_url, labels=['shirt'], ambi=True, threshold=0.1, img_name='default.jpg', options='-d') :
        segments_and_colors = self.segcolor(img_url, img_name=img_name, options=options)
        if type(segments_and_colors) == type([]) :
            segments, colors = segments_and_colors[1], segments_and_colors[3]
            for sinx in range(len(segments)) :
                if set(labels)&set(self.config['LABEL'][''.join(segments[sinx].split()[:-1])]) and sinx<len(colors):
                    if ambi : return self.ambcolor(colors[sinx], threshold=threshold)
                    else    : return colors[sinx]
        return None