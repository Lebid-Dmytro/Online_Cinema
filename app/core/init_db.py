from sqlalchemy.orm import Session

from app.models.user import UserGroup
from app.models.enums import UserGroupEnum


def init_user_groups(db: Session):
    """Initialize user groups if they don't exist"""
    groups = [UserGroupEnum.USER, UserGroupEnum.MODERATOR, UserGroupEnum.ADMIN]
    
    for group_name in groups:
        existing_group = db.query(UserGroup).filter(UserGroup.name == group_name).first()
        if not existing_group:
            new_group = UserGroup(name=group_name)
            db.add(new_group)
    
    db.commit()

