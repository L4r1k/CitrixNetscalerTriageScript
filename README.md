# Citrix Netscaler Triage Script

A script to help automate the recovery of triage artifacts from compromised Netscaler hosts.

## How it works

1. The script creates a directory on the /var partition `/var/artifactRecovery` to store the triage artifacts temporarily
2. The desired artifacts are copied to this temporary location then zipped into an archive `/var/artifactRecovery/<hostname>-recoveredArtifacts.zip`
    - Shutil copytree is used to help preserve metadata such as permissions and timestamps where possible

## How to run the script

1. Curl the script down to your host `curl https://raw.githubusercontent.com/L4r1k/CitrixNetscalerTriageScript/master/citrixTriageScript.py -o triageScript.py`
2. Run the script `python triageScript.py`
3. Once completed, retrieve the zip archive of recovered triage artifacts
    - `/var/artifactRecovery/<hostname>-recoveredArtifacts.zip`
4. Remove the script and the recovery directory from the host if desired
    - `rm -rf /var/artifactRecovery`
    - `rm triageScript.py` (or wherever else it was saved - see the output of the script for help)

## Triage Artifacts the script tries to recover

- /var/log
- /netscaler
- /var/tmp/netscaler
- /var/cron/tabs
- /var/nstmp
- /tmp/.init
- 'ps aux' output
- 'lsof -i -n -P' output
