#python3.4
#jieba == 0.39
#nltk == 3.2.5 


class HPO_Class:
    def __init__(self, _id=[], _name=[], _alt_id=[],  _def=[], _comment=[], _synonym=[], _xref=[], _is_a=[],_alt_Hs={}, _chpo=[], _chpo_def=[]):
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



#########################################################################################################################################################

def dumping(obo_file, chpo_file, save_file_dir):
    import pickle

    HPOs={}
    _id=[];_name=[];_alt_id=[];_def=[];_comment=[];_synonym=[];_xref=[];_is_a=[];_chpo=[];_chpo_def=[]
    fi=open(obo_file)
    obo_terms=fi.read().split('[Term]')
    fi.close()
    alt_Hs={}
    for term in obo_terms:
        if 'id: ' in term:
            seq=term.split('\n')
            for one in seq:
                if ': ' in one:
                    if 'id: ' in one and 'alt_id: '  not in one:
                        _id.append(one.split(': ')[1])
                    if 'name: ' in one:
                        _name.append(one.split(': ')[1])
                    if 'alt_id: ' in one:
                        alt_Hs[one.split(': ')[1]] = _id[-1]
                        _alt_id.append(one.split(': ')[1])
                    if 'def: ' in one:
                        _def.append(one.split(': ')[1])
                    if 'comment: ' in one:
                        _comment.append(one.split(': ')[1])
                    if 'synonym: ' in one:
                        if '"' in one:
                            _synonym.append(one.split(': ')[1].split('"')[1])
                        else:
                            _synonym.append(one.split(': ')[1])
                    if 'xref: ' in one:
                        _xref.append(one.split(': ')[1])
                    if 'is_a: ' in one:
                        _is_a.append(one.split(': ')[1].split('!')[0].replace(' ',''))

            HPOs[_id[0]]=HPO_Class(_id,_name,_alt_id,_def,_comment,_synonym,_xref,_is_a,_chpo=[],_chpo_def=[])
            _id=[];_name=[];_alt_id=[];_def=[];_comment=[];_synonym=[];_xref=[];_is_a=[];_chpo=[];_chpo_def=[]


    # Alt_names  
    HPOs['HP:0000118']._alt_Hs=alt_Hs
    
    #CHPO
    fi=open(chpo_file)
    for line in fi:
        seq=line.rstrip().split('\t')
        hpoid=seq[0]
        flag=1
        if hpoid in HPOs:
            _id=hpoid
        elif hpoid in alt_Hs:
            #print(hpoid)
            _id=alt_Hs[hpoid]
        else:
            flag=0
        if flag==1:
            _chpo=seq[2]
            HPOs[_id]._chpo.append(_chpo)
            #print(HPOs[_id]._chpo)
            if len(seq)>=5:    
                _chpo_def=seq[4]
                #print(HPOs[_id]._chpo_def)
                HPOs[_id]._chpo_def.append(_chpo_def)
                #print(HPOs[_id]._chpo_def)
         
        



    #Find_father
    def find_father(_ori_id,_id):
        if  HPOs[_id]._name=='All':
            pass
        else:
            for one in HPOs[_id]._is_a:
                HPOs[_ori_id]._father.add(one)
                find_father(_ori_id,one)

    j=0
    for _id in HPOs:
        find_father(_id,_id)
        j=j+1;print(" Finding HPOs' ancestor nodes: "+str(j)+' HPOs ', end='\r')

    #Find_children
    print('')
    j=0
    for asHPO in HPOs:   
        for HPO in HPOs:
            if asHPO in HPOs[HPO]._father:
                HPOs[asHPO]._child_self.add(HPO)
            HPOs[asHPO]._child_self.add(asHPO) # add self
        j=j+1;print(" Finding HPOs' child nodes: "+str(j)+' HPOs ', end='\r')


    print('')
    fo=open(save_file_dir,'wb')
    data=HPOs
    pickle.dump(data,fo)
    fo.close()



#########################################################################################################################################################

def loading(data_file):
    import pickle
    fi=open(data_file,'rb')
    HPOs=pickle.load(fi)
    return HPOs



#########################################################################################################################################################

#def splitting(input_dir, HPOs, chpo_dic_dir,  split_punc_dir,  rm_en_dir, rm_cn_dir, rm_pro_dir, output_dir):
def splitting(input_dir, HPOs, chpo_dic_dir,  split_punc_dir,  rm_dir):
    
    import jieba
    import jieba.posseg as psg 
    import nltk 
    jieba.load_userdict(chpo_dic_dir)
    


    split_punc=set()
    fi=open(split_punc_dir)
    for line in fi:
        split_punc.add(line.rstrip())
    fi.close()


    words=open(input_dir).read().replace('\n','; ').replace('\r','; ')
    L=len(words)
    rmlist = open(rm_dir).read().rstrip().split('\n')

 
    #Txt2phrase
    phrases=[] 
    old=set()
    i=0
    tmp=0
    while i<len(words):
        word=words[i]
        if word in split_punc:
            phrase=words[tmp:i].strip()
            
            if phrase not in old:
                old.add(phrase)
                for one in rmlist:
                    phrase=phrase.replace(one,'')    
                if len(phrase)>0:        
                    phrases.append(phrase)  

            tmp=min(i+1,L-1)
        i+=1

    phrase=words[tmp:i].strip()

    if phrase not in old:
        old.add(phrase)
        for one in rmlist:
            phrase=phrase.replace(one,'')
        if len(phrase) > 0:
            phrases.append(phrase)
