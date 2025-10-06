<!--
Fill out this document during Ship 3.
Describe which project track you are choosing (adventure game, password manager, or quiz app) and outline your ideas.
-->

## Project Proposal

**Chosen Track:** Password Manager

### Description

A command-line tool for securely storing and retrieving passwords. It solves the problem of managing multiple accounts by keeping credentials in an encrypted JSON file, so users don’t need to remember every password. Users interact with the program through CLI commands to add, view, or update entries. Data is encrypted with a master password, and ensures that sensitive information remains protected even if the file is accessed directly.

### Planned Features

- Master Password Authentication – Require the user to register and log in with a master password to unlock access to stored credentials.

- Add New Passwords – Allow users to securely add account credentials (site, username, password) to the encrypted JSON file.

- Retrieve Stored Passwords – Provide a way to search for and view saved passwords after successful authentication.

### Stretch Goals

- Adding a password generator that makes random strong passwords for the user.
- Add a lockout after 3 wrong attempts at the master password.