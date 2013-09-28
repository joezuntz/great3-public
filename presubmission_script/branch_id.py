experiments = ['control', 'real_galaxy', 'variable_psf', 'multiepoch', 'full']
observation_types = ['ground', 'space']
shear_types = ['constant', 'variable']

# Generate a regular expression that will match any branch name, such as
# control-ground-constant or variable_psf/space/variable, as well as a list of branch names
# delineated with hyphens.
branch_regex_names = []
branch_names = []
for exp in experiments:
    for otype in observation_types:
        for stype in shear_types:
            branch_regex_names.append(exp+'.'+otype+'.'+stype)
            branch_names.append(exp+'-'+otype+'-'+stype)
import re
branch_regex=re.compile('|'.join(branch_regex_names))

def formatted_branch_name(branch):
    """
    Takes a branch name which may be delineated by eg '/' (if it's a subdirectory structure),
    and turns it into a hyphen-delinated version of the same string.
    """
    for exp in experiments:
        if exp in branch:
            for otype in observation_types:
                if otype in branch:
                    for stype in shear_types:
                        if stype in branch:
                            return exp+'-'+otype+'-'+stype
    raise RuntimeError('Branch %s does not appear to be a valid branch name--please pass one of '
                         '[%s] with the command-line option -b.'%(branch, ', '.join(branch_names)))

# Subfield offsets for the variable branches.  Note that this section of code will change with 
# each new simulation release!
x_offset = {'control-ground-variable': 
                    [0, 4, 0, 6, 5, 3, 3, 1, 4, 3, 1, 3, 4, 0, 4, 6, 6, 1, 3, 2, 0, 1, 3, 0, 5, 
                     6, 4, 1, 1, 0, 3, 4, 6, 1, 3, 4, 0, 2, 2, 3, 0, 2, 4, 2, 3, 5, 1, 5, 0, 6, 
                     2, 2, 5, 4, 0, 3, 6, 0, 6, 5, 0, 0, 3, 6, 0, 1, 4, 5, 5, 6, 3, 2, 5, 1, 4, 
                     6, 2, 5, 6, 2, 0, 4, 0, 6, 1, 2, 6, 0, 4, 5, 4, 6, 4, 2, 1, 0, 3, 0, 5, 3, 
                     0, 6, 0, 1, 1, 6, 4, 0, 6, 3, 3, 5, 4, 4, 6, 5, 3, 4, 5, 5, 0, 3, 4, 0, 3, 
                     4, 6, 5, 6, 2, 5, 1, 1, 6, 3, 2, 0, 5, 0, 1, 0, 1, 0, 0, 5, 4, 4, 3, 4, 2, 
                     4, 0, 6, 3, 0, 2, 5, 4, 3, 6, 0, 5, 2, 1, 2, 0, 5, 3, 1, 5, 5, 2, 1, 2, 4, 
                     3, 0, 0, 2, 3, 0, 0, 4, 0, 4, 6, 3, 6, 2, 1, 4, 1, 6, 3, 6, 0, 4, 5, 6, 1],
            'control-space-variable':
                    [0, 4, 6, 4, 3, 1, 2, 5, 6, 0, 3, 2, 1, 5, 3, 1, 1, 5, 5, 2, 0, 2, 3, 4, 1, 
                     2, 2, 2, 2, 0, 3, 3, 3, 6, 5, 5, 3, 2, 2, 3, 0, 6, 6, 1, 2, 0, 5, 5, 1, 2, 
                     3, 6, 4, 0, 0, 3, 2, 3, 6, 5, 0, 2, 2, 0, 1, 2, 1, 6, 5, 6, 2, 3, 1, 1, 4, 
                     2, 5, 3, 6, 0, 0, 1, 5, 4, 4, 5, 6, 4, 1, 1, 6, 0, 2, 4, 1, 2, 0, 0, 3, 0, 
                     0, 1, 4, 5, 4, 1, 5, 6, 5, 4, 6, 5, 3, 6, 6, 2, 5, 6, 3, 4, 0, 5, 0, 6, 6, 
                     5, 1, 2, 3, 6, 6, 4, 5, 3, 0, 2, 4, 2, 2, 1, 0, 0, 1, 3, 1, 3, 5, 2, 2, 5, 
                     0, 6, 1, 2, 4, 6, 1, 4, 4, 0, 0, 4, 5, 4, 6, 0, 3, 3, 1, 1, 4, 2, 2, 1, 4, 
                     5, 2, 3, 0, 6, 0, 5, 5, 6, 6, 1, 1, 3, 6, 3, 4, 2, 2, 0, 0, 0, 0, 0, 6, 2]}
