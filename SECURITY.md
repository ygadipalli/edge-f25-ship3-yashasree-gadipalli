This project is a beginner CLI password manager. It includes basic security but is not meant for sensitive real-world data.

What is protected:
- The master password is hashed with SHA-256 before being stored.
- All saved passwords are encrypted using a key derived from the master password with PBKDF2 (SHA-256, 100k iterations).
- A salt is stored separately in salt.bin.
- Passwords are stored in encrypted form in passwords.json.

Validation included:
- Usernames, site names, and passwords cannot be empty.
- IDs for retrieval and deletion must be numbers and must exist.
- Files are checked for missing or invalid JSON.

What is not protected (known limits):
- Only one user is supported.
- No defense against brute-force attacks or malware.
- Salt is stored locally, which is not ideal for production.
- Anyone with folder access can delete or replace the files.
