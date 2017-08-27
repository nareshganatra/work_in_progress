"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from google.cloud import bigquery

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    bq_test()
    return 'Hello World!'


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

def BigQuery_test():
    # Added by Naresh Ganatra
    # Instantiates a client

    client = bigquery.Client()

    query_results = client.run_sync_query("""
    SELECT
        APPROX_TOP_COUNT(corpus, 10) as title,
        COUNT(*) as unique_words
    FROM `publicdata.samples.shakespeare`;""")
    # Use standard SQL syntax for queries.
    # See: https://cloud.google.com/bigquery/sql-reference/
    query_results.use_legacy_sql = False
    query_results.run()
    query_results.fetch_data()

    # Drain the query results by requesting a page at a time.
    page_token = None
    while True:
        rows, total_rows, page_token = query_results.fetch_data(
            max_results=10,
            page_token=page_token)

        for row in rows:
            print(row)

        if not page_token:
            break
    print ("completed")


