import os
import json
import psycopg2
from typing import Dict, Any

# Config for PostgreSQL
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# Validate required environment variables
required_env_vars = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )

# Query
query = """
select
  distinct
    s.name,
  staging_sponsors.name as source_sponsor_name,
  staging_sponsors.source_sponsor_id,
  staging_sponsors.source_name,
  case
    when staging_sponsors.global_sponsor_id = s.id then 'Mapped'
    else 'Unmapped'
  end as mapping_status,
  case
    when staging_sponsors.global_sponsor_id is not null then 'In Staging'
    else 'Not In Staging'
  end as staging_status
from
  leadinsights.tenant_sponsor_campaign tsc
join leadinsights.sponsor s on
  s.id = tsc.sponsor_id
left join (
  select
    distinct
        s1.global_sponsor_id,
    s1.name,
    s1.source_sponsor_id,
    s1.source_name
  from
    leadinsights_staging.campaign_sponsor_mapping csm
  join leadinsights_staging.sponsor s1 on
    s1.id = csm.sponsor_id
  where
    csm.campaign_id in ('08a33a97-aa91-546b-a3f7-496360af8a47', '5afb0696-d52f-5004-96a6-16ae135a0636', 'ef948a6c-af68-5fa0-9ad8-32539e7a4de7') --staging campaign ids
) staging_sponsors on
  s.id = staging_sponsors.global_sponsor_id
where
  tsc.campaign_id = '22f96b30-bda7-4120-a5fc-898bff147937' --global campaign id
order by
  s.name asc;
"""


def handler(event, context) -> Dict[str, Any]:
    """
    Lambda handler for fetching sponsor mapping data.

    Args:
        event: Lambda event object
        context: Lambda context object

    Returns:
        Dict containing statusCode, body, and headers
    """
    conn = None
    cursor = None

    try:
        # Connect to the Database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Execute query
        cursor.execute(query)
        results = cursor.fetchall()

        # Get column names for better response structure
        column_names = [desc[0] for desc in cursor.description]

        # Format results as list of dictionaries
        formatted_results = [dict(zip(column_names, row)) for row in results]

        return {
            "statusCode": 200,
            "body": json.dumps(
                {"data": formatted_results, "count": len(formatted_results)}
            ),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }

    except psycopg2.Error as db_error:
        print(f"Database error: {str(db_error)}")
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "error": "Database connection or query failed",
                    "message": str(db_error),
                }
            ),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "message": str(e)}),
            "headers": {"Content-Type": "application/json"},
        }

    finally:
        # Ensure connections are closed even if error occurs
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except:
            pass  # Connection might already be closed
