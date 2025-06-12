# 🧪 JSON to Parquet Data Validation & Transformation Project

This project validates the structure and content of a JSON file against a defined JSON Schema, transforms it into a Parquet file using ETL rules, and verifies that the transformations were applied correctly through automated tests.

---

## 📁 Project Structure

```bash
├── data/
│ ├── datos.json # Input data in JSON format
│ ├── datos_schema.json # JSON Schema definition
│ └── resultado_transformado.parket # Output Parquet file after transformation
├── scripts/
│ ├── ETL_to_parquet.py # Script to transform JSON into Parquet
│ └── gen_schema.py # Script to generate a JSON Schema
├── tests/
│ ├── config.py # Project-wide configuration constants
│ ├── conftest.py # Fixture configuration for JSON session validation
│ ├── test_integridad.py # Validates JSON with Pytest data tests
│ ├── test_schema.py # Validates JSON structure against schema
│ └── test_transformacion_parquet.py # Validates ETL transformations
├── requeriments.txt 
└── README.md
```

---

## ⚙️ Requirements

- Python 3.10+
- pytest
- json
- jsonschema
- genson
- pandas
- pyarrow

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

1. Validate JSON against its schema
```bash
pytest tests/test_schema.py -v
```
2. Run the JSON → Parquet transformation
```bash
python scripts/transformar_datos.py -v
```
This will generate the resultado_transformado.parquet file.

3. Run tests to validate the transformed Parquet data
```bash
pytest tests/test_transformacion_parquet.py -v
```

4. Run all tests wit a html-report
```bash
pytest -v --html=reports/html_test_report.html --self-contained-html 
```

---

## 🧠 ETL Transformation Rules
The transformation script applies the following business rules:

- user_id: Copied from id
- birth_year: Calculated as 2025 - edad
- height_cm: Height converted from meters to centimeters
- roles_csv: List of roles joined by commas
- address_full: Full address created by joining street, city, postal code, and country
- mobile_phone / landline_phone: Phone numbers split by type
- interests: Preferences joined with |
- project_summary: Each project name combined with its progress in parentheses
- comment_status: If the original comentarios is null, replaced with "no_comments"
- extra_mixed_data: Mixed array converted to a flat string representation