from random import shuffle

import json


class AccountManager:
    def __init__(self, should_shuffle):
        self.current_index = 0

        with open("keys.json", "r") as fp:
            self.accounts = json.loads(fp.read())

        if should_shuffle:
            self.shuffle_accounts()

    def shuffle_accounts(self):
        shuffle(self.accounts)

    def change_account(self):
        self.current_index += 1
        if self.current_index >= len(self.accounts):
            self.current_index = 0

    def get_account(self):
        return self.accounts[self.current_index]

    def accounts_length(self):
        return len(self.accounts)
