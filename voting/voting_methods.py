
from math import ceil
import numpy as np
import random

from voting.profile import generate_linear_orderings

# Voting methods

def plurality(profile):
    """Plurality"""

    plurality_tally = profile.plurality_tally()
    max_plurality_score = max(plurality_tally.values())
    
    return sorted([c for c in plurality_tally.keys() if plurality_tally[c] == max_plurality_score])

def majority(profile):
    '''Majority'''
    
    maj_size = profile.strict_maj_size()
    plurality_scores = profile.plurality_tally()
    maj_winner = [c for c in profile.candidates if c in plurality_scores.keys() and plurality_scores[c] >= maj_size]
    
    return sorted(maj_winner)

def borda(profile):
    """Borda"""
    
    candidates = profile.candidates
    borda_scores = profile.borda_scores()
    max_borda_score = max(borda_scores.values())
    
    return sorted([c for c in candidates if borda_scores[c] == max_borda_score])

def copeland(profile): 
    """Copeland"""
    
    tally  = profile.tally()
    candidates = tally.keys()
    copeland_scores = {c:len([1 for c2 in tally[c].keys() if tally[c][c2] > 0]) - len([1 for c2 in tally[c].keys() if tally[c][c2] < 0]) for c in candidates}
    max_copeland_score = max(copeland_scores.values())
    return sorted([c for c in candidates if copeland_scores[c] == max_copeland_score])


def maxmin(profile): 
    """MaxMin"""
    
    candidates = profile.candidates
    min_support = {c: min([profile.support(c,_c) for _c in candidates if _c != c]) for c in candidates}
    max_overall_support = max(min_support.values())
    return sorted([c for c in candidates if min_support[c] == max_overall_support])

def plurality_with_runoff(profile):
    """PluralityWRunoff"""

    plurality_tally = profile.plurality_tally()
    max_plurality_score = max(plurality_tally.values())
    first = [c for c in profile.candidates if plurality_tally[c] == max_plurality_score]
    if len(first) > 1:
        runoff_candidates = first
    else:
        second_plurality_score = list(reversed(sorted(plurality_tally.values())))[1]
        second = [c for c in profile.candidates if plurality_tally[c] == second_plurality_score]
        runoff_candidates = first + second
        
    runoff_profile = profile.remove_candidates([c for c in profile.candidates if c not in runoff_candidates])
    return plurality(runoff_profile)  

def hare(profile):
    """Hare"""
    
    candidates = profile.candidates
        
    plurality_scores = profile.plurality_tally()
    maj_winner = majority(profile)
    
    updated_profile = profile
    while len(maj_winner) == 0:
        min_plurality_score = min(plurality_scores.values())
        lowest_first_place_votes = [c for c in candidates if c in plurality_scores.keys() and plurality_scores[c] == min_plurality_score]
        
        # remove lowest plurality winners
        updated_profile = updated_profile.remove_candidates(lowest_first_place_votes)        
        if updated_profile.is_empty():
            maj_winner = sorted(lowest_first_place_votes)
        else:
            plurality_scores = updated_profile.plurality_tally()
            maj_winner = majority(updated_profile)
    return maj_winner

def coombs(profile):
    """Coombs"""
    
    maj_winner = majority(profile)
    
    updated_profile = profile
    while len(maj_winner) == 0:
        
        candidates, num_candidates = updated_profile.candidates, updated_profile.num_candidates
        last_place_scores = {c: updated_profile.num_rank(c,level=num_candidates) for c in candidates}
        max_last_place_score = max(last_place_scores.values())
        greatest_last_place_votes = [c for c in candidates if c in last_place_scores.keys() and last_place_scores[c] == max_last_place_score]
        
        # remove lowest plurality winners
        updated_profile = updated_profile.remove_candidates(greatest_last_place_votes)
        
        if updated_profile.is_empty():
            maj_winner = sorted(greatest_last_place_votes)
        else:
            maj_winner = majority(updated_profile)
    return maj_winner


def strict_nanson(profile):
    """StrictNanson"""
    
    borda_scores = profile.borda_scores()
    avg_borda_scores = np.mean(borda_scores.values())
    below_borda_avg_candidates = [c for c in profile.candidates if borda_scores[c] < avg_borda_scores]
    
    updated_profile = profile.remove_candidates(below_borda_avg_candidates)

    winners = updated_profile.candidates if updated_profile.num_candidates == 1 else []
    
    while len(winners) == 0: 
        
        borda_scores = updated_profile.borda_scores()
        avg_borda_scores = np.mean(borda_scores.values())
    
        below_borda_avg_candidates = [c for c in updated_profile.candidates if borda_scores[c] < avg_borda_scores]
        updated_profile = updated_profile.remove_candidates(below_borda_avg_candidates)
        
        if len(below_borda_avg_candidates) == 0:
            winners = sorted(updated_profile.candidates)
        elif updated_profile.num_candidates == 1:
            winners = updated_profile.candidates
        
    return winners 

