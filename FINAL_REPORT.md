<!--
This report will be completed during the final ship.  You do not need to edit it until then.
-->

## Final Report

At the end of the semester, summarise your project here.  Include an overview of what you built, challenges you faced, what you learned and future improvements.

**Project Overview:**
For Ship 7, I built a secure and reliable password manager with a command-line interface (CLI). The application allows users to register, log in, store passwords, and manage them safely. Key features include: input validation to prevent malformed data, encryption of sensitive content, integrity checks on files, and safe saving mechanisms with backups. Users can add, list, reveal, edit, and delete passwords, all while keeping their data secure.

**Challenges:**
One of the main challenges was implementing encryption and key derivation correctly while keeping the CLI simple. I also had to carefully manage file integrity and safe saving to avoid accidental data loss. Git workflows added some complexity when pushing branches and recovering work, which taught me how to better handle version control in collaborative projects.

**What I Learned:**
- I gained hands-on experience with:
- Secure password storage using hashing and encryption
- Input validation and error handling in Python CLI applications
- File integrity checks and atomic save operations
- Writing unit and integration tests for security-sensitive code
- Git workflows: feature branches, pull requests, and conflict resolution

**Future Improvements:**
- Add automated password strength checks and suggestions
- Implement a more advanced search and filtering system for stored entries
- Extend encryption support for multi-user collaboration
- Build a graphical interface for improved user experience
- Explore cloud-based syncing while maintaining local encryption for security
