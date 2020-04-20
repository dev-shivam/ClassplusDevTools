import os
import requests
import subprocess
import fileinput
import re
import json
import time

gitDirectory = "/Users/shivam/Documents/Classplus/App/android-v2"
buildNumberDict = {}  # needs to be always empty, will get items inserted while the script is running
currentBuildNumberDict = {}
buildSlugDict = {}  # needs to be always empty, will get items inserted while the script is running
currentBuildSlugDict = {}


def testSubprocess():
    a = subprocess.call(["ls -l"], stdin=None, stdout=None, stderr=None, shell=False)
    print(a)


def test():
    command = "l" + "s"
    print(command)
    os.system(command)


def printResult(resultLabel, result):
    print("\n\n" + resultLabel + ": " + str(result) + "\n\n")


def branchStatus():
    statusResult = subprocess.call(["git", "-C", gitDirectory, "status"], stdin=None, stdout=None, stderr=None,
                                   shell=False)
    return statusResult


def checkoutBranch(orgCode, branchHeader):
    checkoutResult = subprocess.call(["git", "-C", gitDirectory, "checkout", "-b", branchHeader + orgCode, "--track",
                                      "origin/" + branchHeader + orgCode])
    return checkoutResult


def mergeBranch(parentBranch):
    mergeResult = subprocess.call(["git", "-C", gitDirectory, "merge", "--no-commit", parentBranch])
    return mergeResult


def addFilesToCommit():
    addCode = subprocess.call(["git", "-C", gitDirectory, "add", "."])
    return addCode


def commitBranch(orgCode):
    commitResult = subprocess.call(["git", "-C", gitDirectory, "commit", "-m", orgCode + ": version updated"])
    return commitResult


def pushBranch(orgCode, branchHeader):
    pushResult = subprocess.call(["git", "-C", gitDirectory, "push", "origin", branchHeader + orgCode])
    return pushResult


def resetCode():
    addResult = addFilesToCommit()
    resetResult = subprocess.call(["git", "-C", gitDirectory, "reset", "--hard"])
    return resetResult


def deleteBranch(orgCode, branchHeader):
    deleteResult = subprocess.call(["git", "-C", gitDirectory, "branch", "-d", branchHeader + orgCode])
    return deleteResult


def changeBranch(parentBranch):
    changeResult = subprocess.call(["git", "-C", gitDirectory, "checkout", parentBranch])
    return changeResult


def changeVersions(versionName):
    data = []
    with open(gitDirectory + "/app/build.gradle", "r") as file:
        data = file.readlines()
        # print(data[20].split(' '))
        # print(data[21].split(' '))
        # versionCodeLine = data[20].strip().split(' ')
        # versionCode = int(a[1]) + 1
        # data[20] = "        versionCode " + str(versionCode) + "\n"
        # data[21] = '        versionName "1.0.22.1"\n'

        for i, line in enumerate(data):
            if "versionCode" in line:
                versionCodeLine = data[i].strip().split(' ')
                versionCode = int(versionCodeLine[1]) + 1
                data[i] = "        versionCode " + str(versionCode) + "\n"
            if "versionName" in line:
                data[i] = '        versionName "' + versionName + '"\n'

    with open(gitDirectory + "/app/build.gradle", "w") as file:
        file.writelines(data)
    #
    #   for line in file:
    #     if "versionName" in line:
    #       file.write("versionName 1.0.20.1")
    #     if "versionCode" in line:
    #       a = line.strip().split(' ')
    #       code = a[1] + 1
    #       file.write("versionCode code")

    # with fileinput.FileInput("/Users/farheenshah/AndroidStudioProjects/classplus/app/build.gradle", inplace=True) as file:
    #   for line in file:
    #     if "versionName" in line:
    #       print(line)

    # for line in fileinput.input('/Users/farheenshah/AndroidStudioProjects/classplus/app/build.gradle', inplace=True):
    #     if "versionCode" in line:
    #       # print(line)
    #       a = line.strip().split(' ')
    #       versionNumber = int(a[1]) + 1
    #       line.replace('versionCode ' + str(versionNumber-1), 'versionCode ' + str(versionNumber))


