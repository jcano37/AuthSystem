from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.company import Company as CompanySchema
from app.schemas.company import CompanyCreate, CompanyUpdate

router = APIRouter()


@router.get("/", response_model=List[CompanySchema])
def get_companies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve companies based on user permissions.
    - Root/Superusers see all companies
    - Regular users see only their own company
    """
    companies = crud.company.get_companies(
        db, skip=skip, limit=limit, current_user=current_user
    )
    return companies


@router.post("/", response_model=CompanySchema)
def create_company(
    *,
    db: Session = Depends(deps.get_db),
    company_in: CompanyCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new company.
    Only root/superusers can create companies.
    """
    try:
        company = crud.company.create_company(db, company_in=company_in)
        return company
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{company_id}", response_model=CompanySchema)
def get_company(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get company by ID.
    - Root/Superusers can access any company
    - Regular users can only access their own company
    """
    company = crud.company.get_company_by_id(db, company_id=company_id)

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    # Check access permissions
    if not current_user.is_superuser and current_user.company_id != company.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this company",
        )

    return company


@router.put("/{company_id}", response_model=CompanySchema)
def update_company(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    company_in: CompanyUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a company.
    Only root/superusers can update companies.
    """
    company = crud.company.get_company_by_id(db, company_id=company_id)

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    try:
        company = crud.company.update_company(db, db_obj=company, obj_in=company_in)
        return company
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{company_id}", response_model=CompanySchema)
def delete_company(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a company.
    Only root/superusers can delete companies.
    Root company cannot be deleted.
    """
    company = crud.company.get_company_by_id(db, company_id=company_id)

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    if company.is_root:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Root company cannot be deleted",
        )

    company = crud.company.delete_company(db, company_id=company_id)
    return company
