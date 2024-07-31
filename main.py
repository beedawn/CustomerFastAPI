import json
from fastapi import FastAPI, status, HTTPException, Query, Body, Depends
from pydantic import ValidationError
from sql.schemas import (
    CustomerBasicInfoCreate,
    CustomerBasicInfo,
)
from fastapi.openapi.utils import get_openapi
from typing import Optional, Any
from sql import crud, models
from sql.database import SessionLocal, engine
from sqlalchemy.orm import Session
import re
from sqlalchemy import null


models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/ui", openapi_url="/openapi.yaml")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


example_customer_basic_info_create = {
    "messageInformation": null,
    "id": "dbe071f3-d2fa-4b0e-9940-c2241b1fc39d",
    "firstName": "John",
    "middleName": "Smith",
    "lastName": "Doe",
    "dateOfBirth": "1980-01-01",
    "gender": "Male",
    "county": "Some County",
    "fixedAddress": True,
    "assistanceWithInsurance": True,
    "familyPlanningBenefits": False,
    "otherContactInfo": {
        "preferredContactMethod": "Email",
        "phone": {
            "areaCode": "123",
            "preFix": "456",
            "lineNumber": "7890",
            "phoneType": "Mobile",
            "id": "b5b3a8e1-7f3c-412b-afd2-7ca3cff7b775_info",
        },
        "alternatePhone": {
            "areaCode": "987",
            "preFix": "654",
            "lineNumber": "3210",
            "phoneType": "Personal",
            "id": "77a84148-d8ac-4b98-b592-6329b6ae1fee_info",
        },
        "email": "john.doe@example.com",
        "preferredLanguage": "English",
        "id": "ee3cdef3-812e-4a02-a671-15d583f32028",
    },
}


def is_valid_email(email: str) -> bool:
    # Regular expression for a basic email validation
    email_regex = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email) is not None


