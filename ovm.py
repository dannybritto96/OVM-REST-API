import requests
import json
import time

# Use this if you get InsecurePlatformWarning Error

# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)

######

# Initializing the session

s = requests.Session()
s.auth = ('username','password')
s.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})
baseUri = 'https://serveraddress:7002/ovm/core/wsapi/rest'

######

# Use this to skip SSL verification

# s.verify = False

######

# Get ID From Name Function

def get_id_from_name(s,baseUri,resource,obj_name):
    uri = baseUri+'/'+resource+'/id'
    r = s.get(uri)
    for obj in r.json():
        if 'name' in obj.keys():
            if obj['name'] == obj_name:
                return obj
    raise Exception("Failed to find ID")

# Create VM

repo_id = get_id_from_name(s,baseUri,'Repository','reponame')
sp_id= get_id_from_name(s,baseUri,'ServerPool','serverpoolname')
data= {'name':'vmname','description':'VM created using REST API','vmDomainType':'XEN_PVM','repositoryId':repo_id,'serverPoolId':sp_id}
uri= '{base}/Vm'.format(base=baseUri)
r= s.post(uri,data=json.dumps(data))

## Wait for Job Function

def wait_for_job(joburi,s):
        while True:
            time.sleep(1)
            r=s.get(joburi)
            job=r.json()
            if job['summaryDone']:
                print('{name}: {runState}'.format(name=job['name'], runState=job['jobRunState']))
                if job['jobRunState'].upper() == 'FAILURE':
                    raise Exception('Job failed: {error}'.format(error=job['error']))
                elif job['jobRunState'].upper() == 'SUCCESS':
                    if 'resultId' in job:
                        return job['resultId']
                    break
                else:
                    break         
x = r.json()
wait_for_job(x['id']['uri'],s)

######

#  Delete VM

vm_info =get_id_from_name(s,baseUri,'Vm','vmname')
r = s.delete(baseUri+'/Vm/'+vm_info['value'])

######

# Get VM Info

vm_info =get_id_from_name(s,baseUri,'Vm','vmname')
r = s.get(baseUri+'/Vm/'+vm_info['value'])
vm_info = r.json()

######

# Increase Memory

vm_info =get_id_from_name(s,baseUri,'Vm','vmname')
r = s.get(baseUri+'/Vm/'+vm_info['value'])
x = r.json()
x['memory'] = '512'
r = s.put(baseUri+'/Vm/'+temp['value'],data=json.dumps(x))

######
