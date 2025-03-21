# /src/usecases/user/update_user_use_case.py

from typing import Dict

from sqlalchemy.orm import Session

from src.core.dtos.user_dto import UpdateUserRequestDTO
from src.core.exceptions.base_exception import BaseException
from src.core.exceptions.user_exception import UserNotFoundException
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.repository.user_repository import UserRepository
from src.utils.logger_util import LoggerUtil

log = LoggerUtil()


class UpdateUserUseCase:
    """
    Class responsible for handling the user update use case.

    This class updates an existing user with only the provided fields.

    Class Args:
        db (Session): The database session required for executing queries.
    """

    def __init__(self, db: Session):
        """
        Constructor method for UpdateUserUseCase.

        Initializes the use case with a database session and a repository instance.

        Args:
            db (Session): The database session used to execute queries.
        """

        self.__repository = UserRepository(db)

    def update(
        self, user_id: str, request: UpdateUserRequestDTO
    ) -> dict[str, str]:
        """
        Public method responsible for updating a user.

        This method updates only the fields provided in the request DTO.
        If the user ID is invalid or does not exist, an exception is raised.

        Args:
            user_id (str): The unique identifier of the user to update.
            request (UpdateUserRequestDTO): The DTO containing the fields to update.

        Returns:
            Dict[str, str]: A dictionary containing the updated user details.

        Raises:
            UserNotFoundException: If the user ID is invalid or not found.
            Exception: If an unexpected error occurs during the update process.
        """

        try:
            if not user_id:
                raise UserNotFoundException(
                    f"User with ID {user_id} is invalid or incorrect!"
                )

            user = self.__repository.find_user(user_id)

            if not user:
                raise UserNotFoundException(
                    f"User with ID {user_id} is invalid or incorrect!"
                )

            update_data = request.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                if hasattr(user, field):
                    setattr(user, field, value)

            self.__repository.database.commit()
            self.__repository.database.refresh(user)

            return self.__response(user)

        except (Exception, BaseException) as error:
            self.__repository.database.rollback()
            log.error(f"Error during the user update process: {error}")
            raise error

    def __response(self, user: UserModel) -> Dict[str, str]:
        """
        Private method responsible for formatting the updated user response.

        Args:
            user (UserModel): The updated user instance.

        Returns:
            Dict[str, str]: A dictionary containing the user ID, name, and email.
        """

        return {
            "user_id": str(user.user_id),
            "name": str(user.name),
            "email": str(user.email),
        }
