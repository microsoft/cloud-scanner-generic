from requests import Session, Response
import logging


class RequestHelper:
    """Http request helper uses underlying Session object to pool http
    connections."""
    _session: Session = None

    @staticmethod
    def post(url, **kwargs) -> Response:
        """Creates a Session object if it does not already exist and performs
        an Http post on the object.

        Args:
            url: The url to post
            **kwargs: Additional arguments to pass to the underlying post method
        Returns:
            The Http Response
        """
        try:
            if RequestHelper._session is None:
                logging.info("Creating new requests Session")
                RequestHelper._session = Session()
            return RequestHelper._session.post(url, **kwargs)
        except Exception as ex:
            logging.error(str(ex))
