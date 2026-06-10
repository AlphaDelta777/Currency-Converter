from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type
import json
import functools
from datetime import datetime, datetime as dt

# =========================
# Decorator for logging
# =========================

def log_operation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__} with args={args[1:]}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} completed")
        return result
    return wrapper


# =========================
# Context manager for JSON files
# =========================

class JsonFileManager:
    def __init__(self, filename: str, mode: str):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc, tb):
        if self.file:
            self.file.close()
        return False


# =========================
# Abstract base + media types
# =========================

class MediaItem(ABC):
    def __init__(self, item_id: int, title: str, author: str, year: int, daily_late_fee: float = 0.50):
        self.id = item_id
        self.title = title
        self.author = author
        self.year = year
        self.daily_late_fee = daily_late_fee
        self.is_checked_out: bool = False
        self.current_borrower_id: Optional[int] = None
        self.due_date: Optional[str] = None  # Stored as YYYY-MM-DD ISO string

    @abstractmethod
    def get_info(self) -> str:
        """Polymorphic string summary representing the specific media item type details."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> MediaItem:
        pass

    def checkout(self, member_id: int, due_date_str: str) -> None:
        if self.is_checked_out:
            raise ValueError(f"'{self.title}' is already checked out.")
        self.is_checked_out = True
        self.current_borrower_id = member_id
        self.due_date = due_date_str

    def return_item(self) -> float:
        """Returns the item and calculates any late fees up to today's date."""
        if not self.is_checked_out:
            return 0.0
        
        late_fee = self.calculate_late_fee()
        self.is_checked_out = False
        self.current_borrower_id = None
        self.due_date = None
        return late_fee

    def calculate_late_fee(self) -> float:
        if not self.is_checked_out or not self.due_date:
            return 0.0
        
        try:
            due = dt.strptime(self.due_date, "%Y-%m-%d").date()
            today = dt.today().date()
            if today > due:
                days_late = (today - due).days
                return max(0.0, days_late * self.daily_late_fee)
        except ValueError:
            pass
        return 0.0

    def __str__(self) -> str:
        status = f"Checked out to Member {self.current_borrower_id}" if self.is_checked_out else "Available"
        return f"{self.__class__.__name__}(id={self.id}, title='{self.title}', Status={status})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, title={self.title!r})"