def deleteBranches(codesList, parentBranch, branchHeader):
    resetCode()
    changeResult = changeBranch(parentBranch)
    if (changeResult == 0):
        for code in codesList:
            printResult("deleteResult", deleteBranch(code, branchHeader))


def makeBitriseCall(orgCode, branchHeader, buildTriggerToken, workflowId, appId):
    url = "https://app.bitrise.io/app/8d0551b8d426d749/build/start.json"
    body = getBitriseBody(orgCode, branchHeader, buildTriggerToken, workflowId, appId)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=body)
    printResult("org: " + str(orgCode) + "\nbuildCode", response.status_code)
    if (response.status_code == 201):
        buildNumberDict[response.json()["build_number"]] = orgCode
        buildSlugDict[response.json()["build_number"]] = response.json()["build_slug"]
    else:
        printResult("org: " + str(orgCode) + "\nbuildCode", response.reason)
        printResult("org: " + str(orgCode) + "\nbuildCode", response.text)
    return response.status_code


def makeBitriseCall2(orgCode, branchHeader, buildTriggerToken, workflowId, appId):
    url = "https://app.bitrise.io/app/d01454473268be77/build/start.json"
    body = getBitriseBody(orgCode, branchHeader, buildTriggerToken, workflowId, appId)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=body)
    printResult("org: " + str(orgCode) + "\nbuildCode", response.status_code)
    if (response.status_code == 201):
        buildNumberDict[response.json()["build_number"]] = orgCode
        buildSlugDict[response.json()["build_number"]] = response.json()["build_slug"]
    else:
        printResult("org: " + str(orgCode) + "\nbuildCode", response.reason)
        printResult("org: " + str(orgCode) + "\nbuildCode", response.text)
    return response.status_code


def makeBitriseCall3(orgCode, branchHeader, buildTriggerToken, workflowId, appId):
    url = "https://app.bitrise.io/app/bd1687afbe52ce94/build/start.json"
    body = getBitriseBody(orgCode, branchHeader, buildTriggerToken, workflowId, appId)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=body)
    printResult("org: " + str(orgCode) + "\nbuildCode", response.status_code)
    if (response.status_code == 201):
        buildNumberDict[response.json()["build_number"]] = orgCode
        buildSlugDict[response.json()["build_number"]] = response.json()["build_slug"]
    else:
        printResult("org: " + str(orgCode) + "\nbuildCode", response.reason)
        printResult("org: " + str(orgCode) + "\nbuildCode", response.text)
    return response.status_code


def makeBitriseCall4(orgCode, branchHeader, buildTriggerToken, workflowId, appId):
    url = "https://app.bitrise.io/app/7f6d2b2f86f08db1/build/start.json"
    body = getBitriseBody(orgCode, branchHeader, buildTriggerToken, workflowId, appId)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=body)
    printResult("org: " + str(orgCode) + "\nbuildCode", response.status_code)
    if (response.status_code == 201):
        buildNumberDict[response.json()["build_number"]] = orgCode
        buildSlugDict[response.json()["build_number"]] = response.json()["build_slug"]
    else:
        printResult("org: " + str(orgCode) + "\nbuildCode", response.reason)
        printResult("org: " + str(orgCode) + "\nbuildCode", response.text)
    return response.status_code


def makeBitriseCall5(orgCode, branchHeader, buildTriggerToken, workflowId, appId):
    url = "https://app.bitrise.io/app/22c6018eccdcf9bd/build/start.json"
    body = getBitriseBody(orgCode, branchHeader, buildTriggerToken, workflowId, appId)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=body)
    printResult("org: " + str(orgCode) + "\nbuildCode", response.status_code)
    if (response.status_code == 201):
        buildNumberDict[response.json()["build_number"]] = orgCode
        buildSlugDict[response.json()["build_number"]] = response.json()["build_slug"]
    else:
        printResult("org: " + str(orgCode) + "\nbuildCode", response.reason)
        printResult("org: " + str(orgCode) + "\nbuildCode", response.text)
    return response.status_code


