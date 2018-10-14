from stages import PrintStage, PrintAndPassStage, ConcurrentRunner, run_pipeline, WaitUntilComplete

from mock_docker import DockerStart, DownloadContent, ProcessContent, SaveContent


def docker_dps():
    print("Now, lets download, process and save each one.")
    make_content = DockerStart(blobs=1, manifests=1, manifest_lists=1)
    download_content = ConcurrentRunner(DownloadContent())
    process = ProcessContent()
    save_stage = SaveContent()
    print_end = PrintStage()
    stages = [make_content, download_content, process, save_stage, print_end]
    run_pipeline(stages)

    print("Well, that may not have been what we intended...")
    print("The manifest lists are all DPS, but manifests and blobs aren't.")
    print("This is because each item only passes through the pipeline once,"
          " manifests and blobs were created in the ProcessContent stage, which "
          "simulates seeing this content in a manifest list file.")
    print()
    print()
    print("To solve this problem, we can just repeat the stages a couple times to"
          " handle the nested content as well.")
    make_content = DockerStart(blobs=1, manifests=1, manifest_lists=1)
    download_content = ConcurrentRunner(DownloadContent())
    process = ProcessContent()
    save_stage = SaveContent()
    print_end = PrintStage()
    stages = [make_content, download_content, process, save_stage, download_content, process,
              save_stage, download_content, process, save_stage, print_end]
    run_pipeline(stages)
    print("Hooray! That did it.")


docker_dps()