class Book(MediaItem):
    def __init__(self, item_id: int, title: str, author: str, year: int, isbn: str, pages: int, genre: str):
        super().__init__(item_id, title, author, year, daily_late_fee=0.50)
        self.isbn = isbn
        self.pages = pages
        self.genre = genre

    def get_info(self) -> str:
        return f"Book [ISBN: {self.isbn}]: {self.title} by {self.author} ({self.year}) - Genre: {self.genre}, {self.pages} pages"

    def to_dict(self) -> dict:
        return {
            "type": "book", "id": self.id, "title": self.title, "author": self.author, "year": self.year,
            "isbn": self.isbn, "pages": self.pages, "genre": self.genre,
            "is_checked_out": self.is_checked_out, "current_borrower_id": self.current_borrower_id, "due_date": self.due_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> Book:
        obj = cls(data["id"], data["title"], data["author"], data["year"], data["isbn"], data["pages"], data["genre"])
        obj.is_checked_out = data.get("is_checked_out", False)
        obj.current_borrower_id = data.get("current_borrower_id")
        obj.due_date = data.get("due_date")
        return obj


class EBook(MediaItem):
    def __init__(self, item_id: int, title: str, author: str, year: int, file_size: str, format: str):
        super().__init__(item_id, title, author, year, daily_late_fee=0.10) # Lower fee for digital assets
        self.file_size = file_size
        self.format = format

    def get_info(self) -> str:
        return f"EBook: {self.title} by {self.author} ({self.year}) - Size: {self.file_size}, Format: {self.format}"

    def to_dict(self) -> dict:
        return {
            "type": "ebook", "id": self.id, "title": self.title, "author": self.author, "year": self.year,
            "file_size": self.file_size, "format": self.format,
            "is_checked_out": self.is_checked_out, "current_borrower_id": self.current_borrower_id, "due_date": self.due_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> EBook:
        obj = cls(data["id"], data["title"], data["author"], data["year"], data["file_size"], data["format"])
        obj.is_checked_out = data.get("is_checked_out", False)
        obj.current_borrower_id = data.get("current_borrower_id")
        obj.due_date = data.get("due_date")
        return obj


class AudioBook(MediaItem):
    def __init__(self, item_id: int, title: str, author: str, year: int, duration: int, narrator: str):
        super().__init__(item_id, title, author, year, daily_late_fee=0.25)
        self.duration = duration
        self.narrator = narrator

    def get_info(self) -> str:
        return f"AudioBook: {self.title} by {self.author} ({self.year}) - Length: {self.duration} mins, Narrator: {self.narrator}"

    def to_dict(self) -> dict:
        return {
            "type": "audiobook", "id": self.id, "title": self.title, "author": self.author, "year": self.year,
            "duration": self.duration, "narrator": self.narrator,
            "is_checked_out": self.is_checked_out, "current_borrower_id": self.current_borrower_id, "due_date": self.due_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> AudioBook:
        obj = cls(data["id"], data["title"], data["author"], data["year"], data["duration"], data["narrator"])
        obj.is_checked_out = data.get("is_checked_out", False)
        obj.current_borrower_id = data.get("current_borrower_id")
        obj.due_date = data.get("due_date")
        return obj


# =========================
# Factory for media creation
# =========================

class MediaFactory:
    _type_map: Dict[str, Type[MediaItem]] = {
        "book": Book,
        "ebook": EBook,
        "audiobook": AudioBook,
    }

    @staticmethod
    def create(media_type: str, **kwargs) -> MediaItem:
        media_type = media_type.lower()
        cls = MediaFactory._type_map.get(media_type)
        if cls is None:
            raise ValueError(f"Unknown media type: {media_type}")
        
        if "id" in kwargs and "item_id" not in kwargs:
            return cls.from_dict(kwargs)
            
        return cls(**kwargs)


# =========================
# Member Entity Class
# =========================

class Member:
    def __init__(self, member_id: int, name: str, borrowing_limit: int = 3):
        self.member_id = member_id
        self.name = name
        self.borrowing_limit = borrowing_limit
        self.borrowed_items: List[int] = []  # Tracks List of MediaItem IDs

    def can_borrow(self) -> bool:
        return len(self.borrowed_items) < self.borrowing_limit

    def borrow_item(self, item_id: int):
        if not self.can_borrow():
            raise ValueError(f"Member {self.name} has hit their max limit of {self.borrowing_limit} items.")
        if item_id not in self.borrowed_items:
            self.borrowed_items.append(item_id)

    def return_item(self, item_id: int):
        if item_id in self.borrowed_items:
            self.borrowed_items.remove(item_id)

    def __str__(self) -> str:
        return f"Member: {self.name} (ID: {self.member_id}) - Borrowed: {len(self.borrowed_items)}/{self.borrowing_limit}"


# =========================
# Observer pattern (Notification System)
# =========================

class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, message: str, item: Optional[MediaItem] = None):
        pass


class DueDateAlertSystem(Observer):
    def update(self, event_type: str, message: str, item: Optional[MediaItem] = None):
        print(f"[NOTIFICATION ALERT - {event_type.upper()}]: {message}")
        if item and item.due_date:
            print(f"    ↳ Action Item: '{item.title}' is flagged. Due Date was: {item.due_date}")


# =========================
# Singleton Library
# =========================

class Library:
    _instance: Optional[Library] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._items: Dict[int, MediaItem] = {}
            self._members: Dict[int, Member] = {}
            self._observers: List[Observer] = []
            self._initialized = True

    # --- Observer Management ---
    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def _notify(self, event_type: str, message: str, item: Optional[MediaItem] = None):
        for obs in self._observers:
            obs.update(event_type, message, item)

    # --- Core Operations ---
    def add_item(self, item: MediaItem):
        self._items[item.id] = item

    def register_member(self, member: Member):
        self._members[member.member_id] = member

    @log_operation
    def checkout_item(self, member_id: int, item_id: int, due_date_str: str):
        member = self._members.get(member_id)
        item = self._items.get(item_id)

        if not member:
            raise ValueError(f"Member ID {member_id} not found.")
        if not item:
            raise ValueError(f"Media item ID {item_id} not found.")
        
        # Validates member limitations and asset states
        member.borrow_item(item.id)
        try:
            item.checkout(member_id, due_date_str)
            self._notify("checkout", f"{member.name} checked out '{item.title}'", item)
        except ValueError as e:
            # Rollback member transaction if media processing fails
            member.return_item(item.id)
            raise e

    @log_operation
    def return_library_item(self, item_id: int):
        item = self._items.get(item_id)
        if not item:
            raise ValueError(f"Media item ID {item_id} not found.")
        
        if not item.is_checked_out:
            print(f"Item '{item.title}' is already safe inside the library.")
            return

        member = self._members.get(item.current_borrower_id)
        late_fee = item.return_item()
        
        if member:
            member.return_item(item.id)
            
        if late_fee > 0:
            self._notify("overdue_alert", f"Late fee accumulated for {member.name if member else 'Unknown'}: ${late_fee:.2f}", item)
        else:
            self._notify("return", f"Item '{item.title}' returned successfully with no outstanding balances.", item)

    def check_for_due_date_alerts(self):
        """Scans checked-out media arrays to broadcast global system alerts for late items."""
        today = dt.today().date()
        for item in self._items.values():
            if item.is_checked_out and item.due_date:
                due = dt.strptime(item.due_date, "%Y-%m-%d").date()
                if today > due:
                    member = self._members.get(item.current_borrower_id)
                    name = member.name if member else f"ID {item.current_borrower_id}"
                    self._notify("due_date_overdue", f"CRITICAL: '{item.title}' borrowed by {name} is past due!", item)

    # --- Serialization ---
    @log_operation
    def save_state(self, filename: str):
        serialized_items = [item.to_dict() for item in self._items.values()]
        serialized_members = [
            {"member_id": m.member_id, "name": m.name, "borrowing_limit": m.borrowing_limit, "borrowed_items": m.borrowed_items}
            for m in self._members.values()
        ]
        
        payload = {"items": serialized_items, "members": serialized_members}
        with JsonFileManager(filename, "w") as f:
            json.dump(payload, f, indent=2)

    @log_operation
    def load_state(self, filename: str):
        with JsonFileManager(filename, "r") as f:
            payload = json.load(f)
            
        self._items.clear()
        self._members.clear()

        # Re-build items via factory routing
        for item_data in payload.get("items", []):
            m_type = item_data.pop("type")
            item = MediaFactory.create(m_type, **item_data)
            self._items[item.id] = item

        # Re-build member structures
        for mem_data in payload.get("members", []):
            member = Member(mem_data["member_id"], mem_data["name"], mem_data["borrowing_limit"])
            member.borrowed_items = mem_data["borrowed_items"]
            self._members[member.member_id] = member
            
        self._notify("system_load", "Library management data state successfully sync'd from persistent disk storage.")

    # --- Magic Methods ---
    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items.values())

    def __str__(self) -> str:
        return f"Library Catalog Inventory: {len(self)} items dynamically cataloged."


if __name__ == "__main__":
    library = Library()

    alert_handler = DueDateAlertSystem()
    library.attach(alert_handler)

    alice = Member(member_id=101, name="Alice Smith", borrowing_limit=2)
    bob = Member(member_id=102, name="Bob Jones", borrowing_limit=5)
    library.register_member(alice)
    library.register_member(bob)

    book1 = MediaFactory.create("book", item_id=1, title="Design Patterns", author="Gang of Four", year=1994, isbn="978-0201633610", pages=395, genre="Software Engineering")
    ebook1 = MediaFactory.create("ebook", item_id=2, title="Refactoring", author="Martin Fowler", year=1999, file_size="12MB", format="EPUB")
    audio1 = MediaFactory.create("audiobook", item_id=3, title="Code Complete", author="Steve McConnell", year=2004, duration=2400, narrator="Mike DelGaudio")

    library.add_item(book1)
    library.add_item(ebook1)
    library.add_item(audio1)

    print("\n--- Initial Catalog Assessment (Polymorphism) ---")
    for asset in library:
        print(asset.get_info())

    print("\n--- Processing Core Operational Borrow Flows ---")
    library.checkout_item(member_id=101, item_id=1, due_date_str="2026-06-01") # Let's simulate that this was due a few days ago
    
    library.checkout_item(member_id=101, item_id=2, due_date_str="2026-06-20") 
    
    print(alice) # Verify limit metrics

    try:
        library.checkout_item(member_id=101, item_id=3, due_date_str="2026-07-01")
    except ValueError as error:
        print(f"[EXPECTED EXCEPTION]: {error}")

    print("\n--- Triggering Automatic System Audits (Observer Alerts) ---")
    
    library.check_for_due_date_alerts()
    print("\n--- Processing Return Protocols ---")

    library.return_library_item(item_id=1)
    print("\n--- Executing Persistent Data Storage Actions ---")
    library.save_state("library_vault.json")

    library._items.clear()
    library._members.clear()
    print(f"Memory reset metrics: Catalog size = {len(library)}, Registered Members = {len(library._members)}")

    library.load_state("library_vault.json")
    print(f"Memory reconstruction complete: Loaded items length = {len(library)}")
    
   