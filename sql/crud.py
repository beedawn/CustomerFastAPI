from sqlalchemy.orm import Session
from . import models, schemas


def get_customer(db: Session, customer_id: str):
    return (
        db.query(models.CustomerBasicInfo)
        .filter(models.CustomerBasicInfo.id == customer_id)
        .first()
    )


def ensure_other_contact_info_exists(
    db: Session, other_contact_info_ob: schemas.OtherContactInfoCreate
):
    other_contact_info = (
        db.query(models.OtherContactInfo).filter_by(id=other_contact_info_ob.id).first()
    )
    if other_contact_info is None:
        other_contact_info = models.OtherContactInfo(
            id=other_contact_info_ob.id,
            preferredContactMethod=other_contact_info_ob.preferredContactMethod,
            email=other_contact_info_ob.email,
            preferredLanguage=other_contact_info_ob.preferredLanguage,
            phone=models.Phone(
                id=other_contact_info_ob.phone.id,
                areaCode=other_contact_info_ob.phone.areaCode,
                preFix=other_contact_info_ob.phone.preFix,
                lineNumber=other_contact_info_ob.phone.lineNumber,
                phoneType=other_contact_info_ob.phone.phoneType,
            ),
            alternatePhone=models.Phone(
                id=other_contact_info_ob.alternatePhone.id,
                areaCode=other_contact_info_ob.alternatePhone.areaCode,
                preFix=other_contact_info_ob.alternatePhone.preFix,
                lineNumber=other_contact_info_ob.alternatePhone.lineNumber,
                phoneType=other_contact_info_ob.alternatePhone.phoneType,
            ),
        )
        db.add(other_contact_info)
        db.commit()
        db.refresh(other_contact_info)
    return other_contact_info


def create_customer(db: Session, customer: schemas.CustomerBasicInfoCreate):
    ensure_other_contact_info_exists(db, customer.otherContactInfo)
    db_customer = models.CustomerBasicInfo(
        id=customer.id,
        firstName=customer.firstName,
        middleName=customer.middleName,
        lastName=customer.lastName,
        dateOfBirth=customer.dateOfBirth,
        gender=customer.gender,
        county=customer.county,
        fixedAddress=customer.fixedAddress,
        assistanceWithInsurance=customer.assistanceWithInsurance,
        familyPlanningBenefits=customer.familyPlanningBenefits,
        otherContactInfo_id=customer.otherContactInfo.id,
    )
    if customer.otherContactInfo:
        db_other_contact_info = models.OtherContactInfo(
            id=customer.otherContactInfo.id,
            preferredContactMethod=customer.otherContactInfo.preferredContactMethod,
            email=customer.otherContactInfo.email,
            preferredLanguage=customer.otherContactInfo.preferredLanguage,
        )
        if customer.otherContactInfo.phone:
            db_phone = models.Phone(
                id=customer.otherContactInfo.phone.id,
                areaCode=customer.otherContactInfo.phone.areaCode,
                preFix=customer.otherContactInfo.phone.preFix,
                lineNumber=customer.otherContactInfo.phone.lineNumber,
                phoneType=customer.otherContactInfo.phone.phoneType,
            )
            db_other_contact_info.phone_id = db_phone.id
        if customer.otherContactInfo.alternatePhone:
            db_alternate_phone = models.Phone(
                id=customer.otherContactInfo.alternatePhone.id,
                areaCode=customer.otherContactInfo.alternatePhone.areaCode,
                preFix=customer.otherContactInfo.alternatePhone.preFix,
                lineNumber=customer.otherContactInfo.alternatePhone.lineNumber,
                phoneType=customer.otherContactInfo.alternatePhone.phoneType,
            )
            db_other_contact_info.alternatePhone_id = db_alternate_phone.id
        db_customer.otherContactInfo_id = db_other_contact_info.id
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer
