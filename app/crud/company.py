from typing import Any, Dict, List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyUpdate


def get_company_by_id(db: Session, company_id: int) -> Optional[Company]:
    return db.query(Company).filter(Company.id == company_id).first()


def get_company_by_name(db: Session, name: str) -> Optional[Company]:
    return db.query(Company).filter(Company.name == name).first()


def get_company_by_name_or_id(
    db: Session, name: str, company_id: int
) -> Optional[Company]:
    return (
        db.query(Company)
        .filter(or_(Company.name == name, Company.id == company_id))
        .first()
    )


def get_root_company(db: Session) -> Optional[Company]:
    return db.query(Company).filter(Company.is_root == True).first()


def get_companies(
    db: Session, skip: int = 0, limit: int = 100, current_user: Optional[User] = None
) -> List[Company]:
    """
    Get list of companies based on user access
    - Root user/super_admin: All companies
    - Others: Only their own company
    """
    query = db.query(Company)

    # Check if user has root access
    if current_user and not current_user.is_superuser:
        # Regular users can only see their own company
        query = query.filter(Company.id == current_user.company_id)

    return query.offset(skip).limit(limit).all()


def create_company(db: Session, *, company_in: CompanyCreate) -> Company:
    """Create a new company"""
    # Check if company already exists
    if get_company_by_name(db, name=company_in.name):
        raise ValueError(f"Company with name '{company_in.name}' already exists")

    db_obj = Company(**company_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_company(
    db: Session, *, db_obj: Company, obj_in: CompanyUpdate | Dict[str, Any]
) -> Company:
    """Update company details"""
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)

    # Check name uniqueness if name is being updated
    if "name" in update_data and update_data["name"] != db_obj.name:
        if get_company_by_name(db, name=update_data["name"]):
            raise ValueError(
                f"Company with name '{update_data['name']}' already exists"
            )

    # Don't allow changing root status
    if "is_root" in update_data:
        del update_data["is_root"]

    for field in update_data:
        setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_company(db: Session, *, company_id: int) -> Optional[Company]:
    """Delete a company if it's not the root company"""
    company = get_company_by_id(db, company_id=company_id)

    if company and not company.is_root:  # Never delete the root company
        db.delete(company)
        db.commit()

    return company
