#!/usr/bin/python
import json
import os

import click

class Config(object):
    def __init__(self):
        pass

pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option("--configfilein",type=click.File("r"),default="gitclients_credentials.json",required=False)
@click.option("--configfileout",type=click.File("w"),default="gitclients_credentials.json",required=False)
@pass_config
def cli(config, configfilein, configfileout):
    if configfilein is None:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        print os.getcwd()
        config.configfile_in = configfilein
        config.configfile_out = configfileout
    else:
        print os.getcwd()
        config.configfile_in = configfilein
        config.configfile_out = configfileout



def get_cre():
    """
    Read  git credentials from settings file
    """
    with open('gitclients_credentials.json') as cred:
         data = json.load(cred)
    return data
@cli.command("speak")
@click.option("--repeat",default=1)
@pass_config
def say(config,repeat):
    for x in xrange(repeat):
        click.echo("hello",file=config.configfile_in)

@cli.command("gitclient")
@click.option('--name', prompt='Name of git client',
              help='The name of the git client you want to configure your current git project for')
@pass_config
def gc(config, name):
    """This configures your current git project to use the git client
     you passed in with the name argument"""
    gitclient = name.lower().replace(" ","")
    git_credentials = json.load(config.configfile_in)#get_cre()
    try:
        os.system('git config user.name ' + git_credentials[gitclient]["user.name"])
        os.system('git config user.email ' + git_credentials[gitclient]["user.email"] )               
        click.echo("Current git project configured for your " +gitclient +" account" )
    except KeyError:
        click.echo ("You have not added details for this client yet, please add it by running passing the add argument")
    #todo : add ability to check the .git/config file for the right values and then trigger the right"""

@cli.command('add',short_help="Use this to add new git client")
@click.option('--gc',prompt="Name of git client you want to add",help='Pass in the name of the new git client to pass like so github.Note everything passed in is converted to lower case and trimmed...ie GIT hub becomes github')
@click.option("--username",prompt="Username for this client",help="Add in  your username")
@click.option("--useremail",prompt="Email for this new client", help="Passing the email")
#todo validate email is actually an email, want happens when username is empty using regex
@pass_config
def add(config, gc,username,useremail):
    """
    Add a configuration for a new git client
    """
    git_client = gc.lower().replace(" ", "")
    git_credentials = json.load(config.configfile_in)
    git_credentials[git_client] ={"user.name":username, "user.email":useremail}
    #with open("gitclients_credentials.json",'w') as fh:
    try:
        json.dump(git_credentials, config.configfile_out)
    except:
        click.echo("New client {} was not added".format(git_client))
    click.echo("New client {} has been added".format(git_client))

if __name__ == '__main__':
    cli()
    