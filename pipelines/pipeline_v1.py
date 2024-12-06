class PipelineBase:
    def __init__(self):
        pass

    def serve(self):
        raise NotImplementedError


class PipelineV1(PipelineBase):
    def __init__(self):
        super().__init__()

    def serve(self):
        print("PipelineV1 is serving")