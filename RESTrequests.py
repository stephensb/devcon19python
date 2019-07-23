import requests
import json
key = 'KeyFromBbDevAppRegistration'
secret = 'SecretSquirrel'
target_domain = 'mybb.institution.edu'

api_base_path = '/learn/api/public/'
api_default_version = 'v1'
rest_api = {
    'token': f"{api_base_path}{api_default_version}/oauth2/token",
    'users': f"{api_base_path}{api_default_version}/users/:userId",
    'courses': f"{api_base_path}{api_default_version}/courses/:courseId",
    'memberships': f"{api_base_path}{api_default_version}/courses/:courseId/users",
    'enrollment': f"{api_base_path}{api_default_version}/courses/:courseId/users/:userId",
    'enrollments': f"{api_base_path}{api_default_version}/users/:userId/courses",
}
payload = {"grant_type": "client_credentials", "token": None}
# lets the auth and headers here
auth = ''
headers = ''


def set_token():
    global auth
    global headers
    oauth_url = f"https://{target_domain}{rest_api['token']}"
    print(f"[POST] OAuth2 Set Token URL: {oauth_url}")
    oauth_res = requests.post(oauth_url, data=payload, auth=(key, secret))
    print(f"=== Token Response ===\n{oauth_res.text}\n")
    payload['token'] = oauth_res.json()['access_token']
    auth = f"Bearer {payload['token']}"
    headers = {'Authorization': auth, 'Content-Type': 'application/json'}


def post_bb_data(version=None, **kwargs):
    bb_object = kwargs['api'].title()
    url = f"https://{target_domain}{rest_api[kwargs['api']]}"

    try:
        url = url.replace(kwargs['remove'], kwargs['replace'])
    except KeyError:
        pass

    data = kwargs['data']
    print(f"[POST] {bb_object} URL: {url}")
    rest_res = requests.post(url, json=data, headers=headers)
    print(f"=== {bb_object} Response ===\n{rest_res.text}\n")
    return rest_res.json()


def get_bb_data(version=None, **kwargs):
    bb_object = kwargs['api'].title()
    url = f"https://{target_domain}{rest_api[kwargs['api']]}"

    if version:
        url = url.replace(api_default_version, version)

    if kwargs['api'] == 'users' or kwargs['api'] == 'enrollments':
        url = url.replace(':userId', kwargs['userId'])
    elif kwargs['api'] == 'courses' or kwargs['api'] == 'memberships':
        url = url.replace(':courseId', kwargs['courseId'])
    elif kwargs['api'] == 'enrollment':
        url = url.replace(':courseId', kwargs['courseId'])
        url = url.replace(':userId', kwargs['userId'])

    print(f"[GET] {bb_object} URL: {url}")

    res = requests.get(url, headers=headers)

    print(f"=== {bb_object} Response ===\n{res.text}\n")
    return res.json()


def main():
    set_token()
    print(auth)
    print(headers)
    userId = 'userName:mbechtel'
    courseId = 'externalId:LOR-CC-mbechtel'
    user = get_bb_data(api='users', userId=userId)
    print(f"user ID: {user['userName']} email: {user['contact']['email']}\n")
    course = get_bb_data(api='courses', courseId=courseId)
    print(f"course ID: {course['id']} external ID: {course['externalId']}\n")
    memberships = get_bb_data(api='memberships', courseId=courseId)
    print('memberships:', memberships, '\n')
    enrollments = get_bb_data(api='enrollments', userId=userId)
    print('user enrollments:', enrollments, '\n')
    enrollment = get_bb_data(
        api='enrollment', courseId=courseId, userId=userId)
    print('course user enrollment:', enrollment, '\n')

    new_user_data = {
        'externalId': 'devcon19_user',
        'userName': 'devcon19user',
        'name': {
            'given': 'DevCon19',
            'family': 'User'
        },
        'password': '1234',
        'contact': {
            'email': 'no-reply@no.email.here'
        }
    }

    new_user = post_bb_data(api='users', data=new_user_data,
                            remove='/:userId', replace='')
    print('Created new user:', new_user)


if __name__ == '__main__':
    main()
