from utils.logger import logger


def test_get_all_posts(client):
    logger.info("Testing GET /posts")

    response = client.get("posts")
    assert response.status_code == 200, "Expected 200 OK"

    posts = response.json()
    assert isinstance(posts, list), "Response should be a list"
    assert len(posts) == 100, "There should be 100 posts"
    
    for post in posts:
        assert isinstance(post, dict), "Each post should be a dictionary"

        assert "userId" in post, "Missing 'userId'"
        assert "id" in post, "Missing 'id'"
        assert "title" in post, "Missing 'title'"
        assert "body" in post, "Missing 'body'"

        assert isinstance(post["userId"], int)
        assert isinstance(post["id"], int)
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)
