import json, requests

from gl_proc import err

class API():
    ''' API(): Interact with a GitLab API                       '''

    def __init__(self, instance):
        ''' instance:                                           '''
        ''' ['url', 'version', 'tls_check', 'token']            '''
        
        try:        # Check instance accessibility
            requests.get(instance['url'])
        except:
            err("Unable to access GitLab instance at " + instance['url'])

        self.path = instance['url'] + instance['version']
        self.tls = instance['tls_check']        # Verify TLS certificate

        if len(instance['token']) > 0:
            self.token = instance['token']
        else:
            self.token = None

    def user_search(self, query):
        ''' user_search(): Open-ended user search               '''
        ''' In: query criteria; ex: username, user ID, email    '''
        ''' Out: Search results (if any)                        '''

        results = []

        search = requests.get(
                self.path + "search?scope=users&search=" + query,
                verify=self.tls,
                headers={"Private-Token":self.token}
                ).json()

        for user in search:
            results.append(
                requests.get(
                    self.path + "users/" + str(user['id']),
                    verify=self.tls,
                    headers={"Private-Token":self.token}
                ).json()
            )

        return(results)

    def whoami(self, token):
        ''' whoami(): Find owner of an API token                '''
        ''' In: API token                                       '''
        ''' Out: JSON of the authenticated user (if successful) '''

        return requests.get(
                self.path + "user",
                verify=self.tls,
                headers={"Private-Token":token}
                ).json()

    def user_note(self, userid, note):
        ''' admin_note(): Write an admin note on a user account '''
        ''' In: user ID int, note to be written                 '''
        ''' Out: API response                                   '''

        return(requests.put(
                self.path + "users/" + userid, 
                data={'note': note},
                verify=self.tls, 
                headers={"Private-Token":self.token}
                )
        )

    def user_block(self, user):
        ''' user_block(): Block a user account                  '''
        ''' In: user ID int                                     '''
        ''' Out: API response                                   '''

        return(requests.post(
            self.path + "users/" + str(user) + "/block",
            data={'block': 'true'}, 
            verify=self.tls,
            headers={"Private-Token":self.token}
            )
        )

    def user_unblock(self, userid):
        ''' user_unblock(): Unblock a user account              '''
        ''' In: user ID int                                     '''
        ''' Out: API response                                   '''

        return(requests.post(
            self.path + "users/" + userid + "/unblock",
            data={'unblock': 'true'},
            verify=self.tls, 
            headers={"Private-Token":self.token}
            )
        )

    def mr_getcommits(self, projectid, mergeid):
        ''' mr_getcommits(): Get commits in a Merge Request     '''
        ''' In: project ID int, merge request ID int            '''
        ''' Out: json of commits in MR                          '''

        return(requests.get(
            self.path + "projects/" + projectid + "/merge_requests/" + mergeid + "/commits",
            verify=self.tls,
            headers={"Private-Token":self.token}            
            ).json()
        )

    def mr_delete(self, projectid, mergeid):
        ''' mr_delete(): Delete the specified Merge Request     '''
        ''' In: project ID int, merge request ID int            '''
        ''' Out: API response in json                           '''

        return(requests.delete(
            self.path + "projects/" + projectid + "/merge_requests/" + mergeid,
            verify=self.tls,
            headers={"Private-Token":self.token}
            )
        )
    
    def mr_search(self, projectid, mergeid):
        ''' mr_search(): Locate Merge Request                   '''
        ''' In: project ID int, merge request ID int            '''
        ''' Out: API response in json                           '''

        return(requests.get(
            self.path + "projects/" + projectid + "/merge_requests/" + mergeid,
            verify=self.tls,
            headers={"Private-Token":self.token}
            ).json()
        )