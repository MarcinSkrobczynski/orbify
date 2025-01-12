from copy import deepcopy

import pytest
from fastapi import status
from pytest_parametrize import parametrize

PAYLOAD = {
    "name": "Simple project",
    "description": "Simple description",
    "start_date": "2025-01-01",
    "end_date": "2025-01-31",
    "area_of_interest": {
        "type": "Feature",
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [-52.8430645648562, -5.63351005831322],
                        [-52.8289481608136, -5.674529420529012],
                        [-52.8114438198008, -5.6661010219506664],
                        [-52.8430645648562, -5.63351005831322],
                    ]
                ]
            ],
        },
    },
}


@parametrize(
    {
        "no_description": {"values": [("description", None)]},
        "empty_description": {"values": [("description", "")]},
        "simple_description": {"values": [("description", "Simple description")]},
    }
)
def test_create_project_returns_201_when_ok(endpoint_uri, client, values):
    payload = deepcopy(PAYLOAD)
    for key, value in values:
        payload[key] = value

    response = client.post(endpoint_uri("projects"), json=payload)
    assert response.status_code == status.HTTP_201_CREATED, response.text

    data = response.json()
    assert data["id"]
    data.pop("id")
    assert data == payload


CREATE_AND_UPDATE_TESTS = {
    "no_name": {"values": [("name", None)]},
    "empty_name": {"values": [("name", "")]},
    "too_long_name": {"values": [("name", "a" * 33)]},
    "no_start_date": {"values": [("start_date", None)]},
    "invalid_start_date": {"values": [("start_date", "2025-01-32")]},
    "no_end_date": {"values": [("end_date", None)]},
    "invalid_end_date": {"values": [("end_date", "2025-01-32")]},
    "start_date_greater_than_end_date": {"values": [("start_date", "2025-01-02"), ("end_date", "2025-01-01")]},
    "no_area_of_interest": {"values": [("area_of_interest", None)]},
    "no_area_of_interest_type": {
        "values": [
            (
                "area_of_interest",
                {
                    "type": None,
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [
                                [
                                    [-52.8430645648562, -5.63351005831322],
                                    [-52.8289481608136, -5.674529420529012],
                                    [-52.8114438198008, -5.6661010219506664],
                                    [-52.8430645648562, -5.63351005831322],
                                ]
                            ]
                        ],
                    },
                },
            )
        ]
    },
    "no_area_of_interest_geometry": {
        "values": [
            (
                "area_of_interest",
                {
                    "type": "Feature",
                    "geometry": None,
                },
            )
        ]
    },
    "bad_area_of_interest_geometry_type": {
        "values": [
            (
                "area_of_interest",
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "WrongType",
                        "coordinates": [
                            [
                                [
                                    [-52.8430645648562, -5.63351005831322],
                                    [-52.8289481608136, -5.674529420529012],
                                    [-52.8114438198008, -5.6661010219506664],
                                    [-52.8430645648562, -5.63351005831322],
                                ]
                            ]
                        ],
                    },
                },
            ),
        ]
    },
    "bad_area_of_interest_geometry_coordinates": {
        "values": [
            (
                "area_of_interest",
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [
                                [
                                    [-52.8430645648562, -5.63351005831322],
                                    [-52.8289481608136, -5.674529420529012],
                                    [-52.8430645648562, -5.63351005831322],
                                ]
                            ]
                        ],
                    },
                },
            )
        ]
    },
}


@parametrize(CREATE_AND_UPDATE_TESTS)
def test_create_project_returns_422_when_wrong_payload(endpoint_uri, client, values):
    payload = deepcopy(PAYLOAD)
    for key, value in values:
        payload[key] = value

    response = client.post(endpoint_uri("projects"), json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


@pytest.fixture
def project_id(endpoint_uri, client):
    response = client.post(endpoint_uri("projects"), json=PAYLOAD)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    yield data["id"]
    client.delete(endpoint_uri(f"projects/{data['id']}"))


def test_get_project_returns_200_when_ok(endpoint_uri, client, project_id):
    response = client.get(endpoint_uri(f"projects/{project_id}"))
    assert response.status_code == status.HTTP_200_OK, response.text


def test_get_project_returns_404_when_not_found(endpoint_uri, client):
    response = client.get(endpoint_uri("projects/99999999"))
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_get_project_returns_422_when_not_int_id(endpoint_uri, client):
    response = client.get(endpoint_uri("projects/wrong-id"))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


def test_get_projects_returns_200_when_ok(endpoint_uri, client):
    response = client.get(endpoint_uri("projects"))
    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_get_projects_returns_200_and_empty_list_when_skip_too_many(endpoint_uri, client):
    response = client.get(endpoint_uri("projects?skip=1000000"))
    assert response.status_code == status.HTTP_200_OK, response.text
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


UPDATE_TESTS = {
    "new_name": {"values": [("name", "New name")]},
    "new_description": {"values": [("description", "New description")]},
    "new_start_date": {"values": [("start_date", "2025-01-02")]},
    "new_end_date": {"values": [("end_date", "2025-01-30")]},
    "new_area_of_interest": {
        "values": [
            (
                "area_of_interest",
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "MultiPolygon",
                        "coordinates": [
                            [
                                [
                                    [-52.8430645648562, -5.63351005831322],
                                    [-52.8289481608136, -5.674529420529012],
                                    [-52.8114438198008, -5.6661010219506664],
                                    [-52.8289481608136, -5.674529420529012],
                                    [-52.8114438198008, -5.6661010219506664],
                                    [-52.8289481608136, -5.674529420529012],
                                    [-52.8114438198008, -5.6661010219506664],
                                    [-52.8289481608136, -5.674529420529012],
                                    [-52.8114438198008, -5.6661010219506664],
                                    [-52.8430645648562, -5.63351005831322],
                                ]
                            ]
                        ],
                    },
                },
            )
        ]
    },
}


@parametrize(UPDATE_TESTS)
def test_update_project_returns_200_when_ok(endpoint_uri, client, project_id, values):
    payload = deepcopy(PAYLOAD)
    for key, value in values:
        payload[key] = value

    response = client.put(endpoint_uri(f"projects/{project_id}"), json=payload)
    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    payload["id"] = project_id
    assert data == payload


@parametrize(CREATE_AND_UPDATE_TESTS)
def test_update_project_returns_422_when_wrong_payload(endpoint_uri, client, project_id, values):
    payload = deepcopy(PAYLOAD)
    for key, value in values:
        payload[key] = value

    response = client.put(endpoint_uri(f"projects/{project_id}"), json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


@parametrize(UPDATE_TESTS)
def test_partial_update_project_returns_200_when_ok(endpoint_uri, client, project_id, values):
    payload = dict(values)

    response = client.patch(endpoint_uri(f"projects/{project_id}"), json=payload)
    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    for key, value in values:
        assert data[key] == value


def test_delete_project_returns_204_when_ok(endpoint_uri, client, project_id):
    response = client.delete(endpoint_uri(f"projects/{project_id}"))
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    response = client.get(endpoint_uri(f"projects/{project_id}"))
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
