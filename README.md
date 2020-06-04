## proCleaner

##### Data pre-processing module

for installing and using, requirements are below : 

* tqdm : https://github.com/tqdm/tqdm

* elasticsearch : https://github.com/elastic/elasticsearch-py

* jSona : https://github.com/oimq/jSona

* handEl : https://github.com/oimq/handEl

***

### Installation

The pre-install resource is jSona, handEl

```code
pip3 install proCleaner-master/
```

***

### Projects

Before we started, notice that the proCleaner separates in five parts.

At those parts, please ignore the ImagesDownloader module.

Except this, proCleaner consisted by four parts. 



##### proImagery

* This module is dependant to flask and det2Clo module. We will share utilties later.

##### proMan
Make pre-processing materials

* make : Load dataset for store documents in elasticsearch

* proper : Store documents to elasticsearch

##### proSweeper
Do the pre-processing data from proMan's materials.

* start : Do the pre-processing

##### protools

* Most important part is that. first, understand the structures.
    * RULES : Entities that would be absorbed from main entity.
    * REFRS : Fields that refer the main field.
    * SIMLS : Pair or more numbers fields that be tolerated.
    * NULLS : Fields that okay to habe non-exists value.
    * REPLS : Define the converted keywords for each fields.
    * STOPS : Define the removal keywords for each fields.
    
```code
SWEEPER
    RULES
        field
            entity  : [entity0, ...]
    REFRS
        field
            refers  :[field0, ... or null], 
            FT      :boolean
            TOP     :boolean
    SIMLS   :[(entity0, entity1), ...]
    NULLS   :[field0, ...],
    REPLS
        field
            entity  :[string0, ...]
    STOPS
        field   :[string0, ...]
    TOOLS
        ES
            PREFIX_INDEX:string
    
```



***

### Examples

* Script
```python3

```
* Outputs
```python

```

***


### Notices

###### Unauthorized distribution and commercial use are strictly prohibited without the permission of the original author and the related module.