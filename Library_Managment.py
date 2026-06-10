from __future__ import annotations

import functools
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type


# 1. ABSTRACT BASE CLASS (MediaItem)
# ==================================
class MediaItem(ABC):
    """Abstract base class for all media types."""

    def __init__(self, id: int, title: str, author: str, year: int):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.is_borrowed = False
        self.borrower_id: Optional[int] = None

    @abstractmethod
    def get_info(self) -> str:
        """Requirement: get_info"""
        pass

    @abstractmethod
    def calculate_late_fee(self, days_late: int) -> float:
        """Requirement: calculate_late_fee"""
        pass

    def checkout(self, member_id: int):
        """Requirement: checkout"""
        if self.is_borrowed:
            raise ValueError(f"'{self.title}' is already checked out.")
        self.is_borrowed = True
        self.borrower_id = member_id

    def return_item(self):
        """Requirement: return (implemented as return_item to avoid keyword clash)"""
        self.is_borrowed = False
        self.borrower_id = None

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> MediaItem:
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, title='{self.title}')"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, title={self.title!r})"


# 2. INHERITANCE: Book, EBook, AudioBook
# ======================================
class Book(MediaItem):
    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        year: int,
        isbn: str,
        pages: int,
        genre: str,
    ):
        super().__init__(id, title, author, year)
        self.isbn = isbn
        self.pages = pages
        self.genre = genre

    def get_info(self) -> str:
        return f"Book: {self.title} by {self.author} ({self.year}) - ISBN: {self.isbn}, Genre: {self.genre}, {self.pages} pages"

    def calculate_late_fee(self, days_late: int) -> float:
        return days_late * 0.50  # $0.50 late fee balance per day

    def to_dict(self) -> dict:
        return {
            "type": "book",
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
            "pages": self.pages,
            "genre": self.genre,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Book:
        data.pop("type", None)
        return cls(**data)


class EBook(MediaItem):
    def __init__(
        self, id: int, title: str, author: str, year: int, file_size: float, format: str
    ):
        super().__init__(id, title, author, year)
        self.file_size = file_size
        self.format = format

    def get_info(self) -> str:
        return f"EBook: {self.title} by {self.author} ({self.year}) - Format: {self.format}, Size: {self.file_size}MB"

    def calculate_late_fee(self, days_late: int) -> float:
        return 0.0  # Digital products do not incur direct physical late penalties

    def to_dict(self) -> dict:
        return {
            "type": "ebook",
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "file_size": self.file_size,
            "format": self.format,
        }

    @classmethod
    def from_dict(cls, data: dict) -> EBook:
        data.pop("type", None)
        return cls(**data)


class AudioBook(MediaItem):
    def __init__(
        self, id: int, title: str, author: str, year: int, duration: int, narrator: str
    ):
        super().__init__(id, title, author, year)
        self.duration = duration
        self.narrator = narrator

    def get_info(self) -> str:
        return f"AudioBook: {self.title} by {self.author} ({self.year}) - Narrated by {self.narrator}, Duration: {self.duration} mins"

    def calculate_late_fee(self, days_late: int) -> float:
        return days_late * 0.25  # $0.25 standard penalty layer per day

    def to_dict(self) -> dict:
        return {
            "type": "audiobook",
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "duration": self.duration,
            "narrator": self.narrator,
        }

    @classmethod
    def from_dict(cls, data: dict) -> AudioBook:
        data.pop("type", None)
        return cls(**data)


# 3. MEMBER CLASS
# ===============
class Member:
    """Tracks borrowed items and borrowing limits."""

    def __init__(self, member_id: int, name: str, borrow_limit: int = 3):
        self.member_id = member_id
        self.name = name
        self.borrow_limit = borrow_limit
        self.borrowed_items: List[int] = []

    def can_borrow(self) -> bool:
        return len(self.borrowed_items) < self.borrow_limit

    def borrow_item(self, item_id: int):
        if not self.can_borrow():
            raise ValueError(
                f"Member {self.name} has hit their maximum borrowing limit!"
            )
        self.borrowed_items.append(item_id)

    def return_item(self, item_id: int):
        if item_id in self.borrowed_items:
            self.borrowed_items.remove(item_id)


# 4. DECORATOR FOR LOGGING
# ========================
def log_operation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__} with args={args[1:]}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} completed")
        return result

    return wrapper


# 5. CONTEXT MANAGER FOR SAFE FILE HANDLING
# =========================================
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


# 6. FACTORY PATTERN
# ==================
class MediaFactory:
    _type_map: Dict[str, Type[MediaItem]] = {
        "book": Book,
        "ebook": EBook,
        "audiobook": AudioBook,
    }

    @staticmethod
    def create(media_type: str, **kwargs) -> MediaItem:
        cls = MediaFactory._type_map.get(media_type.lower())
        if cls is None:
            raise ValueError(f"Unknown media type: {media_type}")
        return cls(**kwargs)


# 7. OBSERVER PATTERN (Alert Notification System)
# ===============================================
class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, message: str):
        pass


