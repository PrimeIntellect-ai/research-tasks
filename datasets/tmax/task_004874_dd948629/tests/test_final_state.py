# test_final_state.py
import os
import subprocess
import pytest

def test_expect_script_exists():
    assert os.path.isfile("/home/user/fetch.exp"), "Expect script /home/user/fetch.exp does not exist."

def test_tarball_extracted():
    assert os.path.isfile("/home/user/mail_data.tar"), "Tarball /home/user/mail_data.tar was not generated."
    assert os.path.isfile("/home/user/mail_data/postfix/main.cf"), "Tarball was not extracted properly to /home/user/mail_data/postfix/main.cf."
    assert os.path.isfile("/home/user/mail_data/dovecot/dovecot.conf"), "Tarball was not extracted properly to /home/user/mail_data/dovecot/dovecot.conf."

def test_c_program_compiled():
    assert os.path.isfile("/home/user/reconstruct.c"), "C program source /home/user/reconstruct.c does not exist."
    assert os.path.isfile("/home/user/reconstruct"), "Compiled C program /home/user/reconstruct does not exist."
    assert os.access("/home/user/reconstruct", os.X_OK), "/home/user/reconstruct is not executable."

def test_links_and_directories():
    assert os.path.isdir("/home/user/live_mail"), "/home/user/live_mail directory does not exist."
    assert os.path.islink("/home/user/live_mail/postfix"), "/home/user/live_mail/postfix is not a symlink."
    assert os.path.islink("/home/user/live_mail/dovecot"), "/home/user/live_mail/dovecot is not a symlink."

def test_symlink_targets():
    target_postfix = os.readlink("/home/user/live_mail/postfix")
    target_dovecot = os.readlink("/home/user/live_mail/dovecot")
    assert target_postfix == "/home/user/mail_data/postfix", f"Symlink for postfix points to {target_postfix}, expected /home/user/mail_data/postfix."
    assert target_dovecot == "/home/user/mail_data/dovecot", f"Symlink for dovecot points to {target_dovecot}, expected /home/user/mail_data/dovecot."

def test_acls():
    postfix_acl = subprocess.run(["getfacl", "/home/user/mail_data/postfix"], capture_output=True, text=True).stdout
    main_cf_acl = subprocess.run(["getfacl", "/home/user/mail_data/postfix/main.cf"], capture_output=True, text=True).stdout

    assert "user:nobody:r-x" in postfix_acl, "ACL for nobody on /home/user/mail_data/postfix is not 'r-x'."
    assert "user:nobody:r--" in main_cf_acl, "ACL for nobody on /home/user/mail_data/postfix/main.cf is not 'r--'."