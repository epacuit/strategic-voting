# Strategic Voting Under Uncertainty about the Voting Method

This repo contains code that was used in the paper:

Wes Holliday and Eric Pacuit, 2019, "Strategic Voting Under Uncertainty About the Voting Method," in *Proceedings of TARK 2019*, Toulouse. 

## Requirements


- preflibtools: https://github.com/nmattei/PrefLib-Tools (to generate profiles, a fork of these Python scripts is contained in this repo) 
- jupyter (to  run the notebooks)
- numpy (only used for simple calculations)
- pandas (used from some simple data manipulation)
- pickle (for storing instances of manipulation)
- seaborn: https://seaborn.pydata.org/index.html (for producing graphs)
- prettytable: https://pypi.org/project/PrettyTable/ (to display voting scenarios)

## Contents

1. voting: a directory containing the scripts that implement the various voting methods 
  * ranking.py: definition of the Ranking class 
  * voter.py: definition of the Voter class 
  * profile.py: definition of the Profile class and some helper functions
  * voting_methods.py: definition of various voting methods and some help functions
2. peflibtools: A fork of the Pythoon scripts from https://github.com/nmattei/PrefLib-Tools
3. VotingScripts: Jupyter notebook that illustrates the scripts implementing the above voting scripts. **Note**: Uncomment the relevant %%writefile commands to overwrite the files in the voting directory.  
4. CreateReducedProfiles: Jupyter notebook to create profiles of various sizes
5. FindStrategicInstances: Jupyter notebook to create the heatmaps for pairs of voting methods
6. AsymptoticAnalysis: Jupyter notebook searching larger voting situations (more than 3 candidates/more than 7 voters), where profiles are sampled  using the impartial culture model.