class DueDateAlertSystem(Observer):
    """Requirement: Observer pattern for due date alerts"""

    def update(self, event_type: str, message: str):
        if event_type == "due_date_alert":
            print(f"[NOTIFY - ALERT] {message}")


# 8. SINGLETON LIBRARY
# ====================
class Library:
    _instance: Optional["Library"] = None
    _items: Dict[int, MediaItem]
    _members: Dict[int, Member]
    _observers: List[Observer]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._items = {}
            cls._instance._members = {}
            cls._instance._observers = []
        return cls._instance

    def get_item(self, item_id: int) -> Optional[MediaItem]:
        """Retrieves an item from the library catalog by its ID."""
        return self._items.get(item_id)

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def _notify(self, event_type: str, message: str):
        for obs in self._observers:
            obs.update(event_type, message)

    def add_member(self, member: Member):
        self._members[member.member_id] = member

    @log_operation
    def add_item(self, item: MediaItem):
        self._items[item.id] = item

    @log_operation
    def checkout_media(self, member_id: int, item_id: int):
        member = self._members.get(member_id)
        item = self._items.get(item_id)

        if not member or not item:
            raise ValueError("Invalid Member ID or Item ID setup.")

        item.checkout(member_id)
        member.borrow_item(item_id)

    @log_operation
    def return_media(self, member_id: int, item_id: int):
        member = self._members.get(member_id)
        item = self._items.get(item_id)

        if member and item:
            item.return_item()
            member.return_item(item_id)

    # Trigger_due_alerts was a stray top-level function — moved inside Library
    def trigger_due_alerts(self, item_id: int, days_late: int):
        """Simulates checking dates and firing alerts if an item is late."""
        item = self._items.get(item_id)

        if item and item.is_borrowed:
            b_id = getattr(item, "borrower_id", None)
            if b_id is not None:
                member = self._members.get(b_id)
                if member:
                    fee = item.calculate_late_fee(days_late)
                    msg = f"Item '{item.title}' is {days_late} days overdue! Member: {member.name}. Late Fee: ${fee:.2f}"
                    self._notify("due_date_alert", msg)

    @log_operation
    def save_to_file(self, filename: str):
        data = [item.to_dict() for item in self._items.values()]
        with JsonFileManager(filename, "w") as f:
            json.dump(data, f, indent=2)

    # Item_data directly to create(), which would pass "type" to the constructor
    @log_operation
    def load_from_file(self, filename: str):
        with JsonFileManager(filename, "r") as f:
            data = json.load(f)
        self._items.clear()
        for item_data in data:
            media_type = item_data.get("type")
            cls = MediaFactory._type_map.get(media_type)
            if cls is None:
                raise ValueError(f"Unknown media type in file: {media_type}")
            item = cls.from_dict(
                dict(item_data)
            )  # copy so original dict is not mutated
            self._items[item.id] = item

    # All magic methods were dedented out of Library — moved back inside
    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items.values())

    def __str__(self):
        return f"Library with {len(self)} items"

    def __repr__(self):
        return f"Library(items={list(self._items.values())!r})"


# 9. POLYMORPHISM DEMO
# ====================
def print_catalog(library: Library):
    print("\n=== Catalog ===")
    for item in library:
        print(item.get_info())
    print("================\n")


# 10. RUNNING THE COMPLETE SYSTEM
# ===============================
if __name__ == "__main__":
    lib = Library()

    # Attach our explicit Alert Observer system
    alert_system = DueDateAlertSystem()
    lib.attach(alert_system)

    # Register a Member
    alice = Member(member_id=101, name="Alice Smith", borrow_limit=2)
    lib.add_member(alice)

    # Use Factory to build media with explicitly specified attributes
    book1 = MediaFactory.create(
        "book",
        id=1,
        title="Clean Code",
        author="Robert C. Martin",
        year=2008,
        isbn="978-0132350884",
        pages=464,
        genre="Tech",
    )
    ebook1 = MediaFactory.create(
        "ebook",
        id=2,
        title="Fluent Python",
        author="Luciano Ramalho",
        year=2015,
        file_size=5.2,
        format="EPUB",
    )
    audio1 = MediaFactory.create(
        "audiobook",
        id=3,
        title="The Pragmatic Programmer",
        author="Andrew Hunt & David Thomas",
        year=1999,
        duration=480,
        narrator="John Doe",
    )

    lib.add_item(book1)
    lib.add_item(ebook1)
    lib.add_item(audio1)

    # Display working polymorphism tracking
    print_catalog(lib)

    # Checkout and Alert Notification testing suite execution
    print(f"Can Alice borrow items? {alice.can_borrow()}")
    lib.checkout_media(member_id=101, item_id=1)

    # Trigger Observer Alert Demo (5 days late tracking)
    lib.trigger_due_alerts(item_id=1, days_late=5)

    # Save and Clean Load collection state persistence validation
    lib.save_to_file("library_state.json")
    lib.load_from_file("library_state.json")