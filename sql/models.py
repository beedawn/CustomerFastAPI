from sqlalchemy import Boolean, Column, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from .schemas import PhoneType_Type, PreferredContactMethod_Type, Gender_Type
from .database import Base


class Phone(Base):
    __tablename__ = "phone"
    id = Column(String, primary_key=True, index=True)
    areaCode = Column(String, nullable=False)
    preFix = Column(String, nullable=False)
    lineNumber = Column(String, nullable=False)
    phoneType = Column(Enum(PhoneType_Type))


class OtherContactInfo(Base):
    __tablename__ = "other_contact_info"
    id = Column(String, primary_key=True, index=True)
    preferredContactMethod = Column(Enum(PreferredContactMethod_Type))
    phone_id = Column(String, ForeignKey("phone.id"))
    alternatePhone_id = Column(String, ForeignKey("phone.id"))
    email = Column(String)
    preferredLanguage = Column(String)
    phone = relationship("Phone", foreign_keys=[phone_id])
    alternatePhone = relationship("Phone", foreign_keys=[alternatePhone_id])


class CustomerBasicInfo(Base):
    __tablename__ = "customers_basic_info"
    id = Column(String, primary_key=True, index=True)
    firstName = Column(String, nullable=False)
    middleName = Column(String)
    lastName = Column(String, nullable=False)
    dateOfBirth = Column(String, nullable=False)
    gender = Column(Enum(Gender_Type, nullable=False))
    county = Column(String, nullable=False)
    fixedAddress = Column(Boolean, nullable=False)
    assistanceWithInsurance = Column(Boolean, nullable=False)
    familyPlanningBenefits = Column(Boolean, nullable=False)
    otherContactInfo_id = Column(
        String, ForeignKey("other_contact_info.id"), nullable=True
    )
    otherContactInfo = relationship("OtherContactInfo")
