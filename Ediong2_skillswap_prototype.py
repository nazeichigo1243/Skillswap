import time

class Notification:

    def __init__(self, message):
        self.message = message

    def display(self):
        print(f"[Notification] {self.message}")


class RequestNotification(Notification):

    def __init__(self, sender_name, skill_name):
        super().__init__(f"{sender_name} sent you a request for '{skill_name}'")


class RatingNotification(Notification):

    def __init__(self, rater_name, stars):
        super().__init__(f"{rater_name} rated you {stars} star(s)")


class Skill:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class User:
    def __init__(self, username, password):
        self.username = username
        self.__password = password          
        self.full_name = ""
        self.bio = ""
        self.skills_to_teach = []
        self.skills_to_learn = []
        self.ratings = []                   
        self.notifications = []

    def check_password(self, password):
        return self.__password == password

    def add_skill_to_teach(self, skill_name):
        self.skills_to_teach.append(Skill(skill_name))

    def add_skill_to_learn(self, skill_name):
        self.skills_to_learn.append(Skill(skill_name))

    def receive_notification(self, notification):
        self.notifications.append(notification)

    def average_rating(self):
        if not self.ratings:
            return "No ratings yet"
        return round(sum(self.ratings) / len(self.ratings), 1)

    def profile_summary(self):
        teach = ", ".join(str(s) for s in self.skills_to_teach) or "None yet"
        learn = ", ".join(str(s) for s in self.skills_to_learn) or "None yet"
        return (
            f"\n--- {self.username}'s Profile ---\n"
            f"Name          : {self.full_name or 'Not set'}\n"
            f"Bio           : {self.bio or 'Not set'}\n"
            f"Can teach     : {teach}\n"
            f"Wants to learn: {learn}\n"
            f"Rating        : {self.average_rating()}\n"
        )


class ExchangeRequest:
    STATUS_PENDING = "Pending"
    STATUS_ACCEPTED = "Accepted"
    STATUS_DECLINED = "Declined"
    STATUS_COMPLETED = "Completed"

    def __init__(self, sender, receiver, skill_name):
        self.sender = sender
        self.receiver = receiver
        self.skill_name = skill_name
        self.status = self.STATUS_PENDING

    def accept(self):
        self.status = self.STATUS_ACCEPTED

    def decline(self):
        self.status = self.STATUS_DECLINED

    def complete(self):
        self.status = self.STATUS_COMPLETED

    def __str__(self):
        return (f"[{self.status}] {self.sender.username} -> {self.receiver.username} "
                f"(skill: {self.skill_name})")