def weak_nanson(profile):
    """WeakNanson"""
    
    borda_scores = profile.borda_scores()
    avg_borda_scores = np.mean(borda_scores.values())
    below_borda_avg_candidates = [c for c in profile.candidates if borda_scores[c] <= avg_borda_scores]
    
    updated_profile = profile.remove_candidates(below_borda_avg_candidates)

    winners = updated_profile.candidates if updated_profile.num_candidates == 1 else []
    
    if len(below_borda_avg_candidates) == profile.num_candidates: 
        winners = sorted(profile.candidates)
    else:
        while len(winners) == 0: 
        
            borda_scores = updated_profile.borda_scores()
            avg_borda_scores = np.mean(borda_scores.values())

            below_borda_avg_candidates = [c for c in updated_profile.candidates if borda_scores[c] <= avg_borda_scores]
        
            updated_profile = updated_profile.remove_candidates(below_borda_avg_candidates)

            if updated_profile.num_candidates  == 0:
                winners = sorted(below_borda_avg_candidates)
            elif updated_profile.num_candidates == 1:
                winners = updated_profile.candidates
        
    return winners 

def baldwin(profile):
    """Baldwin"""

    borda_scores = profile.borda_scores()
    candidates = profile.candidates
    min_borda_score = min(borda_scores.values())
    last_place_borda_scores = [c for c in candidates if c in borda_scores.keys() and borda_scores[c] == min_borda_score]
        
    # remove lowest plurality winners
    updated_profile = profile.remove_candidates(last_place_borda_scores)
    
    winners = list()
    if updated_profile.num_candidates == 0: 
        winners = sorted(last_place_borda_scores)
    
    while len(winners) == 0:
        
        borda_scores = updated_profile.borda_scores()
                
        candidates = updated_profile.candidates
        min_borda_score = min(borda_scores.values())
        last_place_borda_scores = [c for c in candidates if c in borda_scores.keys() and borda_scores[c] == min_borda_score]
           
        # remove lowest borda scores
        updated_profile = updated_profile.remove_candidates(last_place_borda_scores)
        
        if updated_profile.is_empty():
            winners = sorted(last_place_borda_scores)
        elif updated_profile.num_candidates == 1:
            winners = updated_profile.candidates  
    
    return winners 

def condorcet(profile):
    """Condorcet"""
    
    tally = profile.tally()
    cond_winner = filter(lambda c: all([tally[c][_] > 0 for _ in tally[c].keys()]), profile.candidates)
    return sorted(cond_winner) if len(cond_winner) > 0 else sorted(profile.candidates)



###
#Helper functions
###

def create_tie_breaker(lin_order):
    # given a linear ordering, create a tie breaker function
    
    return lambda cands: sorted(list(cands), key=lambda c: lin_order.index(c))[0]

def create_all_tie_breakers(candidate_names):
    
    # create all tie breakers for a set of candidates 
    # (each linear ordering gives a different tie-breaker)
    
    linear_orders = generate_linear_orderings(candidate_names)
    
    return [create_tie_breaker(lo) for lo in linear_orders]
    
def tie_breaker_cand_names(winners):
    
    # use the tie breaking that returns the candidate
    # whose name is alphabetically  earlies
    
    return sorted(winners)[0]

def tie_breaker_random(winners):
    
    # break time by  uniform probability over the winners
    return random.choice(winners)


def vms_to_str(voting_methods):
    # return a string of the voting method names
    return ','.join([_.__doc__ for _ in voting_methods])

def dom_to_str(dom):
    # return a string of the dominance tuple (weak_dom_name, strict_dom_name)
    return '|'.join(list(dom))

def str_to_dom(dom_str):
    
    return tuple(dom_str.split("|"))
    
def same_voting_methods_string(vms_str1, vms_str2):
    
    # test if the vothing methods strings are the same, e.g., 
    # the following should return true: "Borda", " Borda"; 
    # "Borda, Plurality", "Plurality, Borda"; and 
    # "Borda, Plurality, Plurality", "Plurality, Borda"
    vms1 = [vm_str.strip() for vm_str in vms_str1.split(",")]
    vms2 = [vm_str.strip() for vm_str in vms_str2.split(",")]
    
    return set(vms1) == set(vms2)