@app.get(
    "/CustomerInfo",
    tags=["paths"],
    summary="gets a customers basic information",
    description="By passing in the Customers unique identifier you will get that users basic information",
    operation_id="searchCustomers",
    response_model=CustomerBasicInfo,
    responses={
        200: {
            "description": "search results matching criteria",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "type": "object",
                        "properties": {
                            "messageInformation": {
                                "type": "object",
                                "properties": {
                                    "source": {
                                        "type": "string",
                                        "example": "SwaggerExamplePage",
                                    }
                                },
                                "required": ["source"],
                            },
                            "id": {
                                "type": "string",
                                "format": "uuid",
                                "example": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                            },
                            "firstName": {"type": "string", "example": "Bob"},
                            "middleName": {
                                "type": "string",
                                "nullable": True,
                                "example": "Robert",
                            },
                            "lastName": {"type": "string", "example": "BobsLastName"},
                            "dateOfBirth": {
                                "type": "string",
                                "format": "date",
                                "example": "2016-08-29",
                            },
                            "gender": {
                                "type": "string",
                                "example": "Male",
                                "enum": ["Female", "Male", "Unknown"],
                            },
                            "county": {"type": "string", "example": "Anderson"},
                            "fixedAddress": {"type": "boolean", "example": False},
                            "assistanceWithInsurance": {
                                "type": "boolean",
                                "example": False,
                            },
                            "familyPlanningBenefits": {
                                "type": "boolean",
                                "example": False,
                            },
                            "OtherContactInfo": {
                                "type": "object",
                                "properties": {
                                    "preferredContactMethod": {
                                        "type": "string",
                                        "nullable": True,
                                        "example": "email",
                                        "enum": ["email", "phone", "post"],
                                    },
                                    "phone": {
                                        "type": "object",
                                        "properties": {
                                            "areaCode": {
                                                "type": "string",
                                                "example": "408",
                                            },
                                            "preFix": {
                                                "type": "string",
                                                "example": "867",
                                            },
                                            "lineNumber": {
                                                "type": "string",
                                                "example": "5309",
                                            },
                                            "phoneType": {
                                                "type": "string",
                                                "example": "Mobile",
                                                "enum": [
                                                    "Business",
                                                    "Fax",
                                                    "Mobile",
                                                    "Other",
                                                    "Pager",
                                                    "Personal",
                                                ],
                                            },
                                        },
                                    },
                                    "alternatePhone": {
                                        "type": "object",
                                        "properties": {
                                            "areaCode": {
                                                "type": "string",
                                                "example": "408",
                                            },
                                            "preFix": {
                                                "type": "string",
                                                "example": "867",
                                            },
                                            "lineNumber": {
                                                "type": "string",
                                                "example": "5309",
                                            },
                                            "phoneType": {
                                                "type": "string",
                                                "example": "Mobile",
                                                "enum": [
                                                    "Business",
                                                    "Fax",
                                                    "Mobile",
                                                    "Other",
                                                    "Pager",
                                                    "Personal",
                                                ],
                                            },
                                        },
                                        "nullable": True,
                                    },
                                    "email": {
                                        "type": "string",
                                        "nullable": True,
                                        "example": "jedwards@nope.com",
                                    },
                                    "preferredLanguage": {
                                        "type": "string",
                                        "nullable": True,
                                        "example": "American Sign",
                                    },
                                },
                            },
                        },
                        "required": [
                            "messageInformation",
                            "id",
                            "firstName",
                            "lastName",
                            "dateOfBirth",
                            "gender",
                            "county",
                            "fixedAddress",
                            "assistanceWithInsurance",
                            "familyPlanningBenefits",
                            "OtherContactInfo",
                        ],
                    }
                }
            },
        },
        400: {
            "description": "Bad Request",
            "content": {"application/json": {"example": {"detail": "Item not found"}}},
        },
    },
)
async def searchCustomers(
    searchString: Optional[str] = Query(
        None, description="pass an optional search string for looking " "up inventory"
    ),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    # gets unique identifier from client and provides basic customer info for that id

    customer = crud.get_customer(db, customer_id=searchString)
    if customer is None or searchString is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find the customer",
        )

    response = {
        "messageInformation": {"source": "example"},
        "id": customer.id,
        "firstName": customer.firstName,
        "middleName": customer.middleName,
        "lastName": customer.lastName,
        "dateOfBirth": customer.dateOfBirth,
        "gender": customer.gender.value,
        "county": customer.county,
        "fixedAddress": customer.fixedAddress,
        "assistanceWithInsurance": customer.assistanceWithInsurance,
        "familyPlanningBenefits": customer.familyPlanningBenefits,
        "otherContactInfo": {
            "preferredContactMethod": (
                customer.otherContactInfo.preferredContactMethod.value
                if customer.otherContactInfo.preferredContactMethod
                else None
            ),
            "phone": (
                {
                    "areaCode": (
                        customer.otherContactInfo.phone.areaCode
                        if customer.otherContactInfo.phone
                        else ""
                    ),
                    "preFix": (
                        customer.otherContactInfo.phone.preFix
                        if customer.otherContactInfo.phone
                        else ""
                    ),
                    "lineNumber": (
                        customer.otherContactInfo.phone.lineNumber
                        if customer.otherContactInfo.phone
                        else ""
                    ),
                    "phoneType": (
                        customer.otherContactInfo.phone.phoneType
                        if customer.otherContactInfo.phone
                        else None
                    ),
                    "id": (
                        customer.otherContactInfo.phone.id
                        if customer.otherContactInfo.phone
                        else None
                    ),
                }
                if customer.otherContactInfo.phone
                else None
            ),
            "alternatePhone": (
                {
                    "areaCode": (
                        customer.otherContactInfo.alternatePhone.areaCode
                        if customer.otherContactInfo.alternatePhone
                        else ""
                    ),
                    "preFix": (
                        customer.otherContactInfo.alternatePhone.preFix
                        if customer.otherContactInfo.alternatePhone
                        else ""
                    ),
                    "lineNumber": (
                        customer.otherContactInfo.alternatePhone.lineNumber
                        if customer.otherContactInfo.alternatePhone
                        else ""
                    ),
                    "phoneType": (
                        customer.otherContactInfo.alternatePhone.phoneType
                        if customer.otherContactInfo.alternatePhone
                        else None
                    ),
                    "id": (
                        customer.otherContactInfo.alternatePhone.id
                        if customer.otherContactInfo.alternatePhone
                        else None
                    ),
                }
                if customer.otherContactInfo.alternatePhone
                else None
            ),
            "email": (
                customer.otherContactInfo.email
                if customer.otherContactInfo.email
                else ""
            ),
            "preferredLanguage": (
                customer.otherContactInfo.preferredLanguage
                if customer.otherContactInfo.preferredLanguage
                else ""
            ),
            "id": customer.otherContactInfo.id if customer.otherContactInfo else None,
        },
    }
    return response


