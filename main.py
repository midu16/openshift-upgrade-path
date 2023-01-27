__author__ = 'Mihai IDU'
__version__ = '1.0.0'
import requests
import re
import argparse

def UpgradeSourceCheck(from_version):
    from_url = "https://mirror.openshift.com/pub/openshift-v4/clients/ocp/" + from_version + "/release.txt"
    response = requests.get(from_url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return "Error: " + str(e)

    x = re.findall(r"Upgrades:([^Stock].+)", response.text)
    y = x[0].strip().split(', ')
    return y

def OCPVersionIncrease(ocp_from_version):
    ocp_inter_verison = ocp_from_version.split('.')
    ocp_inter_ver = int(ocp_inter_verison[len(ocp_inter_verison)-1]) + 1
    ocp_inter_verison = [s.replace(ocp_inter_verison[len(ocp_inter_verison)-1], str(ocp_inter_ver)) for s in ocp_inter_verison]
    return ('.'.join(ocp_inter_verison))

if __name__ == '__main__':
    #definig global variables
    text = 'This is the ocp-upgrade-path in order to validate the upgrade path of an OpenShift Cluster'
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument("-f","--ocp-from", help="Add OpenShift Cluster version used. Example: --ocp-from 4.11.10.")
    parser.add_argument("-d","--ocp-dest", help="Add OpenShift Cluster version you want to upgrade to. Example: --ocp-dest 4.12.0.")
    parser.add_argument("-v", "--version", action='version', version='%(prog)s ' + __version__)
    args = parser.parse_args()
    ocp_from_version = str(args.ocp_from)
    ocp_dest_version = str(args.ocp_dest)
    for index in UpgradeSourceCheck(ocp_dest_version):
        if ocp_from_version == index:
            print("From " + " " + ocp_from_version + " " + " To " + " " + ocp_dest_version)
        elif ocp_from_version != index:
            for jintex in UpgradeSourceCheck(ocp_dest_version):
                if OCPVersionIncrease(ocp_from_version) == jintex:
                    print("From " + " " + ocp_from_version + " " + " To " + " " + OCPVersionIncrease(ocp_from_version) + " To " + " " + ocp_dest_version)
            break

