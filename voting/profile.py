
import itertools
from prettytable import *
from math import ceil

from voting.voter import Voter
from voting.ranking import Ranking

###
#Helper functions
###

def generate_linear_orderings(candidates): 
    # returns all linear orderings for a set of candidates
    
    return list(itertools.permutations(candidates))

def create_subsets(s, n): 
    # return all subsets of s of size n
    
    return list(itertools.combinations(s, n)) 


# Profiles
class Profile(object):
    
    def __init__(self, voter_list):
        
        assert len(voter_list) > 0, "Error: can only  create a profile with more than 0 voters"
        self._profile = voter_list
        self.voter_names = sorted([v.name for v in self._profile])
    
    @property
    def voters(self):
        return self._profile
    
    @property 
    def candidates(self):
        return self._profile[0].candidate_list()
    
    @property
    def num_candidates(self):
        return len(self.candidates)
    
    @property
    def all_rankings(self):
        return generate_linear_orderings(self.candidates)
    
    def get_voter(self, voter_name):
        
        # return the voter given the voter_name
        
        assert voter_name in self.voter_names, "Error: {} voter name is not in the profile: {}".format(voter_name, self.voter_names)
        
        voter = [v for v in self._profile if v.name == voter_name][0]
            
        return voter
    
    def support(self, c1, c2):

        # return the number of voters that rank c1 over c2
        _support  = 0
        for v in self._profile:
            if v.prefers(c1, c2):
                _support +=1
        return _support
    
    def create_new_profile(self, voter, new_ordering):
        # given a voter and a new ordering, create a new profile exactly like the existing one
        return Profile([v if v.name != voter.name else Voter(voter.name, ranking = Ranking(new_ordering)) 
                        for v in self._profile])
    
    def remove_candidates(self, cands):
        # create a new profile with the candidates removed
        
        if type(cands) == str: 
            cands = [cands]
            
        new_voter_list = [Voter(v.name,ranking=Ranking([_ for _ in str(v.ranking).split(' ') if _ not in cands])) for v in self.voters]
        return Profile(new_voter_list)
    
    def is_empty(self):
        # return true if some ranking is empty
        return any([len(v.ranking.candidates) == 0 for v in self._profile])
    
    def tally(self):

        # generate a tally  for all the candidates.   This is a dictionary associating with each voter, the 
        # margin of victory for that candidate over the other candidates. 

        return {c1: {c2: self.support(c1, c2) - self.support(c2, c1) for c2 in self.candidates if c2 != c1} 
                for c1 in self.candidates}

    def majority_prefers(self, c1, c2): 
        # return True if more voters rank c1 over c2 than c2 over c1

        return (self.support(c1, c2) - self.support(c2, c1)) > 0

    def num_rank(self, cand, level = 1):
        # returns the number of voters that rank cand at level
        
        return sum(v.rank_candidate(level) == cand for v in self._profile)

    def plurality_tally(self):
        #  return  the pluarlity tally
        
        return {c: self.num_rank(c, level=1) for c in self.candidates}

    def borda_scores(self):
        # return the Borda scores for each candidate
        
        borda_scores = {c:0 for c in self.candidates}
        num_candidates = len(self.candidates)
        for v in self._profile:
            borda_scores.update({c:((num_candidates - v.rank(c)) + borda_scores[c]) for c in self.candidates})
        return borda_scores
    
    def strict_maj_size(self):
        
        # return the size of  > 50% of the voters
        return len(self.voters)/2 + 1 if len(self.voters) % 2 == 0 else int(ceil(float(len(self.voters))/2))

    def display(self):
        tbl = PrettyTable()
        for v in self._profile:
            tbl.add_column(v.name, str(v.ranking).split(' '))
        print tbl

    def get_profile_string(self):
        tbl = PrettyTable()
        for v in self._profile:
            tbl.add_column(v.name, str(v.ranking).split(' '))
        return str(tbl)

    def as_dict(self): 
        return {v.name: v.ranking.as_tuple() for v in self._profile}
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return all([vs[0].name == vs[1].name and vs[0].ranking == vs[1].ranking for vs in zip(self._profile, 
                                                                                                   other._profile)])
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
# a pointed profile extends the Profile class
class PointedProfile(Profile):
    
    def __init__(self, voter_list, voter_name):
        super(PointedProfile, self).__init__(voter_list)
        
        assert voter_name in [v.name for v in voter_list], "Error: {} voter name is not in the list of voters".format(voter_name)
        self._voter_pos = [v.name for v in voter_list].index(voter_name)
        self._voter_name = voter_name
        
    @property
    def voter(self):
        return self._profile[self._voter_pos]
        
    def create_new_profile(self, new_ranking):
        # given a voter and a new ordering, create a new profile exactly like the existing one
        return PointedProfile([v if v.name != self._voter_name else Voter(self._voter_name,
                                                                          ranking = Ranking(new_ranking)) 
                               for v in self._profile], self._voter_name)    
###
#Helper functions
###

def create_profile(voter_names, rankings):
    # given voter names and a list of rankings, return a profile
    
    assert len(voter_names) == len(rankings), "Error: the number of voters doesn't match the number of rankings"
    return Profile([Voter(vr[0], ranking = Ranking(vr[1])) for vr in zip(voter_names, rankings)])

def create_pointed_profile(voter_names, rankings, voter):
    # given voter names and a list of rankings, return a profile
    
    assert len(voter_names) == len(rankings), "Error: the number of voters doesn't match the number of rankings"
    return PointedProfile([Voter(vr[0], ranking = Ranking(vr[1])) for vr in zip(voter_names, rankings)], voter)

def display_tally(tally):
    # display a nice table for a tally of a profile
    tbl = PrettyTable()
    candidates = sorted(tally.keys())
    
    tbl.add_column('',candidates)
    for c in candidates:
        tbl.add_column(c,[tally[c1][c] if c1 != c else 0 for c1 in candidates])
    print tbl