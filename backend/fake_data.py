from schemas import (
    DBUser,
    DBProject,
    DBPanel,
    DBCell,
    DBUserProject,
    DBEnergyDataPoint,
    DBEnergyPrice,
    DBPowerDataPoint,
)
from insert import insert


users = [
    DBUser(
        id="1",
        username="dev",
        password="supersecret!password",
        account_balance=1000.0,
        cells_owned=0,
        projects_owned=0,
        total_invested=0.0,
        total_earnings=0.0,
        total_energy_generated=0.0,
        maximum_power_generation=0.0,
    ),
]


projects = [
    DBProject(
        project_id="CSP_FR_001",
        name="Cestas Solar Park",
        location_city="Cestas",
        location_country="France",
        latitude=44.772,
        longitude=-0.715,
        bidding_zone="FR",
        installed_capacity="300 MW",
        description=(
            "Located near Bordeaux in the Nouvelle-Aquitaine region, Cestas Solar Park is one of Europe’s largest "
            "photovoltaic installations. Commissioned in 2015 with a capacity of approximately 300 MW and covering "
            "over 260 hectares, the facility employs advanced PV modules to convert abundant sunlight into electricity. "
            "It significantly contributes to France’s renewable energy targets and supplies clean power to tens of thousands "
            "of households."
        ),
        number_of_cells=1000000,  # Estimated based on typical panel capacity
        unit_price=2.50,  # Assumed unit price per cell in EUR
        completed_date="2015-01-01",
        is_completed=True,
    ),
    DBProject(
        project_id="MSP_ES_001",
        name="Mula Solar Power Plant",
        location_city="Mula",
        location_country="Spain",
        latitude=38.046,
        longitude=-1.493,
        bidding_zone="ES",
        installed_capacity="60 MW",
        description=(
            "Situated in the sunny Murcia region, the Mula Solar Power Plant harnesses the area’s high solar irradiance to "
            "generate renewable energy. With an installed capacity of around 60 MW, this project uses state-of-the-art "
            "photovoltaic technology over a sprawling open area. Commissioned in the mid-2010s, it plays an important role "
            "in Spain’s drive toward sustainable energy production and reducing carbon emissions."
        ),
        number_of_cells=200000,
        unit_price=2.30,
        completed_date="2016-01-01",
        is_completed=True,
    ),
    DBProject(
        project_id="SLG_DE_001",
        name="Solarpark Lieberose",
        location_city="Lieberose",
        location_country="Germany",
        latitude=51.983,
        longitude=14.308,
        bidding_zone="DE",
        installed_capacity="70 MW",
        description=(
            "Located in Brandenburg near the town of Lieberose, Solarpark Lieberose is a pioneering photovoltaic installation "
            "in Germany. With a capacity of roughly 70 MW, the project was among the early large-scale PV deployments in the region, "
            "demonstrating solar energy’s viability in northern European climates. Its expansive array of solar panels contributes "
            "clean energy to Germany’s grid and supports the nation’s renewable portfolio."
        ),
        number_of_cells=233333,
        unit_price=2.40,
        completed_date="2011-01-01",
        is_completed=True,
    ),
]

panels = [
    DBPanel(
        panel_id="1",
        project_id="CSP_FR_001",
        description="Panel 1",
        cell_rows=8,
        cell_columns=5,
    ),
    DBPanel(
        panel_id="2",
        project_id="CSP_FR_001",
        description="Panel 2",
        cell_rows=8,
        cell_columns=5,
    ),
    DBPanel(
        panel_id="3",
        project_id="MSP_ES_001",
        description="Panel 2",
        cell_rows=5,
        cell_columns=3,
    ),
    DBPanel(
        panel_id="4",
        project_id="SLG_DE_001",
        description="Panel 3",
        cell_rows=9,
        cell_columns=5,
    ),
]


cells = [
    *[
        DBCell(
            cell_id=f"0_{i}",
            owner_id="1",
            panel_id="1",
            price=2.50,
            cell_index=i,
            color="blue",
        )
        for i in range(8 * 5 * 2)
    ],
    *[
        DBCell(
            cell_id=f"1_{i}",
            owner_id="1",
            panel_id="2",
            price=1.50,
            cell_index=i,
            color="blue",
        )
        for i in range(5 * 3)
    ],
    *[
        DBCell(
            cell_id=f"2_{i}",
            owner_id="1",
            panel_id="2",
            price=3.50,
            cell_index=i,
            color="blue",
        )
        for i in range(9 * 5)
    ],
]

user_projects = [
    DBUserProject(
        user_id="1",
        project_id="SLG_DE_001",
        percentage_owned=0.1,
        time_of_purchase="2025-02-21T12:00:00Z",
    ),
    DBUserProject(
        user_id="1",
        project_id="MSP_ES_001",
        percentage_owned=0.5,
        time_of_purchase="2025-02-21T12:00:00Z",
    ),
]

power_data_points = [
    DBPowerDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T08:00:00Z",
        value=150.0,
    ),
    DBPowerDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T09:00:00Z",
        value=175.0,
    ),
    DBPowerDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T10:00:00Z",
        value=200.0,
    ),
    DBPowerDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T11:00:00Z",
        value=180.0,
    ),
    DBPowerDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T12:00:00Z",
        value=210.0,
    ),
]

energy_data_points = [
    DBEnergyDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T08:00:00Z",
        value=150.0,
    ),
    DBEnergyDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T09:00:00Z",
        value=175.0,
    ),
    DBEnergyDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T10:00:00Z",
        value=200.0,
    ),
    DBEnergyDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T11:00:00Z",
        value=180.0,
    ),
    DBEnergyDataPoint(
        project_id="CSP_FR_001",
        timestamp="2025-02-21T12:00:00Z",
        value=210.0,
    ),
]


energy_prices = [
    DBEnergyPrice(
        bidding_zone="FR",
        timestamp="2025-02-21T08:00:00",
        price=50.0,
    ),
    DBEnergyPrice(
        bidding_zone="FR",
        timestamp="2025-02-21T09:00:00",
        price=55.0,
    ),
    DBEnergyPrice(
        bidding_zone="FR",
        timestamp="2025-02-21T10:00:00",
        price=60.0,
    ),
    DBEnergyPrice(
        bidding_zone="FR",
        timestamp="2025-02-21T11:00:00",
        price=65.0,
    ),
]


if __name__ == "__main__":
    from utils import create_database
    import os

    if os.path.exists("solar.db"):
        os.remove("solar.db")
    create_database()

    for user in users:
        insert("users", user)

    for project in projects:
        insert("projects", project)

    for panel in panels:
        insert("panels", panel)

    for cell in cells:
        insert("cells", cell)

    for user_project in user_projects:
        insert("user_projects", user_project)

    for energy_price in energy_prices:
        insert("energy_price", energy_price)

    for energy_data_point in energy_data_points:
        insert("energy_data", energy_data_point)

    for power_data_point in power_data_points:
        insert("power_data", power_data_point)