# ----------------------------------------------------------------------
# SkillSwapApp -> the main controller that drives navigation (ABSTRACTION)
# ----------------------------------------------------------------------
class SkillSwapApp:
    def __init__(self):
        self.users = {}           
        self.requests = []         
        self.current_user = None
        self.running = True
        self._seed_demo_data()     

    def _seed_demo_data(self):
        alice = User("alice", "1234")
        alice.full_name = "Alice Santos"
        alice.bio = "Freelance graphic designer."
        alice.add_skill_to_teach("Graphic Design")
        alice.add_skill_to_learn("Python Programming")

        bob = User("bob", "1234")
        bob.full_name = "Bob Cruz"
        bob.bio = "CS student who loves coding."
        bob.add_skill_to_teach("Python Programming")
        bob.add_skill_to_learn("Graphic Design")

        self.users["alice"] = alice
        self.users["bob"] = bob

    def start(self):
        print("=" * 50)
        print("   Welcome to SkillSwap - Skill Exchange Platform")
        print("=" * 50)
        time.sleep(0.5)
        while self.running:
            if self.current_user is None:
                self.main_menu()
            else:
                self.dashboard_menu()

    def main_menu(self):
        print("\n--- MAIN MENU ---")
        print("1. Register")
        print("2. Log in")
        print("3. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            self.register()
        elif choice == "2":
            self.login()
        elif choice == "3":
            self.running = False
            print("Goodbye!")
        else:
            print("Invalid option, try again.")

    def register(self):
        print("\n--- REGISTER ---")
        username = input("Choose a username: ").strip()
        if username in self.users:
            print("Username already taken.")
            return
        password = input("Choose a password: ").strip()
        self.users[username] = User(username, password)
        print(f"Account created for '{username}'. Please log in.")

    def login(self):
        print("\n--- LOG IN ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        user = self.users.get(username)
        if user and user.check_password(password):
            self.current_user = user
            print(f"Login successful. Welcome, {username}!")
        else:
            print("Invalid username or password.")

    def dashboard_menu(self):
        print(f"\n--- DASHBOARD ({self.current_user.username}) ---")
        print("1. View / Update Profile")
        print("2. Add Skill to Teach")
        print("3. Add Skill to Learn")
        print("4. Browse Users by Skill")
        print("5. Send Exchange Request")
        print("6. View & Respond to Incoming Requests")
        print("7. Mark an Exchange as Completed")
        print("8. Leave a Rating")
        print("9. Log out")
        choice = input("Select an option: ").strip()

        actions = {
            "1": self.update_profile,
            "2": self.add_skill_to_teach,
            "3": self.add_skill_to_learn,
            "4": self.browse_users,
            "5": self.send_request,
            "6": self.respond_to_request,
            "7": self.complete_exchange,
            "8": self.leave_rating,
            "9": self.logout,
        }
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option, try again.")

    def update_profile(self):
        user = self.current_user
        print(user.profile_summary())
        print("Leave blank to keep current value.")
        name = input("Full name: ").strip()
        bio = input("Short bio: ").strip()
        if name:
            user.full_name = name
        if bio:
            user.bio = bio
        print("Profile updated.")

    def add_skill_to_teach(self):
        skill = input("Skill you can teach: ").strip()
        if skill:
            self.current_user.add_skill_to_teach(skill)
            print(f"Added '{skill}' to skills you can teach.")

    def add_skill_to_learn(self):
        skill = input("Skill you want to learn: ").strip()
        if skill:
            self.current_user.add_skill_to_learn(skill)
            print(f"Added '{skill}' to skills you want to learn.")

    def browse_users(self):
        keyword = input("Search skill keyword (blank = show all): ").strip().lower()
        print("\n--- SEARCH RESULTS ---")
        found = False
        for username, user in self.users.items():
            if user is self.current_user:
                continue
            teach_names = [s.name.lower() for s in user.skills_to_teach]
            if not keyword or any(keyword in name for name in teach_names):
                found = True
                teach = ", ".join(str(s) for s in user.skills_to_teach) or "None"
                print(f"- {username} | teaches: {teach} | rating: {user.average_rating()}")
        if not found:
            print("No matching users found.")

    def send_request(self):
        target_name = input("Username to request from: ").strip()
        target = self.users.get(target_name)
        if not target or target is self.current_user:
            print("User not found.")
            return
        skill = input("Skill you want from them: ").strip()
        request = ExchangeRequest(self.current_user, target, skill)
        self.requests.append(request)
        target.receive_notification(
            RequestNotification(self.current_user.username, skill)
        )
        print(f"Request sent to {target_name} for skill '{skill}'.")

    def respond_to_request(self):
        incoming = [r for r in self.requests
                    if r.receiver is self.current_user and r.status == ExchangeRequest.STATUS_PENDING]
        if not incoming:
            print("No pending incoming requests.")
            return

        print("\n--- INCOMING REQUESTS ---")
        for i, r in enumerate(incoming, start=1):
            print(f"{i}. {r}")

        try:
            idx = int(input("Select request number to respond to: ")) - 1
            chosen = incoming[idx]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return

        decision = input("Accept or Decline? (a/d): ").strip().lower()
        if decision == "a":
            chosen.accept()
            print("Request accepted.")
        elif decision == "d":
            chosen.decline()
            print("Request declined.")
        else:
            print("Invalid choice.")

    def complete_exchange(self):
        active = [r for r in self.requests
                  if (r.sender is self.current_user or r.receiver is self.current_user)
                  and r.status == ExchangeRequest.STATUS_ACCEPTED]
        if not active:
            print("No accepted exchanges ready to complete.")
            return

        print("\n--- ACCEPTED EXCHANGES ---")
        for i, r in enumerate(active, start=1):
            print(f"{i}. {r}")

        try:
            idx = int(input("Select exchange to mark as completed: ")) - 1
            chosen = active[idx]
            chosen.complete()
            print("Exchange marked as completed. You may now leave a rating.")
        except (ValueError, IndexError):
            print("Invalid selection.")

    def leave_rating(self):
        completed = [r for r in self.requests
                     if (r.sender is self.current_user or r.receiver is self.current_user)
                     and r.status == ExchangeRequest.STATUS_COMPLETED]
        if not completed:
            print("No completed exchanges to rate yet.")
            return

        print("\n--- COMPLETED EXCHANGES ---")
        for i, r in enumerate(completed, start=1):
            print(f"{i}. {r}")

        try:
            idx = int(input("Select exchange to rate: ")) - 1
            chosen = completed[idx]
            other_user = chosen.receiver if chosen.sender is self.current_user else chosen.sender
            stars = int(input(f"Rate {other_user.username} (1-5 stars): "))
            feedback = input("Leave a short feedback comment: ").strip()
            other_user.ratings.append(stars)
            other_user.receive_notification(
                RatingNotification(self.current_user.username, stars)
            )
            print(f"Thanks! You rated {other_user.username} {stars} stars.")
            if feedback:
                print(f"Feedback recorded: \"{feedback}\"")
        except (ValueError, IndexError):
            print("Invalid input.")

    def logout(self):
        print(f"Logging out {self.current_user.username}...")
        self.current_user = None

if __name__ == "__main__":
    app = SkillSwapApp()
    app.start()
