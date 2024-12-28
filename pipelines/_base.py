import logging

from base import BaseQuery, ComplexQuery, ImageQuery, TextQuery, TopKFinalists

class PipelineBase:
    def __init__(
        self,
    ):
        pass

    def get_name(self):
        return self.__class__.get_name

    """Serve the query"""

    def serve(self, query: BaseQuery) -> TopKFinalists:
        if type(query) == TextQuery:
            logging.info(f"{self.get_name()} is serving a text query.")
            return self._serve_text(query)
        elif type(query) == ImageQuery:
            logging.info(f"{self.get_name()} is serving an image query.")
            return self._serve_image(query)
        elif type(query) == ComplexQuery:
            logging.info(f"{self.get_name()} is serving a complex query.")
            return self._serve_complex(query)

    def _serve_text(self, query: TextQuery) -> TopKFinalists:
        raise NotImplementedError

    def _serve_image(self, query: ImageQuery) -> TopKFinalists:
        raise NotImplementedError

    def _serve_complex(self, query: ComplexQuery) -> TopKFinalists:
        raise NotImplementedError
