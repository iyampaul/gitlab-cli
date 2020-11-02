import argparse, time, sys

import gl_api, gl_inout

DESC = ''' GitLab API CLI; simplifying administative interaction '''

def args_ingest():
    ''' args_ingest(): CLI arguments to execute script '''

    parser = argparse.ArgumentParser(
        prog="gitlab-cli", 
        description=DESC,
        epilog="Contribute: https://gitlab.com/iyampaul/gitlab-cli"
        )
    parser.add_argument("--block", help="Block user account(s)", action="store_true")
    parser.add_argument("--deleteMR", help="Delete merge request ID", type=int)
    parser.add_argument("-i", "--infile", help="Ingest file, paired with other commands (search, block/unblock, passwd reset, etc)", type=str)
    parser.add_argument("--note", help="Place an admin note on user account(s)", type=str)  
    parser.add_argument("--search", help="Search for a single user (\"-u\") or user list (\"-i\")", action="store_true")  
    parser.add_argument("-o", "--outfile", help="Write output to specified file", type=str)
    parser.add_argument("-p", "--project", help="Specify project ID to manipulate", type=int)
    parser.add_argument("-t", "--token", help="Override configured API token", type=str)
    parser.add_argument("--unblock", help="Unblock user account(s)", action="store_true")
    parser.add_argument("-u", "--user", help="Individual user selection", type=str)
    parser.add_argument("-v", "--verbose", help="Output to console (default true unless using -o)", action="store_true")
    parser.add_argument("--whoami", help="Identify the owner of an API token: --whoami <token>", type=str)

    return(parser.parse_args())

def action(session, actions):
    ''' process(): Execute desired actions      '''
    ''' In: API session, desired action         '''
    ''' Out: Returns results of action          '''

    if actions.search:      # User search
        return(user_search(session, actions))
    if actions.whoami:      # Locate token owner
        return(session.whoami(actions.whoami))
    if actions.block:       # Block user(s)
        return(user_block(session, actions))
    if actions.unblock:     # Unblock user(s)
        return(user_unblock(session, actions))
    if actions.note:        # Admin note on user(s)
        return(user_note(session, actions))
    if actions.deleteMR:    # Delete merge request
        return(mr_delete(session, actions))

    err("No input arguments. Use \"-h\" for list of commands.")


def user_search(session, actions):
    ''' user_search(): Locate and return search results      '''
    ''' In: API session, input arguments                     '''
    ''' Out: Search results                                  '''

    query = user_ingest(actions)
    results = []

    for user in query:
        results.append(session.user_search(user))
        #time.sleep(1)
    
    return(results)

def user_block(session, actions):
    ''' user_block(): Block user account(s)                 '''
    ''' In: API session, user ID(s)                         '''
    ''' Out: Dict {userID:state}                            '''

    query = user_ingest(actions)
    results = []

    for user in query:
        if user_idcheck(user):
            results.append({user:session.user_block(user)})
        else:
            err("User ID's only, problem with: " + user)
    
    return(results)

def user_unblock(session, actions):
    ''' user_unblock(): Unblock user account(s)             '''
    ''' In: API session, user ID(s)                         '''
    ''' Out: Dict {userID:state}                            '''

    query = user_ingest(actions)
    results = []

    for user in query:
        if user_idcheck(user):
            results.append({user:session.user_unblock(user)})
        else:
            err("User ID's only, problem with: " + user)

    return(results)

def user_note(session, actions):
    ''' user_note(): Overwrite admin note on account(s)     '''
    ''' In: API session, user ID(s), note text              '''
    ''' Out: Dict {userID:state}                            '''

    query = user_ingest(actions)
    results = []

    for user in query:
        if user_idcheck(user):
            print(actions.note)
            results.append({user:session.user_note(user,actions.note)})
        else:
            err("User ID's only, problem with: " + user)
        
    return(results)

def mr_delete(session, actions):
    ''' mr_delete(): Verify and delete merge request       '''
    ''' In: API session, input arguments                   '''
    ''' Out: MR details, API response                      '''

    metadata = []
    post =  gl_inout.output(None, True) # CLI output

    if (actions.project != None) and (actions.deleteMR != None):
        metadata = session.mr_search(actions.project,actions.deleteMR)
    else:
        err("Project ID (-p) and Merge Request ID (--deleteMR <id>) must be included")

    if gl_inout.action_confirm("mr", metadata, post):
        return(session.mr_delete(actions.project, actions.deleteMR))

    

def user_ingest(actions):
    ''' user_ingest(): Ingests input file or input arg      '''
    ''' In: Input arguments                                 '''
    ''' Out: User list                                      '''

    users = []
    if actions.infile != None:               # Multiple queries 
        users = gl_inout.input(actions.input)
        return(users.data)
    if actions.user:                # Single query
        users.append(actions.user)
        return(users)

    err("No search criteria included, use \"-u\" or \"-i\" to add")

def user_idcheck(user):
    ''' user_idcheck(): Confirm user ID verses username    '''
    ''' In: user input                                     '''
    ''' Out: True for ID, False for username               '''

    try:
        int(user)
        return(True)
    except:
        return(False)

def err(text):
    ''' err(): Basic error handling '''

    print("ERROR: " + text)
    sys.exit()

