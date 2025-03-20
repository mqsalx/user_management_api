# /src/infrastructure/repository/user_repository.py


from sqlalchemy.orm import Session

from src.core.enums.user_role_enum import UserRoleEnum
from src.infrastructure.models.user_model import UserModel
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()


class UserRepository:
    """
    Class responsible for handling database operations related to user management.

    This repository provides methods for creating, retrieving, and deleting users.

    Class Args:
        db (Session): The database session used for executing queries.
    """

    def __init__(self, db: Session):
        """
        Constructor method for UserRepository.

        Initializes the repository with a database session.

        Args:
            db (Session): The database session used to execute queries.
        """

        self.__database = db

    def create_user(self, **kwargs) -> UserModel:
        """
        Public method responsible for creating a new user in the database.

        This method creates a new `UserModel` instance, persists it in the database,
        and returns the newly created user.

        Args:
            **kwargs: Arbitrary keyword arguments containing user attributes.

        Returns:
            UserModel: The newly created user.

        Raises:
            Exception: If an error occurs while inserting the user into the database.
        """

        try:

            user = UserModel(**kwargs)

            self.__database.add(user)

            self.__database.commit()

            self.__database.refresh(user)

            return user

        except Exception as error:
            self.__database.rollback()
            log.error(f"Error creating user: {error}")
            raise

    def find_user(self, user_id: str) -> UserModel | None:
        """
        Public method responsible for retrieving a user by their user ID.

        This method queries the database to find a user that is not a super administrator.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            UserModel | None: The user matching the user ID if found, otherwise None.
        """

        return (
            self.__database.query(UserModel)
            .filter(
                UserModel.user_id == user_id,
                UserModel.role_id != UserRoleEnum.SUPER_ADMINISTRATOR,
            )
            .first()
        )

    def find_users(self) -> list[UserModel] | None:
        """
        Public method responsible for retrieving all users except super administrators.

        This method queries the database for all users whose role is not `SUPER_ADMINISTRATOR`.

        Args:
            None

        Returns:
            list[UserModel] | None: A list of users or None if no users are found.
        """

        return (
            self.database.query(UserModel)
            .filter(UserModel.role_id != UserRoleEnum.SUPER_ADMINISTRATOR)
            .all()
        )

    def remove_user(self, user: UserModel) -> None:
        """
        Public method responsible for removing a user from the database.

        This method deletes a user and commits the change to the database.

        Args:
            user (UserModel): The user instance to be deleted.

        Raises:
            Exception: If an error occurs while deleting the user.
        """

        try:

            self.__database.delete(user)

            self.__database.commit()

        except Exception as error:
            self.__database.rollback()
            log.error(f"Error removing user: {error}")
            raise

    def find_user_email(self, email: str) -> UserModel:
        """
        Public method responsible for retrieving a user by their email.

        This method queries the database to find a user with the specified email address.

        Args:
            email (str): The email address of the user.

        Returns:
            UserModel | None: The user matching the email if found, otherwise None.
        """

        return (
            self.__database.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

    @property
    def database(self) -> Session:
        """
        Property method responsible for returning the database session.

        This property provides access to the database session used in repository operations.

        Args:
            None

        Returns:
            Session: The database session instance.
        """

        return self.__database
