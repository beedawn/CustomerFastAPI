from fastapi.testclient import TestClient
from sqlalchemy import create_engine, null
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from sql.database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_customer_info_valid():
    user_id = "c8d736e1-014c-4e65-8b9d-76327db8eh8b88c676j490098x9f"
    first_name = "Alice"
    middle_name = "Grace"
    last_name = "Smith"
    date_of_birth = "1985-07-20"
    gender = "Female"
    county = "Jefferson"
    fixed_address = True
    assistance_with_insurance = True
    family_planning_benefits = False
    email = "agrace@yahoo.com"
    preferred_language = "python"

    response = client.post(
        "/CustomerInfo",
        json={
            "id": user_id,
            "firstName": first_name,
            "middleName": middle_name,
            "lastName": last_name,
            "dateOfBirth": date_of_birth,
            "gender": gender,
            "county": county,
            "fixedAddress": fixed_address,
            "assistanceWithInsurance": assistance_with_insurance,
            "familyPlanningBenefits": family_planning_benefits,
            "otherContactInfo": {
                "email": email,
                "preferredLanguage": preferred_language,
            },
        },
    )

    assert response.json() == 201
    response = client.get(f"/CustomerInfo?searchString={user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["firstName"] == first_name
    assert data["middleName"] == middle_name
    assert data["lastName"] == last_name
    assert data["dateOfBirth"] == date_of_birth
    assert data["gender"] == gender
    assert data["county"] == county
    assert data["fixedAddress"] == fixed_address
    assert data["assistanceWithInsurance"] == assistance_with_insurance
    assert data["familyPlanningBenefits"] == family_planning_benefits
    assert data["otherContactInfo"]["email"] == email
    assert data["otherContactInfo"]["preferredLanguage"] == preferred_language


def test_customer_info_invalid_first_name():
    user_id = "c8d736e1-014c-4e65-8b9d-76327db8eh8b88c676j490098x9f"
    first_name = ""
    middle_name = "Grace"
    last_name = "Smith"
    date_of_birth = "1985-07-20"
    gender = "Female"
    county = "Jefferson"
    fixed_address = True
    assistance_with_insurance = True
    family_planning_benefits = False
    email = "agrace@yahoo.com"
    preferred_language = "python"

    response = client.post(
        "/CustomerInfo",
        json={
            "id": user_id,
            "firstName": first_name,
            "middleName": middle_name,
            "lastName": last_name,
            "dateOfBirth": date_of_birth,
            "gender": gender,
            "county": county,
            "fixedAddress": fixed_address,
            "assistanceWithInsurance": assistance_with_insurance,
            "familyPlanningBenefits": family_planning_benefits,
            "otherContactInfo": {
                "email": email,
                "preferredLanguage": preferred_language,
            },
        },
    )

    assert response.json() == {"detail": "The first name must not be empty"}
    assert response.status_code == 400


def test_customer_info_invalid_last_name():
    user_id = "c8d736e1-014c-4e65-8b9d-76327db8eh8b88c676j490098x9f"
    first_name = "Alice"
    middle_name = "Grace"
    last_name = ""
    date_of_birth = "1985-07-20"
    gender = "Female"
    county = "Jefferson"
    fixed_address = True
    assistance_with_insurance = True
    family_planning_benefits = False
    email = "agrace@yahoo.com"
    preferred_language = "python"

    response = client.post(
        "/CustomerInfo",
        json={
            "id": user_id,
            "firstName": first_name,
            "middleName": middle_name,
            "lastName": last_name,
            "dateOfBirth": date_of_birth,
            "gender": gender,
            "county": county,
            "fixedAddress": fixed_address,
            "assistanceWithInsurance": assistance_with_insurance,
            "familyPlanningBenefits": family_planning_benefits,
            "otherContactInfo": {
                "email": email,
                "preferredLanguage": preferred_language,
            },
        },
    )

    assert response.json() == {"detail": "The last name must not be empty"}
    assert response.status_code == 400


def test_customer_info_invalid_email():
    user_id = "c8d736e1-014c-4e65-8b9d-76327db8eh8b88c676j490098x9f"
    first_name = "Alice"
    middle_name = "Grace"
    last_name = "Smith"
    date_of_birth = "1985-07-20"
    gender = "Female"
    county = "Jefferson"
    fixed_address = True
    assistance_with_insurance = True
    family_planning_benefits = False
    email = "agrace"
    preferred_language = "python"

    response = client.post(
        "/CustomerInfo",
        json={
            "id": user_id,
            "firstName": first_name,
            "middleName": middle_name,
            "lastName": last_name,
            "dateOfBirth": date_of_birth,
            "gender": gender,
            "county": county,
            "fixedAddress": fixed_address,
            "assistanceWithInsurance": assistance_with_insurance,
            "familyPlanningBenefits": family_planning_benefits,
            "otherContactInfo": {
                "email": email,
                "preferredLanguage": preferred_language,
            },
        },
    )
    assert response.json() == {"detail": "The email given must be valid"}
    assert response.status_code == 400


def test_customer_info_invalid_object():
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
    response = client.post(
        "/CustomerInfo",
        json={},
    )

    expected_response = {
        "detail": "invalid input, object invalid. received {} expected "
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
        '"id": "724cbe5b-ee65-4bd0-852f-8578da6ca677"}}'
    }

    print("response")
    print(response.json())
    print("expected")
    print(expected_response)
    assert response.json() == expected_response
    assert response.status_code == 400


def test_customer_info_duplicate():
    user_id = "c8d736e1-014c-4e65-8b9d-76327db8eh8b88c676j490098x9f"
    first_name = "Alice"
    middle_name = "Grace"
    last_name = "Smith"
    date_of_birth = "1985-07-20"
    gender = "Female"
    county = "Jefferson"
    fixed_address = True
    assistance_with_insurance = True
    family_planning_benefits = False
    email = "agrace@yahoo.com"
    preferred_language = "python"

    response_1 = client.post(
        "/CustomerInfo",
        json={
            "id": user_id,
            "firstName": first_name,
            "middleName": middle_name,
            "lastName": last_name,
            "dateOfBirth": date_of_birth,
            "gender": gender,
            "county": county,
            "fixedAddress": fixed_address,
            "assistanceWithInsurance": assistance_with_insurance,
            "familyPlanningBenefits": family_planning_benefits,
            "otherContactInfo": {
                "email": email,
                "preferredLanguage": preferred_language,
            },
        },
    )

    response_2 = client.post(
        "/CustomerInfo",
        json={
            "id": user_id,
            "firstName": first_name,
            "middleName": middle_name,
            "lastName": last_name,
            "dateOfBirth": date_of_birth,
            "gender": gender,
            "county": county,
            "fixedAddress": fixed_address,
            "assistanceWithInsurance": assistance_with_insurance,
            "familyPlanningBenefits": family_planning_benefits,
            "otherContactInfo": {
                "email": email,
                "preferredLanguage": preferred_language,
            },
        },
    )

    assert response_2.status_code == 409
    assert response_2.json() == {
        "detail": "an existing Customer with this id already exists"
    }


def test_customer_info_get_bad_id():
    response = client.get(f"/CustomerInfo?searchString=6896665658658")
    assert response.status_code == 400
    assert response.json() == {"detail": "Could not find the customer"}


def test_doc_ui_endpoint():
    response = client.get(f"/ui")
    assert response.status_code == 200
