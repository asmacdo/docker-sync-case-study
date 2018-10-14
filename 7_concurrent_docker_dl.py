from stages import PrintStage, PrintAndPassStage, ConcurrentRunner, run_pipeline, WaitUntilComplete

from mock_docker import DockerStart, DownloadContent


def docker_dl_intro():
    print("Now, lets wrap our download stage in a ConcurrentRunner to speed things up.")
    make_content = DockerStart(blobs=1, manifests=1, manifest_lists=1)
    print_and_pass = PrintAndPassStage()
    download_content = ConcurrentRunner(DownloadContent())
    print_end = PrintStage()
    stages = [make_content, print_and_pass, download_content, print_end]
    run_pipeline(stages)


docker_dl_intro()