def makeBitriseCall6(orgCode, branchHeader, buildTriggerToken, workflowId, appId):
    url = "https://app.bitrise.io/app/0a1b32f2daf7dc90/build/start.json"
    body = getBitriseBody(orgCode, branchHeader, buildTriggerToken, workflowId, appId)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=body)
    printResult("org: " + str(orgCode) + "\nbuildCode", response.status_code)
    if (response.status_code == 201):
        buildNumberDict[response.json()["build_number"]] = orgCode
        buildSlugDict[response.json()["build_number"]] = response.json()["build_slug"]
    return response.status_code


def getOrgCodes(ads):
    if (ads):
        url = "https://api.classplusapp.com/su/organizations/codes?ads=1"
    else:
        url = "https://api.classplusapp.com/su/organizations/codes?ads=0"
    headers = {'accessKey': 'N6FPaqWCG58jH0d7u7Qoh7xTugP5Mw_IJQGjbRnQXKuImDL-9hCaVFQg'}
    response = requests.get(url, headers=headers)
    orgCodes = response.json()["data"]["orgCodes"]
    print(len(orgCodes))
    return orgCodes


def getOrgDetails(orgCode):
    url = "https://api.classplusapp.com/su/organizations/details?orgCode=" + orgCode
    headers = {'Content-Type': 'application/json',
               'accessKey': 'N6FPaqWCG58jH0d7u7Qoh7xTugP5Mw_IJQGjbRnQXKuImDL-9hCaVFQg'}
    response = requests.get(url, headers=headers)
    return response.json()


def getBitriseBody(orgCode, branchHeader, buildTriggerToken, workflowId, appId):
    body = {}
    body["triggered_by"] = "curl"
    body["hook_info"] = {}
    body["hook_info"]["type"] = "bitrise"
    body["hook_info"]["build_trigger_token"] = buildTriggerToken
    body["branch"] = branchHeader + orgCode
    body["build_params"] = {}
    body["build_params"]["branch"] = branchHeader + orgCode
    body["build_params"]["workflow_id"] = workflowId
    body["build_params"]["environments"] = []
    jksObject = {}
    jksObject["mapped_to"] = "BITRISEIO_ANDROID_KEYSTORE_URL"
    jksObject["value"] = "file://./app/" + orgCode + ".jks"
    jksObject["is_expand"] = True

    branchObject = {}
    branchObject["mapped_to"] = "BITRISE_GIT_BRANCH"
    branchObject["value"] = branchHeader + orgCode
    branchObject["is_expand"] = True

    packageNameObject = {}
    packageNameObject["mapped_to"] = "APP_PACKAGE_NAME"
    packageNameObject["value"] = appId
    packageNameObject["is_expand"] = True

    body["build_params"]["environments"].append(jksObject)
    body["build_params"]["environments"].append(branchObject)
    body["build_params"]["environments"].append(packageNameObject)
    return json.dumps(body)


def getBody(orgCode, branchHeader):
    body = '''{
  	"hook_info":{
    "type":"bitrise",
    "api_token":"Iu22CqIaH2Ej96C2dRk7iw"

  	},
  	"build_params":{
    "workflow_id":"stellar_academy",
    "environments":[
      {
        "mapped_to":"BITRISEIO_ANDROID_KEYSTORE_URL", "value":"file://./app/''' + orgCode + '''.jks", "is_expand":true
      },
      {
        "mapped_to":"APP_PACKAGE_NAME", "value":"co.classplus.''' + orgCode + '''", "is_expand":true
      },
      {
        "mapped_to":"BITRISE_GIT_BRANCH","value":"''' + branchHeader + orgCode + '''","is_expand":true

      }
      ]

  	},"triggered_by":"curl"}'''
    return body


