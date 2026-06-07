import dlt
from dlt.sources.sql_database import sql_database


def load_mssql_to_postgres() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="mssql_to_postgres",
        destination="postgres",
        dataset_name="adventureworks"
    )

    source = sql_database(
        schema="dbo"
    ).with_resources("AWBuildVersion")

    info = pipeline.run(
        source,
        write_disposition="replace"
    )

    print(info)


if __name__ == "__main__":
    load_mssql_to_postgres()