from bbrest import BbRest

key = 'KeyFromBbDevAppRegistration'
secret = 'SecretSquirrel'
bbURL = 'mybb.institution.edu'

def main():
    bb = BbRest(key, secret, bbURL)
    userName = 'inst_bs'
    courseId = 'dev-bs'
    user = bb.GetUser(userId=userName).json()
#     print(user.request.url)
    print(user)
    print(f"\nuser ID: {user['userName']} \
          email: {user['contact']['email']}")
    course = bb.GetCourse(courseId=courseId).json()
    print(f"course ID: {course['id']} \
          external ID: {course['externalId']}")
    memberships = bb.GetCourseMemberships(courseId=courseId).json()
    print('\nmemberships:', memberships)
    enrollments = bb.GetUserMemberships(userId=userName).json()
    print('\nuser enrollments:', enrollments)
    enrollment =bb.GetMembership(courseId=courseId, 
                                 userId=userName).json()
    print('\ncourse user enrollment:', enrollment)   
          
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
    user_name = new_user_data['userName']
    del_user = bb.DeleteUser(user_name)
    print(f'\nDeleted User: {del_user}')
    new_user = bb.CreateUser(payload=new_user_data)
    print('\n Created new user:', new_user.json())

main()