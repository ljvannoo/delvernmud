#!/usr/bin/env python3

from src.entities.account import Account

salt = b'\x1cE\xaa\xefQ\xaa\xee\x856\x95W\xde\x167\x1d\xc8\x0b\x02\x8a\xe8\xb18\x8c\xb6\x95\x8e\x9c\xf5\xbd\x9eq.'
password = 'fake_password_123!'

account = Account()
account.password_hash = account.hash(salt, password)

print(account.password_hash)
# 00d83df728d961e19ddb3e47470e7320d92edcb6c600ea37f55125c0e2ee4427f1b50b1069ecdbb626715de4b2ed7ad4389fa5124133d99f36208de5cc72db08
