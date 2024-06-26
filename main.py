from modules.account_manager import AccountManager
from modules.answerthepublic import Answer

def answerthepublic(keywords, project_folder):
    account_manager = AccountManager()
    accounts = account_manager.get_accounts()

    for account in accounts:
        email = account['email']
        password = account['password']
        proxy = account['proxy']

        answer = Answer(project_folder, email, password, proxy, headless=False)

        answer.login()

        for key in keywords:
            answer.parse(key)


def keywordtool():
    pass


if __name__ == '__main__':
    project_name = "Weight Loss Workout"

    keys = [
        'weight loss workout',
    ]

    answerthepublic(keys, project_name)



