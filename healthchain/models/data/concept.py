from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Union
import logging
import math

class Standard(Enum):
    cda = "cda"
    fhir = "fhir"


class DataType(BaseModel):
    """
    Base class for all data types
    """

    _source: Optional[Dict] = None


class Quantity(BaseModel):
    content: Optional[Union[str, float]] = None
    scale: Optional[str] = None

    @validator('content', pre=True, always=True)
    def ensure_float_conversion(cls, v):
        if v is None:
            return v
        if isinstance(v, float):
            if math.isinf(v):
                logging.error(f"OverflowError: The value '{v}' is too large.")
                raise OverflowError(f"The value '{v}' is too large.")
            return v
        if isinstance(v, str):
            try:
                value = float(v)
                if math.isinf(value):
                    logging.error(f"OverflowError: The value '{v}' is too large.")
                    raise OverflowError(f"The value '{v}' is too large.")
                return value
            except ValueError:
                logging.error(f"ValueError: Unable to convert '{v}' to float.")
                raise ValueError(f"Unable to convert '{v}' to float.")
        raise TypeError(f"Unsupported type {type(v).__name__}; expected 'str' or 'float'.")




class Range(DataType):
    low: Optional[Quantity] = None
    high: Optional[Quantity] = None


class TimeInterval(DataType):
    period: Optional[Quantity] = None
    phase: Optional[Range] = None
    institution_specified: Optional[bool] = None


class Concept(BaseModel):
    """
    A more lenient, system agnostic representation of a concept e.g. problems, medications, allergies
    that can be converted to CDA or FHIR
    """

    _standard: Optional[Standard] = None
    code: Optional[str] = None
    code_system: Optional[str] = None
    code_system_name: Optional[str] = None
    display_name: Optional[str] = None


class ProblemConcept(Concept):
    """
    Contains problem/condition specific fields
    """

    onset_date: Optional[str] = None
    abatement_date: Optional[str] = None
    status: Optional[str] = None
    recorded_date: Optional[str] = None


class MedicationConcept(Concept):
    """
    Contains medication specific fields
    """

    dosage: Optional[Quantity] = None
    route: Optional[Concept] = None
    frequency: Optional[TimeInterval] = None
    duration: Optional[Range] = None
    precondition: Optional[Dict] = None


class AllergyConcept(Concept):
    """
    Contains allergy specific fields

    Defaults allergy type to propensity to adverse reactions in SNOMED CT
    """

    allergy_type: Optional[Concept] = Field(
        default=Concept(
            code="420134006",
            code_system="2.16.840.1.113883.6.96",
            code_system_name="SNOMED CT",
            display_name="Propensity to adverse reactions",
        )
    )
    severity: Optional[Concept] = None
    reaction: Optional[Concept] = None
