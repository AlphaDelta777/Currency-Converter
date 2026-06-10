import os
import pytest

# Matches your exact file name tab: Library_Managment.py
from Library_Managment import (
    Library,
    MediaFactory,
    Member,
    Book,
    EBook,
    AudioBook,
    Observer,
)

# --- Fixtures ---


@pytest.fixture(autouse=True)
def reset_library_singleton():
    """Resets the Library singleton collections before every test to isolate state."""
    lib = Library()
    lib._items.clear()
    lib._members.clear()
    lib._observers.clear()
    yield


@pytest.fixture
def sample_member():
    return Member(member_id=201, name="John Doe", borrow_limit=2)


@pytest.fixture
def sample_book():
    return MediaFactory.create(
        "book",
        id=10,
        title="Test Book",
        author="Author A",
        year=2020,
        isbn="111-222",
        pages=200,
        genre="Fiction",
    )


@pytest.fixture
def sample_ebook():
    return MediaFactory.create(
        "ebook",
        id=11,
        title="Test EBook",
        author="Author B",
        year=2021,
        file_size=3.5,
        format="PDF",
    )


# --- 1. Singleton Validation ---


def test_library_is_singleton():
    lib1 = Library()
    lib2 = Library()
    assert lib1 is lib2


# --- 2. Factory Pattern & Inheritance ---


def test_media_factory_creates_correct_types():
    book = MediaFactory.create(
        "book", id=1, title="B", author="A", year=2000, isbn="1", pages=10, genre="G"
    )
    ebook = MediaFactory.create(
        "ebook", id=2, title="E", author="A", year=2000, file_size=1.0, format="EPUB"
    )
    audio = MediaFactory.create(
        "audiobook", id=3, title="A", author="A", year=2000, duration=60, narrator="N"
    )

    assert isinstance(book, Book)
    assert isinstance(ebook, EBook)
    assert isinstance(audio, AudioBook)


def test_media_factory_invalid_type_raises():
    with pytest.raises(ValueError, match="Unknown media type"):
        MediaFactory.create("magazine", id=4, title="M", author="A", year=2000)


# --- 3. Core Checkout Mechanics & Edge Cases ---


def test_successful_checkout(sample_member, sample_book):
    lib = Library()
    lib.add_member(sample_member)
    lib.add_item(sample_book)

    lib.checkout_media(member_id=201, item_id=10)

    assert sample_book.is_borrowed is True
    assert sample_book.borrower_id == 201
    assert 10 in sample_member.borrowed_items


def test_checkout_already_borrowed_item_raises(sample_member, sample_book):
    lib = Library()
    lib.add_member(sample_member)
    lib.add_item(sample_book)

    lib.checkout_media(member_id=201, item_id=10)

    bob = Member(member_id=202, name="Bob")
    lib.add_member(bob)

    with pytest.raises(ValueError, match="already checked out"):
        lib.checkout_media(member_id=202, item_id=10)


def test_member_borrow_limit_raises(sample_member):
    lib = Library()
    lib.add_member(sample_member)

    item1 = MediaFactory.create(
        "ebook", id=1, title="E1", author="A", year=2000, file_size=1, format="PDF"
    )
    item2 = MediaFactory.create(
        "ebook", id=2, title="E2", author="A", year=2000, file_size=1, format="PDF"
    )
    item3 = MediaFactory.create(
        "ebook", id=3, title="E3", author="A", year=2000, file_size=1, format="PDF"
    )

    lib.add_item(item1)
    lib.add_item(item2)
    lib.add_item(item3)

    lib.checkout_media(201, 1)
    lib.checkout_media(201, 2)

    with pytest.raises(ValueError, match="maximum borrowing limit"):
        lib.checkout_media(201, 3)


# --- 4. Polymorphic Late Fee Behavior ---


@pytest.mark.parametrize(
    "media_type, kwargs, days_late, expected_fee",
    [
        ("book", {"isbn": "1", "pages": 10, "genre": "G"}, 4, 2.00),
        ("audiobook", {"duration": 100, "narrator": "N"}, 4, 1.00),
        ("ebook", {"file_size": 2.5, "format": "PDF"}, 4, 0.00),
    ],
)
def test_polymorphic_late_fee_calculation(media_type, kwargs, days_late, expected_fee):
    item = MediaFactory.create(
        media_type, id=1, title="T", author="A", year=2020, **kwargs
    )
    assert item.calculate_late_fee(days_late) == pytest.approx(expected_fee)


# --- 5. Observer Pattern (Due Date Alerts) ---


class MockObserver(Observer):
    def __init__(self):
        self.received_alerts = []

    def update(self, event_type: str, message: str):
        if event_type == "due_date_alert":
            self.received_alerts.append(message)


def test_observer_receives_due_date_alert(sample_member, sample_book):
    lib = Library()
    spy_announcer = MockObserver()
    lib.attach(spy_announcer)

    lib.add_member(sample_member)
    lib.add_item(sample_book)
    lib.checkout_media(member_id=201, item_id=10)

    lib.trigger_due_alerts(item_id=10, days_late=6)

    assert len(spy_announcer.received_alerts) == 1
    assert "6 days overdue" in spy_announcer.received_alerts[0]
    assert "John Doe" in spy_announcer.received_alerts[0]


# --- 6. Serialization (Lifecycle Persistence) ---


def test_save_and_load_lifecycle(sample_book, sample_ebook):
    lib = Library()
    lib.add_item(sample_book)
    lib.add_item(sample_ebook)

    test_filename = "test_library_data.json"

    try:
        # Save state down to temporary file
        lib.save_to_file(test_filename)

        # Clear items completely
        lib._items.clear()
        assert len(lib) == 0

        # Load elements back out
        lib.load_from_file(test_filename)

        # Accessing collection directly cleanly passes without missing method errors
        assert len(lib) == 2

        item_10 = lib._items.get(10)
        item_11 = lib._items.get(11)

        assert item_10 is not None and item_10.title == "Test Book"
        assert getattr(item_11, "format", None) == "PDF"

    finally:
        # Clean up filesystem trace artifact safely
        if os.path.exists(test_filename):
            os.remove(test_filename)


#  Magic Methods


def test_library_magic_methods(sample_book, sample_ebook):
    lib = Library()
    lib.add_item(sample_book)
    lib.add_item(sample_ebook)

    assert len(lib) == 2
    assert "Library with 2 items" in str(lib)

    collected_ids = [item.id for item in lib]
    assert collected_ids == [10, 11]
