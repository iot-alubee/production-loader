import pandas as pd
import json

SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1til2yhjlsMEbOBuJs7LdrlHOC7vGplk45BJXnKlJD_g/"
    "export?format=csv&gid=1169700979"
)


def get_google_sheet_data(request):
    device_id = request.args.get("device_id")
    if not device_id:
        return json.dumps({"error": "Missing device_id"}), 400

    device_id = str(device_id).strip()

    df = pd.read_csv(
        SHEET_URL,
        dtype={"DeviceID": str}
    )

    df["DeviceID"] = df["DeviceID"].str.strip()

    row = df[df["DeviceID"] == device_id]

    if row.empty:
        return json.dumps({"error": "DeviceID not found"}), 404

    # Actual data order:
    # DeviceID | Production_Plan | Part_No
    production_plan_raw = row.iloc[0, 3]
    part_no = str(row.iloc[0, 4]).strip()
    shift = str(row.iloc[0, 7]).strip()
    item_code = str(row.iloc[0, 5]).strip()
    fixture = str(row.iloc[0, 6]).strip()
    machine = str(row.iloc[0, 1]).strip()
    unit = str(row.iloc[0, 2]).strip()
    supervisor = str(row.iloc[0, 8]).strip()
    department = str(row.iloc[0, 9]).strip()
    cycle_time = str(row.iloc[0, 11]).strip()
    assignee = str(row.iloc[0, 10]).strip()

    try:
        production_plan = int(float(str(production_plan_raw).strip()))
    except Exception:
        production_plan = 0

    response = {
        "DeviceID": device_id,
        "Item_Code": item_code,
        "Part_No": part_no,
        "Production_Plan": production_plan,
        "Machine": machine,
        "Unit": unit,
        "Shift": shift,
        "Supervisor": supervisor,
        "Department": department,
        "Assignee": assignee,
        "Fixture": fixture,
        "Cycle_Time": cycle_time,
    }

    return (
        json.dumps(response),
        200,
        {"Content-Type": "application/json"}
    )
