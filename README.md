# Ship 3 – Choose Your Project

Welcome to **Ship 3**, the first weekly installment of the final project.  This repository provides three different starter tracks so you can pick a project that interests you:

1. **Choose‑Your‑Own‑Adventure Game** – A text‑based interactive story engine.
2. **Password Manager** – A simple CLI tool for storing and retrieving passwords using encrypted JSON files.
3. **Flashcard Quiz App** – A program to manage flashcards and quiz yourself.

Each track starts with stub functions that raise `NotImplementedError`, but you will begin fleshing them out this week.  You’ll implement basic persistence and one core action for your chosen track so that you have a working foundation for later ships.  Ship 3’s goals are:

## Objectives for Ship 3 (Week of Oct 1 – Oct 6)

1. **Create your own repository.**  Clone this template into your personal GitHub account.  Enable branch protection on `main` and require pull requests to merge.
2. **Choose your project.**  Decide which of the three tracks you want to pursue.  In `project-proposal.md`, describe your choice and what you hope to build.  Mention any stretch goals (e.g. adding graphics to the adventure game, generating random passwords, spaced repetition in the quiz app). Following this, you can delete the other project files that you did not choose.
3. **Practice Git workflow.**  Create a feature branch, make at least two meaningful commits while filling out your proposal and implementing the first feature for your track, then open a pull request back into `main`.  Use descriptive commit messages.
4. **Implement your first feature.**  For Ship 3 you will implement one basic operation and persistence for your chosen track:

   - **CYOA Game:** Read `story.json` file in the `data/` directory with at least two scenes, implement `load_story(file_path)` to parse it, and implement a rudimentary `start_game(story)` that prints the first scene and asks the player for a choice.  Keep the rest of the script as stubs that raise `NotImplementedError`—you will add menu logic and richer story handling in later ships.
   - **Password Manager:** Locate `user_data.json` and `passwords.json` in the `data/` directory.  Implement `register_user(username, master_password)` to hash the master password with `hashlib.sha256` and store it in `user_data.json`.  Implement `add_password(site, username, password)` to append an entry (site, username, password) to `passwords.json` and implement `get_passwords()` to return the list of entries.  Leave login, search and menu features as stubs for future weeks.
   - **Flashcard Quiz App:** Locate `flashcards.json` in the `data/` directory.  Implement `add_flashcard(question, answer)` to append a flashcard to the JSON file and implement `list_flashcards()` to read and display all flashcards.  Leave the quiz loop and menu pieces as stubs that raise `NotImplementedError` until later ships.

5. **Run the code and tests.**  Install dependencies and run the tests with `pytest`.  The tests only verify the existence of stub functions; they will still pass until you update them in later ships.  Use your program manually to confirm your new feature works as expected.

## Project Structure

- `.github/workflows/ci.yml` – GitHub Actions workflow to run your tests on pushes and pull requests.
- `choose_your_own_adventure.py` – Stubs for the adventure game (`load_story`, `start_game`).
- `password_manager.py` – Stubs for the password manager (`register_user`, `add_password`, `get_passwords`).
- `quiz_game.py` – Stubs for the flashcard app (`add_flashcard`, `start_quiz`).
- `tests/` – Minimal tests for each track to verify the stubs exist.  You will expand these tests in future ships.
- `project-proposal.md` – Fill this out during Ship 3 to describe your chosen project.
- `docs/SHIP3_PLAN.md` – This document restates the tasks for Ship 3 and looks ahead to future ships.
- `FINAL_REPORT.md` – Placeholder for your final report at the end of the semester.

## Getting Started

1. Install Python 3.10 or higher and `pip`.
2. Install test dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run each script to see the greeting messages:

   ```bash
   python choose_your_own_adventure.py
   python password_manager.py
   python quiz_game.py
   ```

4. Run the tests:

   ```bash
   pytest
   ```

If all tests pass and you see the greeting messages, your environment is ready.  You can now choose a track and start planning your project.

##how to run:
1. clone this repo
2. run `python password_manager.py` or `python3 password_manager.py`
3. use menu options to add, view, or delete passwords

##example:
Enter master password: ****

Welcome to the Password Manager!

Options:
1. Login
2. Register
3. Add password
4. View passwords
5. Search passwords
6. Edit password
7. Delete password
8. Quit
Choose an option:

> 1
Enter username: shark
Enter master password: shark
Login successful.

> 4
Stored passwords:
2. yahoo | shark | Last updated: 2025-10-26T22:19:31.655625

> 5
Enter site name to search: yahoo
ID 2: yahoo | shark | password: ******** | Last updated: 2025-10-26T22:19:31.655625

## Security Model

1. **Password Encryption:** All stored passwords are encrypted at rest using Fernet symmetric encryption with a key derived from the user's master password via PBKDF2-HMAC-SHA256.
2. **Master Password:** The master password is never stored. It is required at login to derive the encryption key.
3. **Data Integrity:** Password data is versioned, backed up, and verified before writes. Corrupted or tampered files are detected and a backup is used instead.
4. **Input Validation:** All user inputs are sanitized; empty fields and unsafe characters are rejected. Unique identifiers are enforced.
5. **Destructive Actions:** Actions like delete or overwrite require confirmation from the user.

10-Step Demo:
1. Clone the repository
git clone https://github.com/ygadipalli/edge-f25-ship3-yashasree-gadipalli.git

2. Enter the project folder
cd edge-f25-ship3-yashasree-gadipalli

3. Run the password manager
python3 password_manager.py

4. Choose option 2 to register
2

5. Enter a new username
(example)
testuser

6. Enter a master password
(example)
MySecurePass123

7. Run the app again and log in
python3 password_manager.py
Choose:
1
Enter username + master password again

8. After login, choose 1 to add a password
(example entries)
Site: gmail.com
Username: alice
Password: mypassword123

9. Choose 2 from the menu to view saved passwords
Encrypted entries will be shown with IDs.

10. Choose 3 to delete a saved password
Enter the ID to delete (example: 1)