def getBuildOnlyBody(orgCode, branchHeader):
    body = '''{
	"hook_info":{"type":"bitrise","api_token":"Iu22CqIaH2Ej96C2dRk7iw"},
	"build_params":{"workflow_id":"build_apk","environments":[
	  {
	      "mapped_to":"BITRISEIO_ANDROID_KEYSTORE_URL",
	        "value":"file://./app/''' + orgCode + '''.jks",
	        "is_expand":true
	        },
	        {
	        "mapped_to":"BITRISE_GIT_BRANCH",
	        "value":"''' + branchHeader + orgCode + '''",
	        "is_expand":true
	        }
	        ]
	        },
	        "triggered_by":"curl"}'''

    return body


def makeBuildOnlyBitriseCall(orgCode, branchHeader):
    url = "https://app.bitrise.io/app/8d0551b8d426d749/build/start.json"
    body = getBuildOnlyBody(orgCode, branchHeader)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=body)
    printResult("responseCode", response.status_code)


def makeAbortBuildCall(buildSlug, buildNumber):
    url = "https://api.bitrise.io/v0.1/apps/8d0551b8d426d749/builds/" + buildSlug + "/abort"
    body = getAbortBuildBody()
    headers = {'Content-Type': 'application/json',
               'Authorization': 'token YgH32T8fX8XEZK377zBHC3gUCLRBkqkXx2vUBq4XxaZSE2mUlVmYacUBhOD8YZHY6FH3LsAqJGSn_VkMR83esw'}
    response = requests.post(url, headers=headers, data=body)
    printResult("buildNumber: " + str(buildNumber) + "\nabortBuildCode", response.status_code)
    return response.status_code


def getAbortBuildBody():
    body = {}
    body["abort_reason"] = "going-to-fail"
    body["abort_with_success"] = False
    body["skip_notifications"] = False
    return json.dumps(body)


def changeAndDeleteBranch(orgCode, branchHeader, parentBranch):
    changeResult = changeBranch(parentBranch)
    if (changeResult == 0):
        deleteBranch(orgCode, branchHeader)


def start(orgCode, versionName, branchHeader, parentBranch, buildTriggerToken, workflowId, appId):
    resetResult = resetCode()
    if (resetResult != 0):
        return 1

    printResult("statusResult", branchStatus())
    printResult("checkoutResult", checkoutBranch(orgCode, branchHeader))
    mergeResult = mergeBranch(parentBranch)
    printResult("mergeResult", mergeResult)
    if (mergeResult != 0):
        return 1
    buildCode = startAfterMerge(orgCode, versionName, branchHeader, parentBranch, buildTriggerToken, workflowId, appId)
    if (buildCode == 201):
        return 0
    else:
        return 1


def startAfterMerge(orgCode, versionName, branchHeader, parentBranch, buildTriggerToken, workflowId, appId):
    changeVersions(versionName)
    printResult("gitAddCode", addFilesToCommit())
    printResult("commitResult", commitBranch(orgCode))
    printResult("pushResult", pushBranch(orgCode, branchHeader))
    if workflowId == 'stan' or workflowId == 'tarly' or workflowId == 'martin' or workflowId == 'april2019' or workflowId == 'jarvis':
        buildCode = makeBitriseCall2(orgCode, branchHeader, 'dKO-PTbPIGF98WoDapfeOQ', workflowId, appId)
    elif workflowId == 'varys' or workflowId == 'shield' or workflowId == 'kevin' or workflowId == 'nick' or workflowId == 'iron':
        buildCode = makeBitriseCall3(orgCode, branchHeader, 'DhK7pzLRrdh-5yEJKwJqZA', workflowId, appId)
    elif workflowId == 'alexis' or workflowId == 'edvin' or workflowId == 'thor' or workflowId == 'thanos' or workflowId == 'lynde':
        buildCode = makeBitriseCall4(orgCode, branchHeader, 'GfpH4y4mPhrCGpfbjfLrmg', workflowId, appId)
    elif workflowId == 'bolton' or workflowId == 'sansa' or workflowId == 'bran' or workflowId == 'hodor' or workflowId == 'alicia':
        buildCode = makeBitriseCall5(orgCode, branchHeader, 'Zjhz159-fJg_JobfM5oZiA', workflowId, appId)
    elif workflowId == 'groot' or workflowId == 'arya' or workflowId == 'loki' or workflowId == 'davos' or workflowId == 'jorah':
        buildCode = makeBitriseCall6(orgCode, branchHeader, 'x7Y75g8BaEhRJz0X1j8fIg', workflowId, appId)
    else:
        buildCode = makeBitriseCall(orgCode, branchHeader, buildTriggerToken, workflowId, appId)
    resetCode()
    changeResult = changeBranch(parentBranch)
    printResult("deleteResult", deleteBranch(orgCode, branchHeader))
    return buildCode


