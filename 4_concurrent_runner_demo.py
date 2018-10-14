from stages import PrintStage, ConcurrentRunner, run_pipeline

from mock_docker import DockerStart, DownloadContent


def concurrent_runner_demo():
    print("Each fake download takes time. We can improve performance by fake downloading"
          " more than one blob at a time. To do this, use the ConcurrentRunner Stage to wrap"
          " your download stage.")
    make_blobs = DockerStart(blobs=3)
    download_blobs = ConcurrentRunner(DownloadContent())
    print_them = PrintStage()
    stages = [make_blobs, download_blobs, print_them]
    run_pipeline(stages)


concurrent_runner_demo()
