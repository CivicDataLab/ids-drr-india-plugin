# IDS-DRR: India backend

Flood-risk PDF report generator (`GET /report` endpoint) for the IDS-DRR India deployment, packaged as a pluggable Django app.

The report generator reads per-state metadata from `settings.BASE_DIR / "report_config.json"` at request time. Keys are STATE Geography codes. Values are validated by `plugin.config.ReportConfig`.

The `CHART_API_BASE_URL` environment variable must point to a DataSpace chart-generation endpoint in order to fetch chart images. It is read at import time by `plugin/config.py`.