#    print(phrases )
   

        
    #print(phrases)
    #Split phrase

    def get_tag(sen):
        output=[]
        seq=sen.split(' ')
        for one in seq:
            try:
                output.append(nltk.pos_tag(nltk.word_tokenize(one))[0])
            except Exception as e:
                print('Warning!\tThe element is "'+one+'"')
                output.append('JJ')
        return output

    def select_words(line):
        line=line #.upper()
        #print(line)
        tags = get_tag(line.strip())
        #print(tags)
        tmp=[[]]
        tmp_jj=""
        flag=0
        tmp_jj_jj=""
        for one in tags:
            if  one[1] =='JJ' or 'JJ' in one[1]:
              if len(one[0])  <4 or len(one[0])>3 and one[0][-3:] != "ing":
                tmp_jj_jj=tmp_jj
                tmp_jj=one[0]

            elif (len(one[0])>3 and one[0][-3:]== "ing") or one[1] =='NN' or one[1] == 'NNS' or 'NN' in one[1]:
                if tmp_jj!='':
                    tmp[-1].append(tmp_jj)
                tmp[-1].append(one[0])
                tmp_jj_jj=tmp_jj
                tmp_jj=''
            elif one[1] =='CC' or one[1] =='IN' or one[1] =='TO':
                if tmp_jj!='':
                    if tmp_jj_jj !='':
                        tmp[-1].append(tmp_jj_jj)
                        tmp[-1].append(tmp_jj)
                    else:
                        tmp[-1].append(tmp_jj)

                tmp_jj=""
                tmp_jj_jj=""
                tmp.append([])
        if tmp_jj!='':
             if tmp_jj_jj !='':
                 tmp[-1].append(tmp_jj_jj)
                 tmp[-1].append(tmp_jj)
             else:
                 tmp[-1].append(tmp_jj)

        output=[]
        for one in tmp:
            if len(one)>0:
                output.append(' '.join(one))
        #print(output)
        return output




    def split_cn(phrase):
        seq=jieba.cut(phrase)
        return seq
    def split_en(phrase):
        seq=select_words(phrase)
        return seq

    #print(phrases)
    elements=[]
    old=set()
    for phrase in phrases:
        flag='en'
        for alpha in phrase:
            if ord(alpha)>255:
                flag='cn'
        if flag=='cn':
            out = split_cn(phrase)
            seq=[]
            seq.append(phrase)
            for one in out:
                if len(one)>1:
                    seq.append(one)
        else:
            seq = split_en(phrase)
            #print(seq)
        for element in seq:
            if element not in old:
                old.add(element)
                elements.append(element)
            
    return elements


#########################################################################################################################################################

