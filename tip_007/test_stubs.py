import time
from unittest.mock import MagicMock, create_autospec


class SentimentClassifier:
    def predict(self, text: str) -> str:
        # Imagine that prediction is taking a long time
        time.sleep(5)
        return "positive"


class EnrichBlogPost:
    def __init__(self, sentiment_classifier: SentimentClassifier) -> None:
        self._sentiment_classifier = sentiment_classifier

    def execute(self, blog_post: dict) -> dict:
        sentiment = self._sentiment_classifier.predict(blog_post["text"])
        blog_post["sentiment"] = sentiment
        return blog_post


class EnrichBlogPostWrongUsage:
    def __init__(self, sentiment_classifier: SentimentClassifier) -> None:
        self._sentiment_classifier = sentiment_classifier

    def execute(self, blog_post: dict) -> dict:
        sentiment = self._sentiment_classifier.classify(blog_post["text"])
        blog_post["sentiment"] = sentiment
        return blog_post


def test_blog_post_enriched_with_sentiment_magic_mock():
    sentiment_classifier = MagicMock()
    sentiment_classifier.predict.return_value = "positive"
    enrich_blog_post = EnrichBlogPost(sentiment_classifier=sentiment_classifier)
    blog_post = {"text": "I love Python"}

    enriched_blog_post = enrich_blog_post.execute(blog_post=blog_post)

    assert enriched_blog_post["sentiment"] == "positive"
    # This one is passes - usage and setup are correct


def test_blog_post_enriched_with_sentiment_create_autospec():
    sentiment_classifier = create_autospec(SentimentClassifier)
    sentiment_classifier.predict.return_value = "positive"
    enrich_blog_post = EnrichBlogPost(sentiment_classifier=sentiment_classifier)
    blog_post = {"text": "I love Python"}

    enriched_blog_post = enrich_blog_post.execute(blog_post=blog_post)

    assert enriched_blog_post["sentiment"] == "positive"
    # This one passes - usage and setup are correct


def test_blog_post_enriched_with_sentiment_wrong_usage_magic_mock():
    sentiment_classifier = MagicMock()
    sentiment_classifier.classify.return_value = "positive"
    enrich_blog_post = EnrichBlogPostWrongUsage(sentiment_classifier=sentiment_classifier)
    blog_post = {"text": "I love Python"}

    enriched_blog_post = enrich_blog_post.execute(blog_post=blog_post)

    assert enriched_blog_post["sentiment"] == "positive"
    # This one passes because test setup and usage are both wrong, but it should fail


def test_blog_post_enriched_with_sentiment_wrong_usage_create_autospec():
    sentiment_classifier = create_autospec(SentimentClassifier)
    sentiment_classifier.classify.return_value = "positive"
    enrich_blog_post = EnrichBlogPostWrongUsage(sentiment_classifier=sentiment_classifier)
    blog_post = {"text": "I love Python"}

    enriched_blog_post = enrich_blog_post.execute(blog_post=blog_post)

    assert enriched_blog_post["sentiment"] == "positive"
    # AttributeError: Mock object has no attribute 'classify'
    # This one fails because we're trying to use 'classify' which isn't present in SentimentClassifier