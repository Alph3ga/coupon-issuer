import mongomock
import pytest
from mongoengine import connect, disconnect
from mongoengine.errors import DoesNotExist

from src.datastore.user import createUser, getUserByFlatNumber, getUserByUserId
from src.dtos.user import UserDTO
from src.models.user import User


@pytest.fixture(scope="function", autouse=True)
def mock_db():
    connect("testdb", mongo_client_class=mongomock.MongoClient)
    yield
    disconnect()


@pytest.fixture
def sample_user_dto():
    return UserDTO(
        userId="testuser",
        name="John",
        phoneNumber="9876543210",
        flatNumber="12B",
        hashedPass=b"fakehash",
        isAdmin=False,
    )


def test_create_user(sample_user_dto):
    createUser(sample_user_dto)
    user = User.objects.get(userId="testuser")
    assert user.name == "John"
    assert user.flatNumber == "12B"
    assert user.phoneNumber == "9876543210"
    assert user.isAdmin is False
    assert user.deleted is False


def test_get_user_by_user_id_success(sample_user_dto):
    createUser(sample_user_dto)
    dto = getUserByUserId("testuser")
    assert isinstance(dto, UserDTO)
    assert dto.name == "John"
    assert dto.flatNumber == "12B"


def test_get_user_by_flat_number_success(sample_user_dto):
    createUser(sample_user_dto)
    dto = getUserByFlatNumber("12B")
    assert isinstance(dto, UserDTO)
    assert dto.userId == "testuser"


def test_get_user_by_user_id_not_found():
    with pytest.raises(DoesNotExist):
        getUserByUserId("nonexistent")


def test_get_user_by_flat_number_not_found():
    with pytest.raises(DoesNotExist):
        getUserByFlatNumber("X-404")