def loopInCodesWithDelay(codesList):
    for index, code in enumerate(codesList, 177):
        print("Starting : " + str(index + 1) + "/" + str(len(codesList)))
        time.sleep(1)


def loopInCodes(codesList, versionName, priorityOrgCodes):
    success = []
    failure = []
    for index, code in enumerate(codesList):
        print("Starting : " + str(index + 1) + "/" + str(len(codesList)))
        if code in priorityOrgCodes:
            print(str(code) + " : Skipped")
            continue
        orgData = getOrgDetails(code)["data"]["orgDetails"]
        # todo add null check for ads
        if (orgData["ads"] == 0):
            parentBranch = "white_label_" + orgData["androidBitriseWorkFlowId"]
            branchHeader = "whitelabel_"
        else:
            parentBranch = "white_label_ads_" + orgData["androidBitriseWorkFlowId"]
            branchHeader = "whitelabel_ads_"
        finalResult = start(code, versionName, branchHeader, parentBranch, orgData["androidBitriseToken"],
                            orgData["androidBitriseWorkFlowId"], orgData["androidAppId"])
        if (finalResult == 0):
            success.append(code)
        else:
            failure.append(code)
            break
    # time.sleep(5)

    resetCode()
    changeResult = changeBranch(parentBranch)

    print("success:")
    print(success)
    print("failure:")
    print(failure)
    print(buildNumberDict)
    print("\n\n\n")
    print(buildSlugDict)


failedBuilds = (10923, 10952, 11090, 11140, 11276, 11344, 11366)


# Re-build
def loopInBuildNumberDict(buildDict):
    success = []
    failure = []
    for i in range(17043, 17136):
        code = buildDict[i]
        orgData = getOrgDetails(code)["data"]["orgDetails"]
        # todo add null check for ads
        if (orgData["ads"] == 0):
            parentBranch = "white_label_" + orgData["androidBitriseWorkFlowId"]
            branchHeader = "whitelabel_"
        else:
            parentBranch = "white_label_ads_" + orgData["androidBitriseWorkFlowId"]
            branchHeader = "whitelabel_ads_"
        finalResult = makeBitriseCall(code, branchHeader, orgData["androidBitriseToken"],
                                      orgData["androidBitriseWorkFlowId"], orgData["androidAppId"])
        if (finalResult == 201):
            success.append(code)
        else:
            failure.append(code)
    print("success:")
    print(success)
    print("failure:")
    print(failure)
    print(buildNumberDict)
    print("\n\n\n")
    print(buildSlugDict)


# Abort builds
def loopInBuildSlugDict(slugDict):
    success = []
    failure = []
    for i in range(34986, 34996):
        slug = slugDict[i]
        finalResult = makeAbortBuildCall(slug, i)
        if (finalResult == 200):
            success.append(i)
        else:
            failure.append(i)
        # api fatt gayi, thodi der baad kro
        if finalResult == 429:
            break
    print("success:")
    print(success)
    print("failure:")
    print(failure)


currentVersion = "1.0.93.1"
currentOrgCode = "ruchi"

jwOrgs = ["ead", "exam", "eaa", "techa", "learn", "dmo", "clps", "cau"]

adBranchHeader = "whitelabel_ads_"
noAdBranchHeader = "whitelabel_"
adParentBranch = "white_label_ads"
noAdParentBranch = "white_label"

removedApps1 = ["rqc", "sbz", "devias", "aecl", "bst", "briac", "gki", "igni", "mind"]
removedApps2 = ["nimig", "pei", "proch", "shsa", "pec", "aoa", "prak", "milest"]

