# Python Flask Test App

Test Flask app, that crawls https://news.ycombinator.com.

### Technologies used:

- Python 3.8
- Flask
- docker
- docker-compose
- MongoDB
- pytest

---

## To run the project

1. Clone the project.
2. Run `docker-compose up --build -d`.
3. Visit `localhost:3000/posts`.

### API endpoints:

- `GET /posts` - retrieve saved posts. Parameters:
  - `order` - how to sort posts (default: '\_id');
  - `offset` - offset to start from (default: 0);
  - `limit` - limits number of returned posts (default: 5);

#### Additional info:

- Flask app is launched in one thread and interval timer, that crawls data, in another thread.
- Default scanning interval is 1200s (=20m).
- Posts contain 4 fields:
    - `title`
    - `url`
    - `_id`
    - `created`
- `title` and `url` fields are stripped.
- If `url` is relevant (leads to the same website) - it is converted to absolute path.
---

## To run tests

1. Clone the project.
2. Run `docker-compose up --build -d` to raise Mongo container.
3. Run `pytest` from cloned directory.
