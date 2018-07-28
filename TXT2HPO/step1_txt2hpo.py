import txt2hpo, sys
import  pickle
import os


class HPO_Class:
    def __init__(self, _id=[], _name=[], _alt_id=[],  _def=[], _comment=[], _synonym=[], _xref=[], _is_a=[],_alt_Hs={}, _chpo=[],_chpo_def=[]):
        self._id = _id
        self._name = _name
        self._alt_id = _alt_id
        self._def = _def
        self._comment = _comment
        self._synonym = _synonym
        self._xref = _xref
        self._is_a = _is_a
        self._father=set()
        self._child_self=set()
        self._alt_Hs= _alt_Hs
        self._chpo=_chpo
        self._chpo_def=_chpo_def

#from CONFIG import *

#REALPATH = os.path.realpath(__file__).replace(__file__,'')

REALPATH='/home/zhangfeng/TXT2HPO/'

HPOs=txt2hpo.loading(REALPATH+'/src/HPOdata.pk')

input_dir=sys.argv[1]
chpo_dic_dir=REALPATH+'/src/chpo.txt'
split_punc_dir=REALPATH+'src/split_punc.txt'
rm_dir=REALPATH+'src/rmwords.txt'
rm_pro_dir=REALPATH+'src/rmwords_pro.txt'
output_dir=sys.argv[2]
mapping_list_dir=REALPATH+'src/mapping_list.txt'


elements=txt2hpo.splitting(input_dir, HPOs, chpo_dic_dir, split_punc_dir, rm_dir)
hpos=txt2hpo.mapping(elements, mapping_list_dir, HPOs)


fo=open(output_dir,'w')
fo.write('#Givern_term\n')
fo.write(open(input_dir).read().replace('\n','')+'\n')
fo.write('#Interpreted_term\tHPOs\n')
old=set()
given_hpos=[]
i=0
while i<len(elements):
    if hpos[i] != ['None']:
        fo.write(elements[i]+'\t'+','.join(hpos[i])+'\n')
        for one in hpos[i]:
           if one not in old:
               old.add(one)
               given_hpos.append([one,i])
    i+=1
        

fo.write('#Given_HPO\tHPO_name\tHPO_name_cn\tElement\n')
i=0
while i<len(given_hpos):
    hpo=given_hpos[i][0]
    element=elements[given_hpos[i][1]]
    if len(HPOs[hpo]._chpo )>0:
        chpo=HPOs[hpo]._chpo[0]
    else:
        chpo='无'
    fo.write(hpo+'\t'+HPOs[hpo]._name[0]+'\t'+chpo+'\t'+element+'\n')
    
        
    i+=1