def mapping(elements, mapping_list_dir, HPOs):

    mapping_list={}
    fi=open(mapping_list_dir)
    for line in fi:
        seq=line.rstrip().split('\t')
        if seq[0] not in mapping_list:
            mapping_list[seq[0]]=[seq[1]]
        else:
            if seq[1] not in mapping_list[seq[0]]:
                mapping_list[seq[0]].append(seq[1])
    fi.close()
   

    def wordscore(term1,term2):
        term1=term1.replace('','').replace('\r','').replace('\n','').lower()
        term2=term2.replace('','').replace('\r','').replace('\n','').lower()
        overlap=[]
        j_cutoff=int(min(max(len(term1)/2,1),5))
        i=0
        tmp_end=0
        while i < len(term1):
            j=j_cutoff
            tmp=[0]
            tmp_j=[0]
            tmp_end_lst={}
            tmp_end_lst[0]=[0]
            while j < len(term1)-i+1:
                if term1[i:i+j] in term2[tmp_end:]:
                    flag=0
                    if flag!=1:
                        tmp_j.append(j)
                        tmp.append(j/float(i+1))
                        try:
                            tmp_end_lst[j].append(term2.find(term1[i:i+j]))
                        except Exception as e:
                            tmp_end_lst[j]=[term2.find(term1[i:i+j])]
                j=j+1
            overlap.append(max(tmp))
            i=i+max(tmp_j)+1
            tmp_end=tmp_end_lst[max(tmp_j)][0]+max(tmp_j)+1
            wscore=sum(overlap)/float(len(term1)+len(term2)-sum(overlap))
            if wscore<0.2:
                wscore=0
        return wscore

  
   

    def compareterm(term1,term2):
        words1=term1.lower().replace('"','').split(' ')
        words2=term2.lower().replace('"','').split(' ')
        score={}
        for word1 in words1:
            tmp_score=[]
            tmp_word={}
            for word2 in words2:
                wscore=wordscore(word1,word2)
                tmp_score.append(wscore)
                tmp_word[wscore]=word2
            if max(tmp_score) >= 0:
                score[word1]=[max(tmp_score),tmp_word[max(tmp_score)]]
        SCORE=sum( [ score[w][0] for w in score])
        #if SCORE  < float(len(term2))/3:
         #   SCORE=0
          
        return SCORE
 
    def compareterm_cn(term1,term2):
        #term1=term1.lower()
        #term2=term2.lower()
        score=0
        for word1 in term1:
            if word1 in term2:
                score+=1
        score=score + 1.0/float(int(len(term2)/3.0)+1)
        if score >=2 and score >= float(len(term2))/3:
            return score
        else:
            return 0


     


    def interpreting(keywords):
        keywords=keywords.lower()
        if keywords=='':
            return ['None']
        score=[]
        for HPO in HPOs:
            tmp=[0]
            check_list=HPOs[HPO]._name+HPOs[HPO]._synonym
            for term in check_list:
                tmp.append(compareterm(keywords,term.lower()))
            score.append([max(tmp),HPO])
        score.sort(reverse=True)
        return score

    def interpreting_cn(keywords):
        keywords=keywords.lower()
        if keywords=='':
            return ['None']
        score=[]
        for HPO in HPOs:
            tmp=[0]
            check_list=HPOs[HPO]._chpo
            for term in check_list:
                tmp.append(compareterm_cn(keywords,term))
            if 'HP:0000118' in HPOs[HPO]._father:
                score.append([max(tmp),HPO])
        score.sort(reverse=True)
        #if keywords=='语言发育障碍':
        #    print(score)
        
        return score


    def purifyHPO(score):
        output=[]
        final_output=[]
        if score[0][0]<0.5:
            ok_final_output=['None']
        else:
            tmp=score[0][0]
            i=0
            ori_output=[]
            while score[i][0]==tmp:
                ori_output.append(score[i][1])
                i=i+1
            child_group=set()
            for HPO in ori_output:
                this_HPO=set()
                this_HPO.add(HPO)
                tmp = HPOs[HPO]._child_self - this_HPO
                child_group=child_group | tmp
            for one in ori_output:
                if one not in child_group:
                    output.append(one)

            limit_length=1

            if len(output)>limit_length:


                tmp=[]
                for one in output:
                    father_len=len(HPOs[one]._father)
                    tmp.append([father_len/float(father_len+len(HPOs[one]._child_self)),one])
                    #tmp.append([father_len/float(father_len),one])
                tmp.sort()

            
                for one in tmp[0:limit_length]:                  
                    final_output.append(one[1])
                
                

                if len(tmp)>limit_length:
                    iii=limit_length
                    while iii<len(tmp) and tmp[iii][0]==tmp[limit_length-1][0]:
                        final_output.append(tmp[iii][1])
                        iii+=1
                    limit_length=iii
                    
                #print(final_output)

 
                
                if len(tmp)>limit_length:
                    combined_father=set()
                    this_HPO=set()
                
                    this_HPO.add(tmp[limit_length][1])
                    combined_father=HPOs[tmp[limit_length][1]]._father | this_HPO
                    for one in tmp[limit_length:]:
                        this_HPO=set()
                        this_HPO.add(one[1])
                        combined_father=combined_father & (HPOs[one[1]]._father | this_HPO)
                    tmptmp=[]
                    for one in combined_father:
                        tmptmp.append([len(HPOs[one]._father),one])
                    tmptmp.sort()
                ####################20171108
                    try:
                        final_output.append(tmptmp[-1][1])
                    except Exception as e:
                        pass
                tmp=[]
                for one in  final_output:
                   if 'HP:0000118' not in HPOs[one]._child_self:
                       tmp.append(one)
                final_output=tmp
            else:
                final_output=output

            ok_final_output=[]
            for one in final_output:
                 if 'HP:0000118' in HPOs[one]._father:
                     ok_final_output.append(one)
            if len(ok_final_output)==0:
                ok_final_output=['None']

        return ok_final_output



    


    def mapping_en(element):
        score= interpreting(element)
        hpos=purifyHPO(score)
        return hpos


    def mapping_cn(element):
        score= interpreting_cn(element)
        hpos=purifyHPO(score)
        return hpos



    alt_Hs=HPOs['HP:0000118']._alt_Hs
    mapped_hpos=[]
    for element in elements:
        if element.upper() in mapping_list:
            mapped_hpos.append(mapping_list[element])
        elif element.upper() in HPOs:
            mapped_hpos.append([element])
        elif element.upper() in alt_Hs:
            mapped_hpos.append([alt_Hs[element]]) 
        else:
            flag='en'
            for alpha in element:
                if ord(alpha)>255:
                    flag='cn'
            if flag=='en':
                if len(element)<=2:
                    mapped_hpos.append(['None'])
                else:
                    hpos=mapping_en(element)
                    mapped_hpos.append(hpos)
            else:
                hpos=mapping_cn(element)
                mapped_hpos.append(hpos)

#    i=1 
#    while i<len(elements):
#        print(elements[i])
#        print(mapped_hpos[i])

#       i+=1
    return mapped_hpos




















