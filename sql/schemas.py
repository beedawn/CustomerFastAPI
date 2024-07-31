from enum import Enum
from pydantic import BaseModel
from typing import Optional
import uuid as uuid_pkg
from components.message_information import MessageInformation


class PhoneType_Type(str, Enum):
    Business = "Business"
    Fax = "Fax"
    Mobile = "Mobile"
    Other = "Other"
    Pager = "Pager"
    Personal = "Personal"


class PreferredContactMethod_Type(str, Enum):
    Email = "Email"
    Phone = "Phone"
    Post = "Post"


class Gender_Type(str, Enum):
    Female = "Female"
    Male = "Male"
    Unknown = "Unknown"


class PhoneBase(BaseModel):
    areaCode: Optional[str] = ""
    preFix: Optional[str] = ""
    lineNumber: Optional[str] = ""
    phoneType: Optional[PhoneType_Type] = (
        None  # enum Bussiness, Fax, Mobile, Other, Pager, Personal
    )


class PhoneCreate(PhoneBase):
    id: str = str(uuid_pkg.uuid4()) + "_info"


class AltPhoneCreate(PhoneBase):
    id: str = str(uuid_pkg.uuid4()) + "_alt"


class OtherContactInfoBase(BaseModel):
    preferredContactMethod: Optional[PreferredContactMethod_Type] = (
        PreferredContactMethod_Type.Email
    )
    phone: Optional[PhoneCreate] = PhoneCreate()
    alternatePhone: Optional[PhoneCreate] = AltPhoneCreate()
    email: Optional[str] = ""
    preferredLanguage: Optional[str] = ""


class OtherContactInfoCreate(OtherContactInfoBase):
    id: str = str(uuid_pkg.uuid4())


class CustomerBasicInfoBase(BaseModel):
    messageInformation: Optional[MessageInformation] = None
    id: str  # uuid #required
    firstName: str  # required
    middleName: Optional[str] = ""
    lastName: str  # required
    dateOfBirth: str  # required
    gender: Gender_Type  # required
    county: str  # required
    fixedAddress: bool  # required
    assistanceWithInsurance: bool  # required
    familyPlanningBenefits: bool  # required
    otherContactInfo: Optional[OtherContactInfoCreate] = OtherContactInfoCreate()


class CustomerBasicInfoCreate(CustomerBasicInfoBase):
    pass


class CustomerBasicInfo(CustomerBasicInfoBase):
    class Config:
        from_attributes = True
