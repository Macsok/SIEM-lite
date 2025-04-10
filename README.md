# SIEM-lite
...

# Setting up
...

# Query
To query the Elasticsearch database, you can use the following methods:

### Simple Query
You can perform a simple query using the URL format:
```
http://localhost:9200/loghub-logs-*/_search?q=field_name:phrase&size=number_of_results&pretty
```
- Replace `index_name` with the name of your index.
- Replace `field_name` with the field you want to search.
- Replace `phrase` with the search term.
- Replace `number_of_results` with the number of results you want to retrieve.

### Advanced Query
For more advanced queries, you can use the `curl` command with a JSON payload:
```
curl -X GET "http://localhost:9200/loghub-logs-*/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_phrase": {
      "field_name": "search_term"
    }
  }
}'
```
- Replace `index_name` with the name of your index.
- Replace `field_name` with the field you want to search.
- Replace `search_term` with the term you are looking for.

### Example Linux formatting
To search for documents where the `Content` field contains the phrase "brute force attack":
```
curl -X GET "http://localhost:9200/loghub-logs-*/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_phrase": {
      "Content": "ftpd"
    }
  }
}'
```
### Windows CMD formatting:
To search for documents where the `Content` field contains the phrase "brute force attack" formatting for Windows CMD:
```
curl -X GET "http://localhost:9200/loghub-logs-*/_search?pretty" -H "Content-Type: application/json" -d "{\"query\": {\"match_phrase\": {\"Content\": \"ftpd\"}}}"

```
Another example:
```
http://localhost:9200/loghub-logs-*/_search?q=type:linux_csv+Content:ftpd&size=100&pretty
```

> **Note:** The `*` in `loghub-logs-*` can be replaced with a specific time-based index, such as `loghub-logs-2023.10.01`, to narrow down the query to a specific date or time range.

# Notes
ElasticSearch guide: https://logz.io/blog/elasticsearch-tutorial/
