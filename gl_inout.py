''' Input/Output and Helpers '''

import json, os
import gl_proc as run

def config_ingest():
    ''' config_ingest(): Reads config.json '''

    if os.path.isfile("config.json"):
        with open("config.json") as file:
            data = json.load(file)
            for i in data['instance']:
                if len(i['url']) == 0:
                    run.err("No instance URL in config.json")
        
            return(data)
    else:
        run.err("config.json missing or inaccessible")

def action_confirm(type, target, writer):
    ''' action_confirm(): Verify target is correct      '''
    ''' In: target[] data, type (user, mr, issue)       '''
    ''' In: CLI output writer                       ''' 
    ''' Out: True/False                                 '''

    if type == "mr":
        writer.merge_request(target)

    return False


class input():
    '''  input(): Ingest a line-separated file          '''

    def __init__(self, filename):
        ''' Ingests defined file                        '''
        ''' In: filename to ingest                      '''

        self.data = []

        if os.path.isfile(filename):
            with open(filename) as file:
                for i in file:
                    self.data.append(i)
        else:
            run.err(filename + " missing or inaccessible")

class output():
    ''' output(): Class to write to file and/or console '''

    def __init__(self, filename, verbose):
        ''' Initializes file/console writer             '''
        ''' In: filename and verbosity if requested     '''

        self.verbose = verbose

        if filename:
            self.filename = open(filename, "w+")
        else:
            self.filename = None

    def write(self, data):
        ''' write(): Output to file and/or console      '''
        ''' In: data to write                           '''
        ''' Out: None                                   '''

        if self.filename:
            self.filename.write(str(data))

            if self.verbose:
                print(data)
        else:
            print(data)

    def merge_request(self, data):
        ''' merge_request(): Print MR data to console   '''
        ''' In: Merge request details                   '''
        ''' Out: None                                   '''

        print("Merge Request ID: " + str(data['id']))
        print("Title: " + data['title'])
        print("Created: " + data['created_at'])
        print("Author Name (username): " + data['author']['name'] + " (" + data['author']['username'] + ")")

    def user(self, data):
        ''' user(): Print user data to console          '''
        ''' In: User details                            '''
        ''' Out: None                                   '''

        meta = data[0]

        print("-"*20)
        print("Name (username): " + meta['name'] + " (" + meta['username'] + ")")
        print("User ID: " + str(meta['id']))
        print("Email: " + meta['email'])
        print("Current IP: " + meta['current_sign_in_ip'])
        print("Last IP: " + meta['last_sign_in_ip'])
