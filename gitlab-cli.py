#!/usr/bin/python3

import argparse, json, os, sys

import gl_api, gl_inout
import gl_proc as run 

def main():
    ''' main(): Brains! '''

    config = gl_inout.config_ingest() # Process config file
    actions = run.args_ingest() # Process CLI arguments

    writer = gl_inout.output(actions.outfile, actions.verbose) # Primary Writer
    session = gl_api.API(config['instance'][0]) # API Session

    if actions.token:       # Token override
        session.token = actions.token   # Apply CLI arg token over config token

    writer.write(           # CLI/Out-file writing of final execution
        run.action(session, actions)    # Execute!
    )

if __name__ == "__main__":
    main()
