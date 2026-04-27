"""Shared utilities for the report functionality."""

import json
import os
from typing import Literal

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from pydantic import BaseModel, ConfigDict, Field, RootModel, ValidationError

# DataSpace chart-generation endpoint, used to render charts as images in the
# PDF. Read from the environment at import time so the host Django project
# doesn't need a reports-specific setting.
CHART_API_BASE_URL = os.getenv("CHART_API_BASE_URL")


class _Strict(BaseModel):
    """Forbid unknown keys so typos are caught."""

    model_config = ConfigDict(extra="forbid")


class ReportColumn(_Strict):
    label: str
    slug: str
    cumulative: bool


class ReportTable(_Strict):
    columns: list[ReportColumn]


class ReportChart(_Strict):
    title: str
    description: str
    chart_type: str
    x_axis_column: str
    x_axis_label: str
    y_axis_label: str
    show_legend: Literal["true", "false"]
    filter: str


class ReportSection1(_Strict):
    """Flood Risk Overview."""

    TABLE_2: ReportTable


class ReportSection2(_Strict):
    """Losses and Damages, rendered only when CHARTS is non-empty."""

    title: str
    sub_title: str
    CHARTS: list[ReportChart] = Field(default_factory=list)


class ReportSection3(_Strict):
    """Government Response, rendered only when CHARTS is non-empty."""

    title: str
    sub_title: str
    description: str
    CHARTS: list[ReportChart] = Field(default_factory=list)


class StateReport(_Strict):
    TRANSFORMED_RESOURCE_ID: str = ""
    SECTION_1: ReportSection1
    SECTION_2: ReportSection2
    SECTION_3: ReportSection3


class ReportConfig(RootModel[dict[str, StateReport]]):
    """Top-level report_config.json shape: {state_code: StateReport}."""


def load_reports():
    """Return the report configuration, keyed by state code."""
    path = settings.BASE_DIR / "report_config.json"
    if not path.is_file():
        return {}
    data = json.loads(path.read_text())
    try:
        ReportConfig.model_validate(data)
    except ValidationError as exc:
        raise ImproperlyConfigured(f"Invalid {path}:\n{exc}") from exc
    return data
