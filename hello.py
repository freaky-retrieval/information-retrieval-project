from pipelines.pipeline_v1 import PipelineV1


def main():
    pipeline = PipelineV1()
    pipeline.serve()

if __name__ == "__main__":
    main()
