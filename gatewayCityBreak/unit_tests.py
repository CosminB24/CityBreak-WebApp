from main import app

def test_get_1():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <title>Gateway Service</title>\n</head>\n<body>\n    <h1>Welcome to the Gateway Service</h1>\n    <a href="/search">Search Events and Weather</a>\n</body>\n</html>' in response.data

def test_get_2():
    response = app.test_client().get('/search?city=Brasov&date=2024-08-03')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <title>Search Events and Weather</title>\n</head>\n<body>\n    <h1>Search for Events and Weather</h1>\n    <form method="post" action="/search">\n        <label for="city">City:</label>\n        <input type="text" id="city" name="city" required><br><br>\n        <label for="date">Date:</label>\n        <input type="date" id="date" name="date" required><br><br>\n        <button type="submit">Search</button>\n    </form>\n</body>\n</html>' in response.data

def test_get_3():
    response = app.test_client().get('/search/event')
    assert response.status_code == 404
    assert b'<!doctype html>\n<html lang=en>\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>\n' in response.data

