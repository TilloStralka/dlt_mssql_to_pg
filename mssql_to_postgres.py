import sys
import logging
from datetime import datetime
from pathlib import Path

import dlt
from dlt.sources.sql_database import sql_database


# Log-Ordner und Logdatei pro Lauf
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / f"mssql_to_postgres_{datetime.now():%Y%m%d_%H%M%S}.log"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def load_mssql_to_postgres() -> None:
    schema_name = "dbo"
    table_name = "AWBuildVersion"
    dataset_name = "adventureworks"

    try:
        logger.info("Starte Datenübertragung MSSQL -> PostgreSQL")

        pipeline = dlt.pipeline(
            pipeline_name="mssql_to_postgres",
            destination="postgres",
            dataset_name=dataset_name,
            progress="log"
        )

        logger.info("Pipeline Name: %s", pipeline.pipeline_name)
        logger.info("Ziel: %s", pipeline.destination)
        logger.info("Dataset / Ziel-Schema: %s", dataset_name)
        logger.info("Quell-Schema: %s", schema_name)
        logger.info("Quell-Tabelle: %s", table_name)
        logger.info("Logdatei: %s", LOG_FILE)

        source = sql_database(
            schema=schema_name
        ).with_resources(table_name)

        load_info = pipeline.run(
            source,
            write_disposition="replace"
        )

        logger.info("Übertragung erfolgreich abgeschlossen")

        if hasattr(load_info, "loads_ids"):
            logger.info("Load IDs: %s", load_info.loads_ids)

        logger.info("Load Info:")
        logger.info("%s", load_info)

    except Exception:
        logger.exception("Fehler bei der Datenübertragung")
        sys.exit(1)


if __name__ == "__main__":
    load_mssql_to_postgres()