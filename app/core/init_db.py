from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
import logging

from app.models.user import UserGroup
from app.models.enums import UserGroupEnum

logger = logging.getLogger(__name__)


def init_user_groups(db: Session):
    """Initialize user groups if they don't exist"""
    try:
        groups = [UserGroupEnum.USER, UserGroupEnum.MODERATOR, UserGroupEnum.ADMIN]
        
        for group_name in groups:
            existing_group = db.query(UserGroup).filter(UserGroup.name == group_name).first()
            if not existing_group:
                new_group = UserGroup(name=group_name)
                db.add(new_group)
                logger.info(f"Created user group: {group_name}")
        
        db.commit()
        logger.info("User groups initialized successfully")
    except OperationalError as e:
        logger.warning(f"Database tables may not exist yet: {e}")
        db.rollback()
    except Exception as e:
        logger.error(f"Error initializing user groups: {e}")
        db.rollback()
        raise

