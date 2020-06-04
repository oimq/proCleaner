TOOLS = {
    'SWEEPER':{
        'RULES':{
            "field": {
                'entity' : [],
            }
        },
        'REFRS':{
            "field"       : {
                'refers':[], 'fulltext':False},
        },
        'SIMLS':{
        },
        'NULLS':[
        ],
        'TOOLS':{
            "ES":{
                "PREFIX_INDEX":"elasticsearch_index"
            }
        },
        'REPLS':{
            "field": {
                "entity":[]
            },
        },
        'STOPS':{
            "field" : []
        },
    },
    'IMAGERY':{
        'LABEL':{
        },
        'COLOR':{
            'PATH':'color_dict_path'
        }
    }
}