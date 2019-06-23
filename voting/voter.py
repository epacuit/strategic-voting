
class Voter():
    def __init__(self, name, ranking = None):
        
        self.name = name
        self.ranking = ranking
        
    def candidate_list(self):
        return list(self.ranking.candidates)
    
    # voter preferences 
    def prefers(self, c1, c2):
        # return True if c1 is ranked above c2
        
        # check that candidates are in the rankings
        assert c1 in self.ranking.candidates, "Error: {} not in the voters ranking {}".format(c1, self.ranking)
        assert c2 in self.ranking.candidates, "Error: {} not in the voters ranking {}".format(c2, self.ranking)
        
        # lower rank number means the candidate is ranked higher
        return self.ranking.rank(c1) < self.ranking.rank(c2)

    def wprefers(self, c1, c2):         
        # return True if c1 is ranked above c2 or c1 == c2
        
        # check that candidates are in the rankings
        assert c1 in self.ranking.candidates, "Error: {} not in the voters ranking {}".format(c1, self.ranking)
        assert c2 in self.ranking.candidates, "Error: {} not in the voters ranking {}".format(c2, self.ranking)
        
        return c1 == c2 or self.ranking.rank(c1) < self.ranking.rank(c2)

    def rank_candidate(self, rank):
        # return the candidate at position rank
        
        return self.ranking.cand(rank)
    
    def rank(self, candidate):
        # return the ranking of candidate
        
        return self.ranking.rank(candidate)
    
    def first(self, cs = None):
        # return the first ranked candidate from a list of candidates cs (or all if cs is None)
        if cs is None:
            first = self.rank_candidate(1)
        else:
            first = min(cs, key = lambda c: self.rank(c))
        return first

    def last(self, cs = None):
        # return the last ranked candidate from a list of candidates cs (or all if cs is None)
        if cs is None:
            last = self.rank_candidate(self.ranking.num_candidates)
        else:
            last = max(cs, key = lambda c: self.rank(c))
        return last

    # set preferences
    def AAdom(self, c1s, c2s):         
        # return True if every candidate in c1s is weakly preferred to every  candidate in c2s
        
        # check if all candidates are ranked
        assert set(c1s).union(set(c2s)).issubset(self.ranking.candidates), "Error: candidates in the sets {} and {} are not ranked".format(c1s, c2s)
        return all([all([self.wprefers(c1, c2) for c2 in c2s]) for c1 in c1s])
    
    def strong_dom(self, c1s, c2s):         
        # return True if AAdom(c1s, c2s) and there is a candidate in c1s that is strictly preferred to every  candidate in c2s
        
        # check if all candidates are ranked
        assert set(c1s).union(set(c2s)).issubset(self.ranking.candidates), "Error: candidates in the sets {} and {} are not ranked".format(c1s, c2s)
        
        return self.AAdom(c1s, c2s) and any([all([self.prefers(c1, c2) for c2 in c2s]) for c1 in c1s])

    def weak_dom(self, c1s, c2s):         
        # return True if AAdom(c1s, c2s) and there is a candidate in c1s that is strictly preferred to every  candidate in c2s
        
        # check if all candidates are ranked
        assert set(c1s).union(set(c2s)).issubset(self.ranking.candidates), "Error: candidates in the sets {} and {} are not ranked".format(c1s, c2s)
        
        return self.AAdom(c1s, c2s) and any([any([self.prefers(c1, c2) for c2 in c2s]) for c1 in c1s])

    def optimist_prefers(self, c1s, c2s):
        # return True if the best candidate from c1s is strictly  preferred to the best candidate from c2s
        
        # check if all candidates are ranked
        assert set(c1s).union(set(c2s)).issubset(self.ranking.candidates), "Error: candidates in the sets {} and {} are not ranked".format(c1s, c2s)
        
        return self.prefers(self.first(c1s),self.first(c2s))

    def weak_optimist_prefers(self, c1s, c2s):
        # return True if the best candidate from c1s is weakly preferred to the best candidate from c2s
        
        # check if all candidates are ranked
        assert set(c1s).union(set(c2s)).issubset(self.ranking.candidates), "Error: candidates in the sets {} and {} are not ranked".format(c1s, c2s)
        
        return self.wprefers(self.first(c1s),self.first(c2s))

    def pessimist_prefers(self, c1s, c2s):
        # return True if the worst candidate from c1s is strictly  preferred to the worst candidate from c2s
        
        # check if all candidates are ranked
        assert set(c1s).union(set(c2s)).issubset(self.ranking.candidates), "Error: candidates in the sets {} and {} are not ranked".format(c1s, c2s)
        
        return self.prefers(self.last(c1s),self.last(c2s))

    def weak_pessimist_prefers(self, c1s, c2s):
        # return True if the worst candidate from c1s is weakly preferred to the worst candidate from c2s
        
        # check if all candidates are ranked
        assert set(c1s).union(set(c2s)).issubset(self.ranking.candidates), "Error: candidates in the sets {} and {} are not ranked".format(c1s, c2s)
        
        return self.wprefers(self.last(c1s),self.last(c2s))

    # dominance notions comparing collections of winning sets
    def sure_dominance(self, winning_set1, winning_set2, dom):
        
        # return True if winning_set1 surely dominantes winning_set2 using dom as the dominance notion
        assert len(winning_set1) == len(winning_set2), "Can only apply sure dominance to winning sets of the same size: {}, {}".format(winning_set1, winning_set2)
        
        return all([dom(ws[0], ws[1]) for ws in zip(winning_set1, winning_set2)])

    def safe_dominance(self, winning_set1, winning_set2, wdom, dom):
        
        # return True if winning_set1 safely dominantes winning_set2 using
        # wdom as the weak dominance notion and dom as the dominance notion
        assert len(winning_set1) == len(winning_set2), "Can only apply apply dominance to winning sets of the same size: {}, {}".format(winning_set1, winning_set2)
        
        weak_pref = all([wdom(ws[0], ws[1]) for ws in zip(winning_set1, winning_set2)])
        strict_pref = any([dom(ws[0], ws[1]) for ws in zip(winning_set1, winning_set2)])

        return weak_pref and strict_pref

    def expected_dominance(self, winning_set1, winning_set2, dom):
        
        # return True if winning_set1 expected dominantes winning_set2 using
        # dom as the dominance notion
        assert len(winning_set1) == len(winning_set2), "Can only apply expected dominance to winning sets of the same size: {}, {}".format(winning_set1, winning_set2)
        
        better_outcomes = [1 for ws in zip(winning_set1, winning_set2) if dom(ws[0], ws[1])]
        worse_outcomes = [1 for ws in zip(winning_set1, winning_set2) if dom(ws[1], ws[0])]

        return len(better_outcomes) > len(worse_outcomes)

    # stochastic dominance/probabilities of candidates givine winning sets
    def probability(self, winning_sets, candidates):
        
        # return a dictionary associating the probability that a candidate will win 
        num_methods = len(winning_sets)
        return {c: float(1)/float(num_methods) * sum([float(1)/len(ws) for ws in winning_sets if c in ws]) for c in candidates}


    def prob(self, cand, winning_sets, candidates):
        # return a the probability of the candidate chosen as the winner
        
        assert cand in candidates, "{} must be in the set {}".format(cand, candidates)
        return self.probability(winning_sets, candidates)[cand]

        
    def weak_stochastic_dominance(self, winning_set1, winning_set2, candidates):
        
        # return True if winning_set1 weak stochastic dominantes winning_set2 
        
        assert len(winning_set1) == len(winning_set2), "Can only apply weak stochastic dominance to winning sets of the same size: {}, {}".format(winning_set1, winning_set2)
        
        num_candidates = len(candidates)
        ranks = range(num_candidates, 0, -1)
        
        ws1_probs = self.probability(winning_set1, candidates)
        ws2_probs = self.probability(winning_set2, candidates)

        candidate_sets = [[voter.rank_candidate(r)  for r in ranks[_:len(ranks)+1]] for _ in range(0,len(ranks))]

        candidate_probs_1 =  [sum([ws1_probs[c] for c in _cands]) for _cands in candidate_sets]
        candidate_probs_2 =  [sum([ws2_probs[c] for c in _cands]) for _cands in candidate_sets]

        return all([p[0] >= p[1] for p in zip(candidate_probs_1, candidate_probs_2)])    
    
    def stochastic_dominance(self, winning_set1, winning_set2, candidates):
        
        # return True if winning_set1  stochastic dominantes winning_set2 
        
        assert len(winning_set1) == len(winning_set2), "Can only apply stochastic dominance to winning sets of the same size: {}, {}".format(winning_set1, winning_set2)
        
        num_candidates = len(candidates)
        ranks = range(num_candidates, 0, -1)
        
        ws1_probs = self.probability(winning_set1, candidates)
        ws2_probs = self.probability(winning_set2, candidates)

        candidate_sets = [[self.rank_candidate(r)  for r in ranks[_:len(ranks)+1]] for _ in range(0,len(ranks))]

        candidate_probs_1 =  [sum([ws1_probs[c] for c in _cands]) for _cands in candidate_sets]
        candidate_probs_2 =  [sum([ws2_probs[c] for c in _cands]) for _cands in candidate_sets]

        return all([p[0] > p[1] for p in zip(candidate_probs_1, candidate_probs_2)]) 
