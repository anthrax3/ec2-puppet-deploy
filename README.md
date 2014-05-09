# EC2 Puppet Deploy

## So What Is It?
This is a Python script that uses `fabric` and `boto` to dynamically deploy
Puppet manifests to puppet masters in AWS. This could easily be used with
systems other than puppet, but that's what I use it for. Your deployment
process may well be able to fit as the deployment commands are supplied by you.


It assumes that you need to access the puppet masters via a jumpbox/SSH proxy,
and that there is at least one jumpbox per environment, like below...

```
 ------------   ------------   -------------   -------------
| PM 1 - Dev | | PM 2 - Dev | | PM 1 - Live | | PM 2 - Live |
 ------------   ------------   -------------   -------------
       |              |              |               |
       ----------------             -----------------
      | Jumpbox - Dev  |           | Jumpbox - Live  |
       ----------------             -----------------
                |                            |
                ------------------------------
                             |
                     -----------------
                    |   Workstation   |
                     -----------------
```

For this to work your puppet masters must be tagged with their environment and
some way of identifying them as puppet masters (e.g. `environment` and `role`
tags). What tags you use to identify your puppet masters can be configured in
the `config.yaml` file.

The script uses `boto` to dynamically find your puppet masters and jumpboxes,
then uses `fabric` to run a set of commands (defined in `config.yaml`) on the
puppet masters of a given environment, using the jumpbox as a SSH gateway into
that environment.

You will need to supply your own commands for actually deploying your puppet
manifests, as everyone will do this differently. You might sync a git repo, or
download and unpack an archive from a remote location.

## Installation
Clone the repo and install the dependencies with the following commands:

```
git clone https://github.com/cdodd/ec2-puppet-deploy.git
cd ec2-puppet-deploy
sudo pip install -r requirements.txt
```

You will need to create a `~/.boto` file with your AWS key ID and access
key, as follows:

```
[Credentials]
aws_access_key_id = xxxxxxxxxxxxxxxxxxxx
aws_secret_access_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

You will also need password-less SSH keys installed on jumpboxes and puppet
masters.

## Configuration
All required settings are stored in the `config.yaml` file. When configuring
commands to run in `config.yaml` you would run a standard command with the line
`- run: /path/to/command`. To run a command with sudo you would use `sudo`
instead on `run`, like `- sudo: /path/to/command`. This matches the command
names that `fabric` uses. You'll need to make sure your SSH user is configured
with sudo access for sudo commands to work (obviously).

## Deploying Puppet Manifests to Puppet masters
To deploy puppet to an environment run `./deploy -e ENVIRONMENT`, where
`ENVIRONMENT` matches the tag you've specified for the environment to deploy
to. `fabric` will then SSH onto the puppet masters (via the jumpbox for that
environment)
and run the given deployment commands.

You can also specify the EC2 region to use on the commandline with the option
`-r REGION` or `--region=REGION`, where `REGION` is the EC2 region you want to
deploy to (e.g. `eu-west-1`)
