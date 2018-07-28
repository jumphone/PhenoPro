import txt2hpo, sys
import  pickle

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


obo_file='src/hp.obo'  #sys.argv[1]
chpo_file='src/chpo_total.txt'  #sys.argv[2]
save_file_dir='src/HPOdata.pk'  #sys.argv[3]

txt2hpo.dumping( obo_file, chpo_file, save_file_dir )



