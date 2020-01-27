#! /usr/bin/env python
import shutil
import os
import logging
import subprocess


def main():
    artifact_recovery_path = os.path.join("/var/artifactRecovery")
    artifact_path = os.path.join(artifact_recovery_path, "artifacts")
    artifact_path_tmp = os.path.join(artifact_path, "tmp")
    artifact_path_cron = os.path.join(artifact_path, "cron")
    cwd = None

    if not os.path.exists(artifact_path) or not os.path.exists(artifact_path_tmp) or not os.path.exists(artifact_path_cron):
        #print(artifact_path + " : does not exist")
        os.mkdir(artifact_recovery_path)
        os.mkdir(artifact_path)
        os.mkdir(artifact_path_tmp)
        os.mkdir(artifact_path_cron)
        #print(artifact_recovery_path + " : " + artifact_path + " : " + artifact_path_tmp + " : " + artifact_path_cron + " : created")
        cwd = os.getcwd()
        os.chdir(artifact_path)
        #print("Changed directory to : " + artifact_path)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="%s/recoveryLog.log" % artifact_path)

    def _verboseCopy(path, names):
        logging.info("Traversing path: %s" % path)
        for name in names:
            logging.info("Copying %s/%s" % (path, name))
        return []

    try:
        hostname = os.uname()[1]
    except Exception as e:
        hostname = ""
        logging.info("Unable to recover hostname")
    logging.info("Beginning artifact recovery for host %s" % hostname)
    print("\nBeginning artifact recovery")
    print("Logfile created at: %s/recoveryLog.log" % artifact_path)

    try:
        logging.info("Copying /var/log ...")
        print("Copying /var/log ...")
        shutil.copytree("/var/log", os.path.join(artifact_path, "log"), ignore=_verboseCopy)
    except Exception as e:
        logging.error("Error while copying /var/log : " + str(e))
        print("Error while copying /var/log. See log file for more details")

    try:
        logging.info("Copying /netscaler ...")
        print("Copying /netscaler ...")
        shutil.copytree("/netscaler", os.path.join(artifact_path, "netscaler"), ignore=_verboseCopy)
    except Exception as e:
        logging.error("Error while copying /netscaler : " + str(e))
        print("Error while copying /netscaler. See log file for more details")

    try:
        logging.info("Copying /var/tmp/netscaler ...")
        print("Copying /var/tmp/netscaler ...")
        shutil.copytree("/var/tmp/netscaler", os.path.join(artifact_path_tmp, "netscaler"), ignore=_verboseCopy)
    except Exception as e:
        logging.error("Error while copying /var/tmp/netscaler : " + str(e))
        print("Error while copying /var/tmp/netscaler. See log file for more details")

    try:
        logging.info("Copying /var/cron/tabs ...")
        print("Copying /var/cron/tabs ...")
        shutil.copytree("/var/cron/tabs", os.path.join(artifact_path_cron, "tabs"), ignore=_verboseCopy)
    except Exception as e:
        logging.error("Error while copying /var/cron/tabs : " + str(e))
        print("Error while copying /var/cron/tabs. See log file for more details")

    try:
        logging.info("Copy /var/nstmp/.nscache ...")
        print("Copying /var/nstmp.nscache ...")
        shutil.copytree("/var/nstmp", os.path.join(artifact_path_tmp, "nstmp"), ignore=_verboseCopy)
    except Exception as e:
        logging.error("Error while copying /var/nstmp : " + str(e))
        print("Error while copying /var/nstmp. See log file for more details")

    try:
        logging.info("Copy /tmp/.init ...")
        print("Copying /tmp/.init ...")
        shutil.copytree("/tmp/.init", os.path.join(artifact_path_tmp, ".init"), ignore=_verboseCopy)
    except Exception as e:
        logging.error("Error while copying /tmp/.init : " + str(e))
        print("Error while copying /tmp/.init. See log file for more details")

    try:
        logging.info("Capturing ps output")
        print("Capturing ps output ...")
        ps_f = open("%s/ps_output.txt" % artifact_path, "w")
        subprocess.call(["ps", "aux"], stdout=ps_f)
        ps_f.close()
    except Exception as e:
        logging.error("Error while capturing ps output : " + str(e))
        print("Error while capturing ps output. See log file for more details")

    try:
        logging.info("Capturing lsof output")
        print("Capturing lsof output ...")
        lsof_f = open("%s/lsof_output.txt" % artifact_path, "w")
        subprocess.call(["lsof", "-i", "-n", "-P"], stdout=lsof_f)
        lsof_f.close()
    except Exception as e:
        logging.error("Error while capturing lsof output : " + str(e))
        print("Error while capturing lsof output. See log file for more details")

    logging.info("Zipping recovered artifacts")
    print("Zipping recovered artifacts")
    shutil.make_archive(
        "%s/%s-recoveredArtifacts" % (artifact_recovery_path, hostname),
        "zip",
    )
    os.chdir(cwd)
    print("\nRecovery Complete. Please provide the file: \"%s/%s-recoveredArtifacts.zip\" for analysis." % (artifact_recovery_path, hostname))
    print("""Once the file is provided you can remove the following from this host:
    Recovery directory: %s
    This script: %s""" % (artifact_recovery_path, os.path.abspath(__file__)))


if __name__ == "__main__":
    main()