@app.post(
    "/CustomerInfo",
    tags=["paths"],
    response_model=None,
    summary="Adds CustomerInfo",
    description="Adds CustomerInfo to the system",
    operation_id="addCustomerInfo",
    responses={
        201: {"description": "Item created"},
        400: {"description": "Invalid input, object invalid"},
        409: {"description": "An existing Customer with this id already exists"},
    },
)
# could parse item to CustomerBasicInfo in params, need to use Any and parse in body to provide error matching specs
async def addCustomerInfo(item: Any = Body(...), db: Session = Depends(get_db)):

    try:
        parsed_input = CustomerBasicInfoCreate(**item)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"invalid input, object invalid. received {item} expected "
            '{"messageInformation": null, "id": "70443ecb-fa5c-4a64-8ad8-906a0a2ea088", '
            '"firstName": "John", '
            '"middleName": "Smith", '
            '"lastName": "Doe", '
            '"dateOfBirth": "1980-01-01", '
            '"gender": "Male", '
            '"county": "Some County", '
            '"fixedAddress": true, '
            '"assistanceWithInsurance": true, '
            '"familyPlanningBenefits": false, '
            '"otherContactInfo": {'
            '"preferredContactMethod": "Email", '
            '"phone": {'
            '"areaCode": "123", '
            '"preFix": "456", '
            '"lineNumber": "7890", '
            '"phoneType": "Mobile", '
            '"id": "6928dd7a-3bb2-4aad-94e4-f4e7bb532b07_info"}, '
            '"alternatePhone": '
            '{"areaCode": "987", '
            '"preFix": "654", '
            '"lineNumber": "3210", '
            '"phoneType": "Personal", '
            '"id": "10359a5f-6a45-4d6b-bbb4-b4419ab99e47_info"'
            "}, "
            '"email": "john.doe@example.com", '
            '"preferredLanguage": "English", '
            '"id": "724cbe5b-ee65-4bd0-852f-8578da6ca677"}}',
        )
    if len(parsed_input.firstName) <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The first name must not be empty",
        )
    if len(parsed_input.lastName) <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The last name must not be empty",
        )
    if parsed_input.otherContactInfo and parsed_input.otherContactInfo.email:
        if not parsed_input.otherContactInfo.email.strip() or not is_valid_email(
            parsed_input.otherContactInfo.email
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The email given must be valid",
            )
    customer = crud.get_customer(db, customer_id=parsed_input.id)
    if customer:
        raise HTTPException(
            status_code=409, detail="an existing Customer with this id already exists"
        )
    crud.create_customer(db, parsed_input)
    return status.HTTP_201_CREATED


# override FastApi defaults in docs at /ui
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Simple CustomerInfo API",
        version="1.0.0",
        summary="",
        description="This is the customer api for initial",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    openapi_schema["info"]["contact"] = {
        "email": "test@nope.com",
    }
    app.openapi_schema = openapi_schema
    # Remove default fastapi 422 response from the docs schema
    for path_item in app.openapi_schema["paths"].values():
        for method in path_item.values():
            responses = method.get("responses", {})
            if "422" in responses:
                del responses["422"]
    # Remove default 200 from docs schema for /CustomerInfo
    for path, path_item in openapi_schema["paths"].items():
        if "/CustomerInfo" in path:
            for method, method_info in path_item.items():
                if method == "post":
                    responses = method_info.get("responses", {})
                    if "200" in responses:
                        del responses["200"]
    return app.openapi_schema


app.openapi = custom_openapi
