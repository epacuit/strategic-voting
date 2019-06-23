
class Ranking():
    '''Ranking: a ranking of a set of candidates is a linear order of the candidates'''
    def __init__(self, cand_list):
        # cand_list is a list of candidates 
        
        # make sure that there are no duplicates
        assert len(list(set(cand_list))) == len(cand_list), "Cannot create a ranking when there are duplicates is the candidate ordering {}".format(cand_list)
        
        # a list of candidate records: (rank, candidate_name)
        self._ranking = list(enumerate(cand_list))
    
    @property
    def num_candidates(self):
        return len(self._ranking)
    
    @property
    def candidates(self):
        return set([cr[1] for cr in self._ranking])
    
    def _get_cr_by_cand(self, cand):      
        # get the candidate rank given the name of the candidate
        
        assert cand in self.candidates
        
        return [cr for cr in self._ranking if cr[1] == cand][0]

    def _get_cr_by_rank(self, rank):
        # get the candidate record by the rank
        
        assert rank >= 1 and rank <= len(list(self.candidates)) + 1
        
        return [cr for cr in self._ranking if cr[0] == rank - 1][0]

    def rank(self,cand):
        # return the rank of a candidate
        
        return self._get_cr_by_cand(cand)[0] + 1
    
    def cand(self,rank):
        # return the candidate positioned at rank
        return self._get_cr_by_rank(rank)[1]
        
    def __str__(self):
        # return the list of candidates as a string
        
        return " ".join([cr[1] for cr in self._ranking])
    
    def as_tuple(self):
        # return the ranking as a tuple 
        return tuple([cr[1] for cr in self._ranking])
    
    def __eq__(self, other): 
        if isinstance(other, self.__class__):
            return list(self._ranking) == list(other._ranking)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)        
        