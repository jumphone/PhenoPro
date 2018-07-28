import phenopro
import cPickle as pickle
from scipy.stats.mstats import ks_2samp
from numpy import array
import sys


class PhenoBayes_Data:
            def __init__(self,HPOs,Diseases,Genes,Diseases_all_Ps,Diseases_Genes):
                  self.HPOs=HPOs
                  self.Diseases=Diseases
                  self.Genes=Genes
                  self.Diseases_all_Ps=Diseases_all_Ps
                  self.Diseases_Genes=Diseases_Genes


class HPO_Class:
            def __init__(self, _id=[], _name=[], _alt_id=[],  _def=[], _comment=[], _synonym=[], _xref=[], _is_a=[],_alt_Hs={}):
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
                  self._alt_Hs= _alt_Hs


obo_file=sys.argv[1]
HPO_disease_gene_file=sys.argv[2]
output_dir=sys.argv[3]

phenobayes_withrc.loading(obo_file,HPO_disease_gene_file,output_dir)

HPO_disease_gene_demo='''
#Format: diseaseId<tab>gene-symbol<tab>gene-id(entrez)<tab>HPO-ID<tab>HPO-term-name
OMIM:614652     PDSS2   57107   HP:0002133      Status epilepticus
OMIM:614652     PDSS2   57107   HP:0000093      Proteinuria
OMIM:614652     PDSS2   57107   HP:0100704      Cortical visual impairment
OMIM:614652     PDSS2   57107   HP:0002151      Increased serum lactate
OMIM:614652     PDSS2   57107   HP:0000007      Autosomal recessive inheritance
OMIM:614652     PDSS2   57107   HP:0000100      Nephrotic syndrome
OMIM:614652     PDSS2   57107   HP:0001319      Neonatal hypotonia
OMIM:614652     PDSS2   57107   HP:0011968      Feeding difficulties
OMIM:614652     PDSS2   57107   HP:0000969      Edema
OMIM:614652     COQ2    27235   HP:0002133      Status epilepticus
OMIM:614652     COQ2    27235   HP:0000093      Proteinuria
OMIM:614652     COQ2    27235   HP:0100704      Cortical visual impairment
OMIM:614652     COQ2    27235   HP:0002151      Increased serum lactate
OMIM:614652     COQ2    27235   HP:0000007      Autosomal recessive inheritance
OMIM:614652     COQ2    27235   HP:0000100      Nephrotic syndrome
OMIM:614652     COQ2    27235   HP:0001319      Neonatal hypotonia
OMIM:614652     COQ2    27235   HP:0011968      Feeding difficulties
OMIM:614652     COQ2    27235   HP:0000969      Edema
OMIM:614508     RAD51   5888    HP:0001335      Bimanual synkinesia
OMIM:614508     RAD51   5888    HP:0000006      Autosomal dominant inheritance
OMIM:614508     RAD51   5888    HP:0003829      Incomplete penetrance
OMIM:614508     DCC     1630    HP:0001335      Bimanual synkinesia
OMIM:614508     DCC     1630    HP:0000006      Autosomal dominant inheritance
OMIM:614508     DCC     1630    HP:0003829      Incomplete penetrance
OMIM:300419     ZNF711  7552    HP:0001249      Intellectual disability
'''
 
