import subprocess
import shlex
import re
import os

print "Gathering information please wait..."
sshcommand = shlex.split("lscpu")
process = subprocess.Popen(sshcommand, stdout=subprocess.PIPE)
_node_internal_ip = ''
_node_name = ''
_node_ext_ip = ''
_header = "NodeName,NodeIP,CPU,"
_value = ""
_json = "{\"NodeName\":"
_json_cpu = "\"CPU\":["
_json_mem = "\"MEMORY\":["
output, err = process.communicate()
list = output.split('\n')
for x in list:
    v = x.split(':')
    key = v[0].lstrip()
    if key == 'Architecture' or key == 'CPU(s)' or key == 'CPU MHz' or key == 'CPU max MHz' or key == 'CPU min MHz':
        _json_cpu += "{\"" + v[0].lstrip() + "\":\"" + v[1].lstrip() + "\"},"
        _header += str(v[0].lstrip()) + ","
memInfocommand = shlex.split("cat /proc/meminfo")
processmemInfo = subprocess.Popen(memInfocommand, stdout=subprocess.PIPE)
outputmemInfo, err1 = processmemInfo.communicate()
listmemInfo = outputmemInfo.split('\n')
_header += "MEMORY,"
for x in listmemInfo:
    v = x.split(':')
    key = v[0].lstrip()
    if key == 'MemTotal' or key == 'MemFree' or key == 'Cached' or key == 'Active(file)' or key == 'PageTables':
        _json_mem += "{\"" + v[0].lstrip() + "\":\"" + v[1].lstrip() + "\"},"
        _header += str(v[0].lstrip()) + ","
iopscommand = shlex.split("iostat")
processiops = subprocess.Popen(iopscommand, shell=False,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
outputiops, err1 = processiops.communicate()
tmp = outputiops.split('\n')
_json_combined = ""
_json_cpu = _json_cpu[:-1]
_json_cpu = _json_cpu + "]"
_json_mem = _json_mem[:-1]
_json_mem = _json_mem + "]"
_user = "%user"
str ="\"Disk_iops\":[{"
_iops_cpu ="\"avg-cpu\":[{"
_header_row_cpu_persentage = []
_header_row_iops = []
num = 0
for f in tmp:
    if f.lstrip() != '':
        g = re.sub(' +', '#', f)
        if "avg-cpu" in g:
            _header_row_cpu_persentage = g.split("#")
        if "Device" in g:
            _header_row_iops = g.split("#")
        _cpu_per = []
        if num == 2:
            _cpu_per = g.split("#")
            o=0
            for x in _cpu_per:
                if o>0 :
                 _iops_cpu+="\""+_header_row_cpu_persentage[o]+"\":\""+x+"\","
                o =o+1
        if num > 3:
            _iops = g.split("#")
            o=0
            for x in _iops :
                str += "\""+_header_row_iops[o]+"\":\""+x+"\","
                o=o+1
                if o==6 :
                    str=str[:-1]+"},{"
        num = num + 1
# Checking the PING delay for each pod from this pod.
# os.system('echo $CLUSTER_IPS')
# node ip find out
_iops1= str[:-2]+"]"
_iops2=_iops_cpu[:-1]+"}]"
nodeIP = os.popen('ifconfig | grep Bcast').read()
nodeIPList = nodeIP.split(' ')
for f in nodeIPList:
    if 'addr' in f:
        tok = f.split(':')
        _node_internal_ip = tok[1]
        break
out = os.popen('echo $CLUSTER_IPS').read()
listping = out.split(',')
_json_ping = "\"NetworkLatancy\":["
_json_ping_pod = ""
_json_all_pod = ""
for x in listping:
    y = x.split(":")
    nodeNM = y[0]
    key = y[1]
    value = y[2].replace('\n', '')
    value = value.lstrip()
    if (value == _node_internal_ip):
        _node_name = nodeNM
        _node_ext_ip = key

    # print nodeNM
    pingout = os.popen('ping -w 1 ' + value + ' | grep icmp_seq=1').read()
    pingoutsplit = pingout.split(" ")
    # print nodeNM,key,value,pingoutsplit[6]
    _json_ping_pod = "{\"POD_NAME\":\"" + nodeNM + "\",\"POD_IP\":\"" + value + "\",\"NODE_IP\":\"" + key + "\",\"TIME\":\"" + \
                     pingoutsplit[6] + "\"},"
    _json_all_pod = _json_all_pod + _json_ping_pod
_json_combined = "{" + _json_cpu + "," + _json_mem + "," + _json_ping + _json_all_pod[:-1] + "]" ","+_iops1+","+_iops2+ "}"
print _json_combined