y_offset = {'control-ground-variable': 
                    [0, 0, 6, 1, 0, 1, 3, 1, 5, 0, 5, 2, 2, 4, 4, 3, 4, 2, 5, 0, 0, 3, 2, 4, 6, 
                     4, 6, 2, 0, 6, 6, 0, 3, 1, 4, 1, 1, 0, 1, 5, 0, 1, 6, 0, 4, 0, 6, 3, 3, 1, 
                     5, 6, 4, 4, 5, 3, 3, 4, 0, 1, 0, 6, 3, 4, 2, 1, 1, 0, 4, 0, 6, 3, 1, 3, 2, 
                     5, 2, 2, 6, 4, 0, 6, 4, 6, 4, 1, 4, 2, 0, 6, 5, 3, 1, 4, 5, 3, 2, 5, 1, 5, 
                     0, 4, 2, 2, 5, 5, 5, 3, 2, 3, 0, 0, 6, 3, 0, 3, 1, 1, 1, 2, 0, 2, 1, 2, 0, 
                     0, 3, 0, 1, 2, 5, 2, 4, 6, 5, 3, 1, 3, 5, 0, 0, 2, 5, 3, 2, 0, 2, 4, 3, 4, 
                     4, 1, 3, 0, 2, 5, 5, 5, 6, 1, 0, 1, 2, 4, 0, 4, 6, 4, 6, 3, 4, 6, 0, 1, 1, 
                     1, 1, 3, 5, 2, 0, 4, 4, 5, 1, 3, 0, 0, 6, 1, 0, 2, 1, 3, 2, 3, 6, 4, 5, 0],
            'control-space-variable':
                    [0, 2, 2, 4, 2, 3, 4, 3, 4, 5, 6, 2, 0, 5, 3, 6, 2, 4, 2, 1, 0, 1, 4, 1, 3, 
                     5, 4, 0, 3, 4, 3, 0, 6, 3, 2, 3, 2, 2, 6, 1, 0, 0, 3, 2, 3, 6, 1, 2, 5, 0, 
                     4, 6, 4, 1, 2, 5, 2, 0, 2, 4, 0, 2, 6, 4, 5, 1, 3, 1, 2, 0, 3, 0, 2, 1, 3, 
                     5, 3, 6, 3, 1, 0, 6, 0, 0, 1, 2, 0, 4, 3, 2, 6, 5, 3, 2, 4, 4, 2, 4, 4, 3, 
                     0, 3, 3, 0, 4, 2, 4, 4, 6, 2, 6, 5, 0, 3, 1, 3, 3, 5, 2, 0, 0, 5, 5, 3, 2, 
                     6, 0, 4, 4, 1, 5, 6, 2, 3, 2, 5, 4, 2, 3, 3, 0, 1, 0, 2, 2, 6, 4, 0, 5, 0, 
                     6, 3, 1, 6, 3, 1, 3, 6, 4, 2, 0, 3, 2, 4, 0, 5, 0, 2, 6, 0, 0, 1, 0, 2, 6, 
                     5, 2, 1, 6, 3, 0, 1, 5, 0, 6, 2, 6, 6, 2, 5, 2, 1, 3, 6, 2, 5, 3, 1, 3, 4]}                   
                    

def expected_galaxy_ids(branch):
    """
    Builds a list of galaxy IDs to compare user catalogs against, using known offsets if a 
    variable-shear branch.
    """
    if 'constant' in branch:
        expected_galaxy_id = ['%09i'%(1000000*k+1000*j+i) for i in range(100) 
                                                          for j in range(100) 
                                                          for k in range(200)]
    else:
        expected_galaxy_id = ['%09i'%(1000000*k+7000*j+7*i) for i in range(100) 
                                                            for j in range(100) 
                                                            for k in range(200)]                           
        # Note: Above lines are for first alpha release ONLY.  Second alpha release with fixed 
        # galaxy IDS uses this code: 
        # expected_galaxy_id = ['%09i'%(1000000*k+1000*(7*j+x_offset[branch][k])
        #                               +7*i+y_offset[branch][k])
        #                                      for i in range(100) for j in range(100) 
        #                                      for k in range(200)]                                                           
    return expected_galaxy_id
    