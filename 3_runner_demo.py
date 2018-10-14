from stages import PrintStage, run_pipeline

from mock_docker import DockerStart, DownloadContent


def runner_demo():
    """
    So far, each stage we created is only run 1 at a time. asyncio allows us to run all of the
    stages at once, but at any time, only 1 instance of each stage is running.

    For stages that use a lot of io, it is useful to run many instances of a stage concurrently.
    To do this, we use a Runner Stage.
    """
    print("Make a few fake blobs, and then fake download them in serial.")
    print("To simulate io, I've put a sleep statement in download.")
    make_blobs = DockerStart(blobs=3)
    download_blobs = DownloadContent()
    print_them = PrintStage()
    stages = [make_blobs, download_blobs, print_them]
    run_pipeline(stages)


runner_demo()