# makeBitriseCall("demo", noAdBranchHeader)
# makeAbortBuildCall("2790d0480d3cced0", 5531)
# print(len(april2019_slot1))
# print(len(stellarOrgs_slot1))
# print getBuildOnlyBody("ac", "whitelabel_")
# print(getOrgCodes(True))

########################################################################################################################################
# BuildDict Loop
# loopInBuildNumberDict(currentBuildNumberDict)
########################################################################################################################################

########################################################################################################################################
# BuildSlugDict Loop
# loopInBuildSlugDict(currentBuildSlugDict)
########################################################################################################################################

########################################################################################################################################
# Priority Loop
# loopInCodes(failedOrgsFetchedFromScript, currentVersion, [])
# loopInCodes(["geeks"], currentVersion, [])
#######################################################################################################################################

########################################################################################################################################
# Org loop
# loopInCodes(april2019, currentVersion, list(set(storeOrgs + doneStoreOrgs + doneOrgs)))
# ["tak","shreec","uccl","funda","smarto","aoapl","jugad","sada","avg","svadhya","medipg"]
# loopInCodes(priority3, currentVersion, [])#removedApps + removedApps2 + removedApps3)#list(set(storeOrgs + doneStoreOrgs + doneOrgs)))
# loopInCodes(['isdvk', 'gw', 'vpcl', 'aara', 'zqiyn'], currentVersion, [])
# loopInCodes(['apns', 'bart', 'mppsc'], currentVersion, [])
# loopInCodes(['bfa', 'abhayaas', 'pinfo', 'se'], currentVersion, [])
loopInCodes(removedApps2, currentVersion, [])

# pulse, hmukr
# whatsapp
# bajpai
# praveen
# keval
# sachar orgs from mail
# daman ji removed apps

# jarvis

# ['read', 'apns', 'rix',
# ['slc', 'inb', 'mtbe', 'chavan']
# loopInCodesWithDelay(adOrgCodes)
########################################################################################################################################

########################################################################################################################################
# Test loop
# loopInCodesWithDelay(priorityOrgCodes)
########################################################################################################################################


# makeBitriseCall3("jzwln", "whitelabel_", "DhK7pzLRrdh-5yEJKwJqZA", "iron", "co.iron.jzwln")
# makeBitriseCall("medipg", "whitelabel_", "Iu22CqIaH2Ej96C2dRk7iw", "khal", "co.khal.medipg")
# makeBitriseCall2("sbz", "whitelabel_", "dKO-PTbPIGF98WoDapfeOQ", "stan", "co.stan.sbz")
# makeBitriseCall2("galaxy", "whitelabel_", "dKO-PTbPIGF98WoDapfeOQ", "april2019", "co.april2019.galaxy")
# makeBitriseCall("geeks", "whitelabel_", "Iu22CqIaH2Ej96C2dRk7iw", "april2019", "co.april2019.geeks")
# makeBitriseCall("kbcg", "whitelabel_", "Iu22CqIaH2Ej96C2dRk7iw", "april2019", "co.april2019.kbcg")
# makeBitriseCall("exemp", "whitelabel_", "Iu22CqIaH2Ej96C2dRk7iw", "april2019", "co.april2019.exemp")
# makeBitriseCall("na", "whitelabel_", "Iu22CqIaH2Ej96C2dRk7iw", "april2019", "co.april2019.na")
# makeBitriseCall("rpsc", "whitelabel_ads_", "Iu22CqIaH2Ej96C2dRk7iw", "jarvis", "co.jarvis.rpsc")

# makeBitriseCall(currentOrgCode, noAdBranchHeader)
# start(currentOrgCode, currentVersion, noAdBranchHeader, noAdParentBranch)
# startAfterMerge(currentOrgCode, currentVersion, noAdBranchHeader)
# changeAndDeleteBranch(currentOrgCode, noAdBranchHeader, noAdParentBranch)

# start(currentOrgCode, currentVersion, adBranchHeader, adParentBranch)
# startAfterMerge(currentOrgCode, currentVersion, adBranchHeader)
# changeAndDeleteBranch(currentOrgCode, adBranchHeader, adParentBranch)
