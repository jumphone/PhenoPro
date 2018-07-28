import cPickle as pickle
import sys
import phenopro
class PhenoBayes_Data:
            def __init__(self,HPOs,Diseases,Genes,Diseases_all_Ps):
                  self.HPOs=HPOs
                  self.Diseases=Diseases
                  self.Genes=Genes
                  self.Diseases_all_Ps=Diseases_all_Ps


class HPO_Class:
            def __init__(self, _id=[], _name=[], _alt_id=[],  _def=[], _comment=[], _synonym=[], _xref=[], _is_a=[]):
                  self._id = _id
                  self._name = _name
                  self._alt_id = _alt_id
                  self._def = _def
                  self._comment = _comment
                  self._synonym = _synonym
                  self._xref = _xref
                  self._is_a = _is_a
                  self._father=set()
                  self._disease=set()
                  self._child_self=set()


fdata = open('./PhenoproData.pk')
data = pickle.load(fdata)
fdata.close()

HPO_root=set()
HPO_root.add('HP:0000118')

fi=open(sys.argv[1])
given_HPOs=set()
for line in fi:
    if line[0]!='#':
        seq=line.replace('\n','')
        given_HPOs.add(seq)



result=phenopro.Ranked_Score_Disease_Pheno(given_HPOs,data)

fo=open(sys.argv[2],'w')
for one in result:
        fo.write(one[1]+'\t'+str(one[0])+'\t'+one[3]+'\t'+one[2]+'\n')



